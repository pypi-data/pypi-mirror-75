import asyncio
import socket
from basic_queuetools.queue import read_queue_gen
# contrib modules
import ujson as json

# Own module
from gnsocket.exceptions import clean_exception

# module tasktools
from networktools.colorprint import gprint, bprint, rprint


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
        self.raise_timeout = kwargs.get("raise_timeout", False)
        self.client = None
        self.client_name = kwargs.get('client_name', "test")
        self.commands = {
        }
        self.stop_read = {}
        self.stop_write = {}

    async def sock_write(self, gs, idc, *args, **kwargs):
        if not idc:
            idc = gs.relation.get(self.client_name)
        queue = self.qn2t
        await asyncio.sleep(1)
        if idc in list(gs.clients.keys()):
            if not self.stop_write[idc]:
                try:
                    for msg in read_queue_gen(queue, fn_name='sock_write'):
                        msg_send = json.dumps(msg)
                        idc_server = msg.get('idc_server')
                        try:
                            bprint(f"Enviando msg de vuelta {msg_send}")
                            send_msg = gs.send_msg(msg_send, idc)
                            await send_msg
                        except BrokenPipeError as be:
                            gs.report(
                                "sock_write", "Close->Broken Pipe Error al cerrar %s bytes" % (be))
                            gs.logger.exception("Tiempo fuera en escritura %s, mode %s" % (
                                be, gs.mode))
                            await asyncio.sleep(1)
                            continue
                        except socket.error as se:
                            gs.report(
                                "socke_write", "Close->Socket Error al leer %s bytes" % (se))
                            await asyncio.sleep(1)
                            continue
                        except asyncio.TimeoutError as te:
                            gs.report("sock write", "Timeout error A", te)
                            gs.logger.exception("Tiempo fuera en escritura %s, mode %s" % (
                                te, gs.mode))
                            await asyncio.sleep(1)
                            continue
                        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                            gs.report("sock write", "Error de conexion",
                                      conn_error, gs.mode)
                            gs.logger.exception("Excepción por desconexión %s, mode %s" % (
                                conn_error, gs.mode))
                            await asyncio.sleep(1)
                            gs.set_status(False)
                            del gs.clients[idc]
                            continue
                        except Exception as ex:
                            gs.on_new_client(self.client_name)
                            gs.report("sock write", "Exepción", ex)
                            gs.logger.exception(
                                "Error con modulo cliente gnsocket coro write %s" % ex)
                            print(
                                "Error con modulo de escritura del socket IDC %s" % idc)
                            continue
                except asyncio.TimeoutError as te:
                    gs.report("sock write", "Timeout error B", te)
                    gs.logger.exception("HEARTBEAT: Tiempo fuera en escritura %s, mode %s" % (
                        te, gs.mode))
                    await asyncio.sleep(10)
                except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                    gs.report("sock write", "Error de conexion",
                              conn_error, gs.mode)
                    gs.logger.exception("HEARTBEAT: Excepción por desconexión %s, mode %s" % (
                        conn_error, gs.mode))
                    await asyncio.sleep(10)
                    gs.set_status(False)
                    del gs.clients[idc]
                except Exception as ex:
                    gs.report("sock write", "Exepción", ex)
                    gs.logger.exception(
                        "HEARTBEAT: Error con modulo cliente gnsocket coro write %s" % ex)
                    gs.report(
                        "sock_write",
                        f"Error con modulo de escritura del socket IDC {idc}")
            kwargs["stop"] = self.stop_write[idc]
        else:
            await asyncio.sleep(2)
        return [gs, idc, *args], kwargs
    # socket communication terminal to engine

    async def sock_read(self, gs, idc, *args, **kwargs):
        if not idc:
            idc = gs.relation.get(self.client_name)
        queue_t2n = self.qt2n
        msg_from_engine = []
        await asyncio.sleep(1)
        if idc in list(gs.clients.keys()):
            try:
                recv_msg = gs.recv_msg(idc)
                datagram = await recv_msg
                if datagram not in {'', "<END>", 'null', None}:
                    msg_dict = json.loads(datagram)
                    if 'SOCKET_COMMAND' in msg_dict:
                        msg_dict['socket_id'] = idc
                        self.check_msg(msg_dict)
                    else:
                        msg = {'dt': msg_dict, 'idc': idc}
                        queue_t2n.put(msg)
            except BrokenPipeError as be:
                gs.report(
                    "sock_read", "Close->Broken Pipe Error al cerrar %s bytes" % (be))
                gs.logger.exception("Tiempo fuera en escritura %s, mode %s" % (
                    be, gs.mode))
                await asyncio.sleep(1)
            except socket.error as se:
                gs.report("socke_read",
                          "Close->Socket Error al leer %s bytes" % (se))
                await asyncio.sleep(1)
            except asyncio.TimeoutError as te:
                gs.report("sock_read", "Timeout error A", te)
                gs.logger.exception("Tiempo fuera en escritura %s, mode %s" % (
                    te, gs.mode))
                await asyncio.sleep(2)
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                gs.report("sock_read", "Error de conexion",
                          conn_error, gs.mode)
                gs.logger.exception("Excepción por desconexión %s, mode %s" % (
                    conn_error, gs.mode))
                await asyncio.sleep(2)
                gs.set_status(False)
                del gs.clients[idc]
                if self.exception:
                    self.exception(conn_error, gs, idc)
            except Exception as ex:
                gs.report("sock_read", "Exepción", ex)
                rprint(ex)
                gs.logger.exception(
                    f"Error con modulo cliente gnsocket coro read {ex}")
                gs.report("sock_read", f"Some error {ex} en sock_read")
        else:
            await asyncio.sleep(2)
            idc = self.client
        return [gs, idc, *args], kwargs

    def check_msg(self, msg):
        command = msg.get('SOCKET_COMMAND', "print")
        callback = self.commands.get(command, print)
        callback(**msg)

    def set_socket_task(self, callback_socket_task):
        self.socket_task = callback_socket_task
