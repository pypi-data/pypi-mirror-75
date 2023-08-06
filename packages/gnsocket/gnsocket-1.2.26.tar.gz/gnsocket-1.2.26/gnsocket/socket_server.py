# Standar lib
from asyncio import wait_for
import asyncio
import functools

# contrib modules
import ujson as json

# Own module
from gnsocket.gn_socket import GNCSocket
from gnsocket.socket_base import GNCSocketBase

# module tasktools
from tasktools.taskloop import TaskLoop
from networktools.colorprint import gprint, bprint, rprint

tsleep = 2


class GNCSocketServer(GNCSocketBase):

    def __init__(self, queue_n2t, queue_t2n, *args, **kwargs):
        super().__init__(queue_n2t, queue_t2n, 'server', *args, **kwargs)
        self.set_socket_task(self.socket_task)
        self.commands = {
            'NEW_CLIENT': self.new_client
        }
        self.clients = {}
        self.server = {}
        self.main_tasks = {}
        self.stop_check = False

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
                        gs.reading[idc] = False
                        self.stop_read[idc] = False
                        self.stop_write[idc] = False
                        self.server[idc] = asyncio.current_task()
                        gs.set_new_client(idc)
                        # First time welcome
                        welcome = json.dumps(
                            {"msg": "Welcome to socket", 'idc_server': idc})
                        await wait_for(gs.send_msg(welcome, idc), timeout=10)
                        await asyncio.sleep(0.1)
                        # task reade
                    except asyncio.TimeoutError as te:
                        gs.report(
                            "socket_task", f"Tiempo fuera en escritura {te}, mode {gs.mode}")
                        gs.logger.exception(
                            f"Tiempo fuera en escritura {te}, mode {gs.mode}")
                        await asyncio.sleep(10)
                    except (ConnectionResetError,
                            ConnectionAbortedError) as conn_error:
                        gs.report(
                            "socket_task", f"Excepción por desconexión {conn_error}, mode {gs.mode}")
                        gs.logger.exception(
                            f"Excepción por desconexión {conn_error}, mode {gs.mode}")
                        await asyncio.sleep(10)
                    try:
                        args = [gs, idc]
                        task_name = f"sock_read_{idc}"
                        task_sock_read = TaskLoop(self.sock_read, args,
                                                  **{
                                                      "name": task_name
                                                  })
                        task_sock_read.create()
                        bprint(f"Task read- > {task_sock_read}")
                        self.main_tasks[task_name] = task_sock_read
                        # task write
                        task_name = f"sock_write_{idc}"
                        task_sock_write = TaskLoop(self.sock_write, args,
                                                   **{
                                                       "name": task_name
                                                   })
                        self.main_tasks[task_name] = task_sock_write
                        bprint(f"Task write- > {task_sock_write}")
                        task_sock_write.create()
                        # check_connection(self, idc, gs, *args, **kwargs
                    except Exception as exe:
                        raise exe
                future = loop.create_task(
                    gs.create_server(socket_io, loop),)

                # activar tarea de control de conexión
                args = [gs, None]

                task_check = TaskLoop(self.check_connection, args,
                                      {},
                                      **{"name": "check_connection"})
                task_check.create()
                bprint(f"Task check- > {task_check}")

                if not loop.is_running():
                    loop.run_forever()
                else:
                    loop.run_until_complete(future)
            except KeyboardInterrupt as k:
                gs.report("socket_task", "Closing with keyboard")
                gs.logger.exception(f"Cierre forzado desde teclado {k}")
                loop.run_until_complete(gs.wait_closed())
                raise k
            except Exception as ex:
                gs.report("socket_task", "Exception", ex)
                gs.logger.exception(
                    "Error con modulo cliente gnsocket %s" % ex)
                print("Otra exception", ex)

    def close(self):
        loop = asyncio.get_event_loop()
        loop.close()

    def new_client(self, value, name, socket_id, **kwargs):
        if name not in self.clients:
            self.clients[name] = dict()
            self.clients[name].update({
                socket_id: value
            })
            gprint(self.clients)
        else:
            self.clients[name].update({
                socket_id: value
            })
            # estable relacion entre id en server
            # e id cliente

    async def check_connection(self, gs, idc, *args, **kwargs):
        bprint(f"Check connection {self.clients.keys()}")
        all_tasks = self.main_tasks.values()
        cancel_set = set()
        if not gs.queue_cancel.empty():
            for i in range(gs.queue_cancel.qsize()):
                idserver = gs.queue_cancel.get()
                cancel_set.add(idserver)
                rprint("="*10)
                bprint(f"Cancelando tarea en server {idserver}")
        for key, server in self.server.items():
            bprint(f"key {key}-> {server.get_name()}")
        for client_name, collection in self.clients.items():
            for socket_id in list(collection.keys()):
                try:
                    hb_args, hb_kwargs = await gs.heart_beat(socket_id)
                    rprint(f"{socket_id} ==== Test hb", hb_kwargs)
                    bprint(f"Cancel set: {cancel_set}")
                    if not hb_kwargs.get('result') or socket_id in cancel_set:
                        print(f"Droping tasks... for {socket_id}")
                        rprint(f"results...hb...{hb_kwargs}")
                        await self.drop_client(
                            client_name,
                            socket_id,
                            gs)
                except Exception as e:
                    print("Heartbeat exception on check_connection")
                    raise e
        await asyncio.sleep(3)
        return [gs, idc, *args], kwargs

    async def drop_client(self, client_name, socket_id, gs):
        if socket_id in self.clients[client_name]:
            # close tasks
            self.stop_read[socket_id] = True
            self.stop_write[socket_id] = True
            bprint(f"{socket_id} stop read {self.stop_read}")
            bprint(f"{socket_id} stop write {self.stop_write}")

            selected = [f"task_sock_write_{socket_id}"
                        f"task_sock_read_{socket_id}"]
            [bprint("Tarea Droping: {} {}".format(key, task.name)) for key, task
             in self.main_tasks.items()]

            for name in selected:
                for task in self.main_tasks.values():
                    print("Task alive", task.name)
                    print(
                        f"Cancelled {task.cancelled()} or done {task.done()}")
                    if name == task.name:
                        rprint(f"Cancelando tarea {task.get_name}")
                        task.stop()
                        await asyncio.sleep(.5)
                        task.cancel()
                        try:
                            task.result()
                        except asyncio.CancelledError as ce:
                            bprint(
                                f"tarea {task.get_name()} cancelada exitosamente")
            server_task = self.server.get(socket_id)
            if server_task:
                server_task.cancel()
                try:
                    server_task.result()
                except asyncio.CancelledError as ce:
                    bprint(
                        f"tarea {server_task.get_name()} cancelada exitosamente")
                    bprint(
                        f"tarea {server_task.get_name()} cancelada exitosamente")
                    bprint(f"Is server canceled? {server_task.cancelled()}")
                del self.server[socket_id]
            del self.clients[client_name][socket_id]
            rprint(f"Ids en cliente: {self.clients[client_name]}")
