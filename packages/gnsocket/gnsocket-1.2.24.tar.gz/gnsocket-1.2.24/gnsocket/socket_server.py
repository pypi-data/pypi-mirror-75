# Standar lib
import asyncio
import functools
from multiprocessing import Manager, Queue, Lock

# contrib modules
import ujson as json

# Own module
from gnsocket.gn_socket import GNCSocket
from gnsocket.socket_base import GNCSocketBase

# module tasktools
from tasktools.taskloop import coromask, renew, simple_fargs_out
from networktools.colorprint import gprint, bprint, rprint

from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps

from basic_queuetools.queue import read_queue_gen, send_queue

tsleep = 2
from asyncio import shield, wait_for, wait


class GNCSocketServer(GNCSocketBase):

    def __init__(self, queue_n2t, queue_t2n, *args, **kwargs):
        super().__init__(queue_n2t, queue_t2n, 'server', *args, **kwargs)
        self.set_socket_task(self.socket_task)
        self.commands = {
            'NEW_CLIENT': self.new_client
        }
        self.clients = {}

    def socket_task(self):
        print("Socket task...")
        with GNCSocket(mode=self.mode,
                       timeout=self.timeout,
                       raise_timeout=self.raise_timeout,
                       log_path=self.log_path) as gs:
            print("Iniciando Socket Task en modo %s" % self.mode)
            loop = asyncio.get_event_loop()
            self.loop = loop
            gs.set_address(self.address)
            gs.set_loop(loop)
            try:
                async def socket_io(reader, writer):
                    try:
                        idc = await gs.set_reader_writer(reader, writer)
                        gs.set_new_client(idc)
                        # First time welcome
                        welcome = json.dumps(
                            {"msg": "Welcome to socket", 'idc_server': idc})
                        await wait_for(gs.send_msg(welcome, idc), timeout=10)
                        await asyncio.sleep(0.1)
                        # task reade
                    except asyncio.TimeoutError as te:
                        gs.report("socket_task","Tiempo fuera en escritura %s, mode %s" %(
                            te, gs.mode) )
                        gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                            te, gs.mode))
                        await asyncio.sleep(10)
                    except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                        gs.report("socket_task","Excepción por desconexión %s, mode %s"%(
                            conn_error, gs.mode))
                        gs.logger.exception("Excepción por desconexión %s, mode %s"%(
                            conn_error, gs.mode))
                        await asyncio.sleep(10)                                                                                               
                    try:
                        args = [gs, idc]
                        task_1 = loop.create_task(
                            coromask(
                                self.sock_read,
                                args, {},
                                simple_fargs_out),
                            name='task_sock_read'
                        )
                        task_1.add_done_callback(
                            functools.partial(
                                renew,
                                task_1,
                                self.sock_read,
                                simple_fargs_out)
                        )
                        args = [gs, idc]
                        # task write
                        task_2 = loop.create_task(
                            coromask(
                                self.sock_write,
                                args, {},
                                simple_fargs_out),
                            name='task_sock_write'
                        )
                        task_2.add_done_callback(
                            functools.partial(
                                renew,
                                task_2,
                                self.sock_write,
                                simple_fargs_out)
                        )
                        args = [gs, idc]
                        #check_connection(self, idc, gs, *args, **kwargs
                        task_3 = loop.create_task(
                            coromask(
                                self.check_connection,
                                args, {},
                                simple_fargs_out),
                            name='task_check_connection'
                        )
                        task_3.add_done_callback(
                            functools.partial(
                                renew,
                                task_3,
                                self.check_connection,
                                simple_fargs_out))
                    except Exception as exe:
                        raise exe
                future = loop.create_task(
                    gs.create_server(socket_io, loop))
                if not loop.is_running():
                    loop.run_forever()
                else:
                    loop.run_until_complete(future)
            except KeyboardInterrupt as k:
                gs.report("socket_task","Closing with keyboard")
                gs.logger.exception("Cierre forzado desde teclado %s" %ex)                
                loop.run_until_complete(gs.wait_closed())
                raise k
            except Exception as ex:
                gs.report("socket_task", "Exception", ex)
                gs.logger.exception("Error con modulo cliente gnsocket %s" %ex)                                
                print("Otra exception", ex)

    def close(self):
        loop = asyncio.get_event_loop()
        loop.close()

    def new_client(self, value, name, socket_id, **kwargs):
        if name not in self.clients:
            self.clients[name] = dict()
            self.clients[name].update({
                socket_id:value
            })
            gprint(self.clients)
        else:
            self.clients[name].update({
                socket_id:value
            })
            # estable relacion entre id en server
            # e id cliente

    async def check_connection(self, gs, idc, *args, **kwargs):
        for client_name, collection in self.clients.items():
            for socket_id in list(collection.keys()):
                try:
                     hb_args, hb_kwargs = await gs.heart_beat(socket_id)
                     if hb_kwargs.get('results'):
                         await self.drop_client(
                             client_name,
                             socket_id,
                             gs)
                except Exception as e:
                    print("Heartbeat exception on check_connection")
                    raise e
        await asyncio.sleep(1)
        return [gs, idc, *args], kwargs

    def drop_client(self, client_name, socket_id, gs):
        if socket_id in self.clients[client_name]:
            del self.clients[client_name][socket_id]

