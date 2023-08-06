import os
from typing import Callable

from IPython.display import display
from ipywidgets import Layout, VBox
from ipywidgets import widgets

from qviz.loaders.base import supported_backends
from .base import UI

box_layout = Layout(display='flex',
                    align_items='stretch',
                    width='100%')


class DataIngestion(UI):

    def __init__(self, callback: Callable, data_path: str = 'data/'):
        self.callback = callback
        self.data_path = data_path

    def _choose_file(self):
        files = [f for f in os.listdir(self.data_path) if os.path.isfile(os.path.join(self.data_path, f))]

        display(widgets.HTML(
            value="Choose a file to load (file must be in the data folder):",
            placeholder='',
            description='',
        ))

        self.file_widget = widgets.Dropdown(
            options=files,
            value=files[0],
            description='',
            disabled=False,
            style={"description_width": "initial"}
        )
        display(self.file_widget)

        text_layout = Layout(display="flex", width="30%", align_items="stretch")

        self.separator_widget = widgets.Text(
            value='',
            placeholder='Separator',
            description='Separator:',
            disabled=False,
            layout=text_layout,
            style={"description_width": "initial"}
        )
        display(self.separator_widget)

        self.header_widget = widgets.Dropdown(
            options=["Yes", "No"],
            value="Yes",
            description='Infer headers:',
            disabled=False,
            style={"description_width": "initial"}
        )

        display(self.header_widget)

    def _dropdown_backends(self):
        self.backend_widget = widgets.Dropdown(
            options=supported_backends,
            value=supported_backends[0],
            description='Choose a backend:',
            disabled=False,
            style={"description_width": "initial"}
        )

        display(self.backend_widget)

        self.backend_widget.observe(self._form_backend)

    def _form_backend(self, *args):
        if self.backend_widget.value == "Cassandra":
            self._form_keyspace_table()

    def _get_loader_backend(self):
        if self.header_widget.value == "Yes":
            header = "infer"
        else:
            header = None

        if self.backend_widget.value == "Cassandra":
            from qviz.loaders.cassandra_loader import CassandraLoader

            self.ksp = self.ksp_widget.value
            self.table = self.table_widget.value

            if self.ksp is None or self.ksp == "" or self.table is None or self.table == "":
                self.error_message.value = "Please type a keyspace and a table."
                self.error_box.children = [self.error_message]
                return None
            sep = self.separator_widget.value or ','
            return CassandraLoader(file="data/" + self.file_widget.value, sep=sep, header=header,
                                   nrows=100)
        else:
            raise NotImplemented("Other loaders not implemented yet")

    def _form_keyspace_table(self):
        display(widgets.HTML(
            value="Type your desired keyspace and table names for your dataset:",
            placeholder='',
            description='',
        ))

        text_layout = Layout(display="flex", width="70%", align_items="stretch")

        self.ksp_widget = widgets.Text(
            value='',
            placeholder='Keyspace name',
            description='Keyspace name:',
            disabled=False,
            layout=text_layout,
            style={"description_width": "initial"}
        )
        display(self.ksp_widget)

        self.table_widget = widgets.Text(
            value='',
            placeholder='Table name',
            description='Table name:',
            disabled=False,
            layout=text_layout,
            style={"description_width": "initial"}
        )
        display(self.table_widget)

    def _error_item(self):
        self.error_message = widgets.HTML(
            value="",
            placeholder='',
            description=''
        )
        self.error_box = VBox(layout=box_layout)
        display(self.error_box)

    def _show_run(self):
        def run(b):
            self.error_message.value = ""
            self.error_box.children = []

            try:
                loader = self._get_loader_backend()
            except Exception as ex:
                with self.debug:
                    raise ex
                return

            if loader is None:
                with self.debug:
                    print("Loader is None. Should not happen.")

            with self.debug:
                print("Connected to database.")

            try:
                with self.debug:
                    print("Creating schema...")
                loader.create_schema(self.ksp, self.table)
                with self.debug:
                    print("Inserting data...")
                loader.insert_data()
            except Exception as ex:
                with self.debug:
                    raise ex
                return

            with self.debug:
                print("data inserted!")

            self.callback()
            self._on_finished_callback()

        run_button = widgets.Button(
            description='Run',
            disabled=False,
            button_style='',
            tooltip='Run'
        )

        display(run_button, self.debug)

        run_button.on_click(run)

    def display(self, on_finished: Callable = None):
        self._on_finished_callback = on_finished
        # output to debug
        self.debug = widgets.Output()

        self._choose_file()

        self._dropdown_backends()

        self._form_backend()

        self._error_item()

        self._show_run()
