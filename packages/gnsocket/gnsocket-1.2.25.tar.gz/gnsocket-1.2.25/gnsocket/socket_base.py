import socket
from basic_queuetools.queue import read_queue_gen
from gnsocket.gn_socket import GNCSocket
# Standar lib
import asyncio
import functools
from multiprocessing import Manager, Queue, Lock

# contrib modules
import ujson as json

# Own module
from gnsocket.gn_socket import GNCSocket
from gnsocket.exceptions import clean_exception

# module tasktools
from tasktools.taskloop import coromask, renew, simple_fargs
from networktools.colorprint import gprint, bprint, rprint

from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps
from networktools.library import my_random_string
from asyncio import shield

import ujson as json
import re
from networktools.path import home_path

tsleep = 2


class GNCSocketBase:

    def __init__(self, queue_n2t,
                 queue_t2n,
                 mode,
                 callback_exception=clean_exception,
                 *args,
                 **kwargs):
        self.qn2t = queue_n2t
        self.qt2n = queue_t2n
        self.address = kwargs.get('address', ('localhost', 6666))
        self.log_path = kwargs.get('log_path', '~/gnsocket_log')
        self.mode = mode
        self.exception = callback_exception
        self.timeout = kwargs.get("timeout", 20)
        self.raise_timeout =  kwargs.get("raise_timeout", False)
        self.client = None
        self.client_name = kwargs.get('client_name',"test")
        self.commands = {
        }

    async def sock_write(self, gs, *args, **kwargs):
        queue = self.qn2t
        await asyncio.sleep(1)
        for idc in list(gs.clients.keys()):
            try:
                for msg in read_queue_gen(queue, fn_name='sock_write'):
                    msg_send = json.dumps(msg)
                    idc_server = msg.get('idc_server')
                    try:
                        send_msg = gs.send_msg(msg_send, idc)
                        await send_msg
                    except BrokenPipeError as be:
                        gs.report("sock_write","Close->Broken Pipe Error al cerrar %s bytes" %(be))
                        gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                            te, gs.mode))
                        await asyncio.sleep(1)
                        continue
                    except socket.error as se:
                        gs.report("socke_write","Close->Socket Error al leer %s bytes" %(se))
                        await asyncio.sleep(1)
                        continue
                    except asyncio.TimeoutError as te:
                        gs.report("sock write", "Timeout error A", te)
                        gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                            te, gs.mode))
                        await asyncio.sleep(1)
                        continue
                    except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                        gs.report("sock write", "Error de conexion", conn_error, gs.mode)
                        gs.logger.exception("Excepción por desconexión %s, mode %s"%(
                            conn_error,gs.mode))
                        await asyncio.sleep(1)
                        gs.set_status(False)
                        del gs.clients[idc]
                        continue
                    except Exception as ex:
                        gs.on_new_client(self.client_name)
                        gs.report("sock write", "Exepción", ex)
                        gs.logger.exception("Error con modulo cliente gnsocket coro write %s" %ex)
                        print("Error con modulo de escritura del socket IDC %s" % idc)
                        continue
            except asyncio.TimeoutError as te:
                gs.report("sock write", "Timeout error B",te)
                gs.logger.exception("HEARTBEAT: Tiempo fuera en escritura %s, mode %s" %(
                    te, gs.mode))
                await asyncio.sleep(10)
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                gs.report("sock write", "Error de conexion", conn_error, gs.mode)
                gs.logger.exception("HEARTBEAT: Excepción por desconexión %s, mode %s"%(
                    conn_error,gs.mode))
                await asyncio.sleep(10)
                gs.set_status(False)
                del gs.clients[idc]
            except Exception as ex:
                gs.report("sock write", "Exepción", ex)
                gs.logger.exception("HEARTBEAT: Error con modulo cliente gnsocket coro write %s" %ex)
                gs.report("sock_write","Error con modulo de escritura del socket IDC %s" % idc)
        else:
            await asyncio.sleep(2)
        return [gs, *args], kwargs
    # socket communication terminal to engine

    async def sock_read(self, gs, *args, **kwargs):
        queue_t2n = self.qt2n
        msg_from_engine = []
        await asyncio.sleep(1)
        for idc in list(gs.clients.keys()):
            try:
                print("Recibiendo msg")
                recv_msg = gs.recv_msg(idc)
                datagram = await recv_msg
                if datagram not in {'', "<END>", 'null', None}:
                    msg_dict = json.loads(datagram)
                    if 'SOCKET_COMMAND' in msg_dict:
                        msg_dict['socket_id']=idc
                        self.check_msg(msg_dict)
                    else:
                        msg = {'dt': msg_dict, 'idc': idc}
                        queue_t2n.put(msg)
            except BrokenPipeError as be:
                gs.report("sock_read","Close->Broken Pipe Error al cerrar %s bytes" %(be))
                gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                    te, gs.mode))
                await asyncio.sleep(1)
                continue
            except socket.error as se:
                gs.report("socke_read","Close->Socket Error al leer %s bytes" %(se))
                await asyncio.sleep(1)
                continue
            except asyncio.TimeoutError as te:
                gs.report("sock_read", "Timeout error A",te)
                gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                    te, gs.mode))
                await asyncio.sleep(2)
                continue
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                gs.report("sock_read", "Error de conexion", conn_error, gs.mode)
                gs.logger.exception("Excepción por desconexión %s, mode %s"%(
                    conn_error, gs.mode))
                await asyncio.sleep(2)
                gs.set_status(False)
                del gs.clients[idc]
                if self.exception:
                    self.exception(conn_error, gs, idc)
                continue
            except Exception as ex:
                gs.report("sock_read", "Exepción", ex)
                rprint(ex)
                gs.logger.exception("Error con modulo cliente gnsocket coro read %s" %ex)           
                gs.report("sock_read","Some error %s en sock_read" % ex)
                continue
        else:
            await asyncio.sleep(2)
            idc = self.client
        return [gs, *args], kwargs

    def check_msg(self, msg):
        command = msg.get('SOCKET_COMMAND', "print")
        callback = self.commands.get(command, print)
        callback(**msg)


    def set_socket_task(self, callback_socket_task):
        self.socket_task = callback_socket_task
