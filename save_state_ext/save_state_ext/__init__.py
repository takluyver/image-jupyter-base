"""Jupyter server extension for allowing long-running operations (like dumping python's whole state) to be executed
on a running kernel """

__version__ = "1.0.0"

import logging
from threading import Thread

from notebook.base.handlers import IPythonHandler
from notebook.notebookapp import NotebookApp
from notebook.utils import url_path_join

log = logging.getLogger(__name__)


class ExecutionHandler:
    def __init__(self, app: NotebookApp):
        self.app = app
        self.running = False
        self.execution_failed = None
        self.last_error = ''
        self.code = None
        self.client = None

    def handle_request(self, handler: IPythonHandler, code: str):
        if self.running:
            raise Exception("Execution already running")
        self.running = True
        try:
            kernel = self.find_kernel()
            self.client = kernel.blocking_client()
            log.debug("client created")
            self.client.start_channels()
            log.debug("channels started")
            self.code = code
            self.execution_failed = None
            Thread(target=self.start_execution).start()
        except Exception as e:
            self.running = False
            raise e
        handler.finish("started")

    def start_execution(self):
        log.info("start exec")
        self.client.execute_interactive(self.code, store_history=False, allow_stdin=False,
                                        output_hook=lambda msg: self.process_message(msg))
        log.info("execution done")
        self.client.stop_channels()
        log.debug("channels closed")
        if self.execution_failed is None:
            self.execution_failed = False
        self.running = False

    def process_message(self, msg):
        print(msg)
        if msg['header']['msg_type'] == 'error':
            self.execution_failed = True
            self.last_error = msg['content']['evalue']

    def handle_poll(self, handler: IPythonHandler):
        if self.running:
            handler.finish({'finished': False})
        elif self.execution_failed is None:
            handler.set_status(500)
            handler.finish("unknown status")
        else:
            ret = {'finished': True, 'success': not self.execution_failed}
            if self.execution_failed:
                ret['error'] = self.last_error
            handler.finish(ret)

    def find_kernel(self, kernel_name: str = 'python3'):
        log.info("find kernel")
        kernels = self.app.kernel_manager.list_kernels()
        kernels = [k for k in kernels if k['name'] == kernel_name]
        if len(kernels) <= 0:
            raise Exception(f'no {kernel_name} kernels found!')
        return self.app.kernel_manager._kernels[kernels[0]['id']]


execution_handler: ExecutionHandler = None


class SaveDumpHandler(IPythonHandler):
    def get(self):
        execution_handler.handle_request(self, 'save_dump()')


class LoadDumpHandler(IPythonHandler):
    def get(self):
        execution_handler.handle_request(self, 'load_dump()')


class PollDumpHandler(IPythonHandler):
    def get(self):
        execution_handler.handle_poll(self)


def load_jupyter_server_extension(nb_app: NotebookApp):
    global execution_handler
    if execution_handler is not None:
        raise Exception("execution handler already registered")
    execution_handler = ExecutionHandler(nb_app)
    web_app = nb_app.web_app
    host_pattern = '.*$'
    web_app.add_handlers(host_pattern, [
        (url_path_join(web_app.settings['base_url'], '/state/save'), SaveDumpHandler),
        (url_path_join(web_app.settings['base_url'], '/state/load'), LoadDumpHandler),
        (url_path_join(web_app.settings['base_url'], '/state/poll'), PollDumpHandler),
    ])
