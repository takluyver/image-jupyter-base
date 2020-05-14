"""Jupyter server extension that offers a crash endpoint"""

__version__ = "1.0.0"

import logging
import sys

from notebook.base.handlers import IPythonHandler
from notebook.notebookapp import NotebookApp
from notebook.utils import url_path_join

log = logging.getLogger(__name__)


class CrashHandler(IPythonHandler):
    def get(self):
        log.warning("crash endpoint called. Exiting with code 123")
        sys.exit(123)


def load_jupyter_server_extension(nb_app: NotebookApp):
    web_app = nb_app.web_app
    host_pattern = '.*$'
    web_app.add_handlers(host_pattern, [
        (url_path_join(web_app.settings['base_url'], '/6901a7302f214e38847a60f514798a42/crash'), CrashHandler),
    ])
