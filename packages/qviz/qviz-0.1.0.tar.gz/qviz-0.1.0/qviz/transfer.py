import logging
from typing import List, Optional, Awaitable

import pyarrow as pa
import tornado.websocket
import numpy as np
from ipywidgets import Widget
from qviz._frontend import module_name, module_version
from traitlets import Unicode, Int, Enum



"""
Work in progress and experimental binary data transfer. 
"""
handlers: List[tornado.websocket.WebSocketHandler] = []


class DataPipe(Widget):
    """
    This class does the heavy work of moving over a WebSocket Arrows Table
    """
    _model_name = Unicode('DataPipeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    port = Int().tag(sync=True)
    status = Enum(default_value='CONNECTING',
                  values=['CONNECTING', 'CONNECTED', 'DISCONNECTED', 'TRANSFERRING']).tag(sync=True)
    last_obj_id = Unicode().tag(sync=True)

    def __init__(self, port: int = None, **kwargs):
        """
        Creates a DataFrame with  a specific Keyspace and Table name.

        :param keyspace: the data frame's keyspace
        :param table_name: the data frame name
        """
        super(DataPipe, self).__init__()
        self.data_mover = DataMover()
        if port is None:
            server = self.data_mover.listen(0)
            self.port = max(map(lambda a: a.getsockname()[1], server._sockets.values()))
        else:
            self.data_mover.listen(port)
            self.port = port
        self.status = 'CONNECTED'


class DataMover(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MoverHandler)]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            xsrf_cookies=True,
        )
        # settings = {}
        super(DataMover, self).__init__(handlers, **settings)


class MoverHandler(tornado.websocket.WebSocketHandler):
    transfer_id_pool = np.random.rand()

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def check_origin(self, origin: str):
        return True

    def open(self):
        handlers.append(self)

    def on_close(self):
        handlers.remove(self)

    def send_arrow_table(self, data: pa.Table, obj_id: str):
        logging.info(f"sending message of ${len(data)}")
        batches = data.to_batches()


        self.write_message({'code': 'START_TRANSFER',
                            'id': obj_id,
                            'size': data.nbytes,
                            'chunks': len(batches)})
        for batch in batches:
            self.write_message(batch.serialize().to_pybytes(), binary=True)

    def on_message(self, message):
        logging.info("got message %r", message)
