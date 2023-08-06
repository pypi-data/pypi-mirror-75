import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Layout, VBox
from typing import Callable

from .base import UI

box_layout = Layout(display='flex',
                    align_items='stretch',
                    width='100%')


class DataPreparation(UI):

    def __init__(self, callback):
        self.callback = callback
        self.data_source = None
        self.data_source_args = None
        # framework init function
        self.framework = None
        # framework object
        self.preparation = None
        self.target_variable = None
        self.df = None

    def _choose_data_source(self):
        self.data_source_widget = widgets.Dropdown(
            options=["Cassandra"],
            value="Cassandra",
            description='Choose a data source:',
            disabled=False,
            style={"description_width": "initial"}
        )

        display(self.data_source_widget)

        self.data_source_widget.observe(self._form_data_source)
        self.data_source_widget.observe(self._form_data_target)

    def _set_framework(self):
        if self.framework_widget.value == "Spark":
            from qviz.adp import SparkAutomatedPreparation
            self.framework = SparkAutomatedPreparation

    def _choose_framework(self):
        self.framework_widget = widgets.Dropdown(
            options=["Spark"],
            value="Spark",
            description='Choose a framework:',
            disabled=False,
            style={"description_width": "initial"}
        )

        display(self.framework_widget)

        self.framework_widget.observe(self._set_framework)

    def _form_data_source(self):
        if self.data_source_widget.value == "Cassandra":
            display(widgets.HTML(
                value="Type an existing keyspace and table:",
                placeholder='',
                description=''
            ))
            self.source_ksp_widget, self.source_table_widget = self._form_keyspace_table("Source")

    def _form_keyspace_table(self, placeholder):
        text_layout = Layout(display="flex", width="70%", align_items="stretch")

        ksp_widget = widgets.Text(
            value='',
            placeholder=f'{placeholder} keyspace',
            description=f'{placeholder} keyspace:',
            disabled=False,
            layout=text_layout,
            style={"description_width": "initial"}
        )
        display(ksp_widget)

        table_widget = widgets.Text(
            value='',
            placeholder=f'{placeholder} table',
            description=f'{placeholder} table:',
            disabled=False,
            layout=text_layout,
            style={"description_width": "initial"}
        )
        display(table_widget)

        return ksp_widget, table_widget

    def _form_options_checkboxes(self):
        display(widgets.HTML(
            value="Check the desired preprocessing for the dataset:",
            placeholder='',
            description=''
        ))

        options = ["Interpolate missing values", "Remove outliers", "Encode categorical variables", "Scaling", "PCA"]
        self.checkboxes = [widgets.Checkbox(value=False, description=option) for option in options]

        box = VBox(self.checkboxes, layout=box_layout)
        display(box)

    def _form_missing_values(self):
        input_layout = Layout(display="flex", width="80%", align_items="stretch")

        missing_values_text = widgets.HTML(
            value="Enter here the possible missing values for your dataset separated by commas (NaNs and nulls already included)",
            placeholder='',
            description='',
        )

        self.args_widgets = {}

        self.args_widgets["missing_values_w"] = widgets.Text(
            value='',
            placeholder='Example: Empty, ,?',
            description='',
            disabled=False,
            layout=input_layout,
            style={"description_width": "initial"}
        )

        return VBox(children=[missing_values_text, self.args_widgets["missing_values_w"]], layout=box_layout)

    def _form_encode(self):
        encode_text = widgets.HTML(
            value="Choose a cardinality threshold to one-hot encode variables. All variables with greater cardinality will be label encoded:",
            placeholder='',
            description='',
        )

        self.args_widgets["encode_w"] = widgets.IntSlider(
            value=15,
            min=2,
            max=100,
            step=1,
            description='',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            style={"description_width": "initial",
                   "flex_flow": "column"}
        )

        return VBox(children=[encode_text, self.args_widgets["encode_w"]], layout=box_layout)

    def _form_scaling(self):
        scaling_text = widgets.HTML(
            value="Select the scaling method:",
            placeholder='',
            description='',
        )

        scaling_options = ["Choose a framework and connect to backend first."]
        self.args_widgets["scaling_w"] = widgets.RadioButtons(
            options=scaling_options,
            value=scaling_options[0],
            description='',
            disabled=False,
            style={"description_width": "initial"}
        )

        return VBox(children=[scaling_text, self.args_widgets["scaling_w"]], layout=box_layout)

    def _form_options(self):
        self._form_options_checkboxes()
        self.input_boxes = {}
        self.input_boxes["missing_values_box"] = self._form_missing_values()
        self.input_boxes["encode_box"] = self._form_encode()
        self.input_boxes["scaling_box"] = self._form_scaling()

        options_box = VBox(layout=box_layout)
        display(options_box)

        self.checkbox_options = {"interpolate_missing_values": False, "remove_outliers": False, "encode": False,
                                 "scale": False, "do_PCA": False}

        def on_checkbox_change(change):
            self.checkbox_options["interpolate_missing_values"] = self.checkboxes[0].value
            self.checkbox_options["remove_outliers"] = self.checkboxes[1].value
            self.checkbox_options["encode"] = self.checkboxes[2].value
            self.checkbox_options["scale"] = self.checkboxes[3].value
            self.checkbox_options["do_PCA"] = self.checkboxes[4].value

            options = []
            if self.checkbox_options["interpolate_missing_values"]:
                options.append(self.input_boxes["missing_values_box"])
            if self.checkbox_options["encode"]:
                options.append(self.input_boxes["encode_box"])
            if self.checkbox_options["scale"]:
                options.append(self.input_boxes["scaling_box"])

            options_box.children = options

        for item in self.checkboxes:
            item.observe(on_checkbox_change)

    def _progress_bar(self):
        self.progress = widgets.IntProgress(
            value=0,
            min=0,
            max=2,
            step=1,
            description='',
            bar_style='',  # 'success', 'info', 'warning', 'danger' or ''
            orientation='horizontal',
            style={"description_width": "initial"}
        )

        self.progress_box = VBox(layout=box_layout)
        display(self.progress_box)

    def _error_item(self):
        self.error_message = widgets.HTML(
            value="",
            placeholder='',
            description=''
        )
        self.error_box = VBox(layout=box_layout)
        display(self.error_box)

    def _parse_input(self):
        missing_values = None
        threshold_cardinality = None
        scaling_method = None

        args = {}

        if self.checkbox_options["interpolate_missing_values"]:
            missing_values = self.args_widgets["missing_values_w"].value.split(",")
        if self.checkbox_options["encode"]:
            threshold_cardinality = self.args_widgets["encode_w"].value
        if self.checkbox_options["scale"]:
            scaling_method = self.args_widgets["scaling_w"].value

        scaling_options = self.framework.get_scaling_options()
        self.target_variable = self.target_widget.value

        args["missing_values"] = missing_values
        args["remove_outliers"] = self.checkbox_options["remove_outliers"]
        args["threshold_cardinality"] = threshold_cardinality

        if scaling_method is not None:
            args["scaling_method"] = scaling_options.index(scaling_method)

        args["do_PCA"] = self.checkbox_options["do_PCA"]
        args["target_variable"] = self.target_variable

        return args

    def _init_progress(self, steps):
        self.progress.value = 0
        self.progress.max = len(list(filter(lambda step: step, steps))) + 3
        self.description = (widgets.HTML(
            value='',
            placeholder='',
            description=''
        ))
        self.description.value = "Preparing data..."
        self.progress_box.children = [self.description, self.progress]

    def _get_data_source(self):
        ksp = self.source_ksp_widget.value
        table = self.source_table_widget.value

        if ksp is None or ksp == "" or table is None or table == "":
            return None
        else:
            return ksp, table

    def _get_data_target(self):
        ksp = self.target_ksp_widget.value
        table = self.target_table_widget.value

        if ksp is None or ksp == "" or table is None or table == "":
            return None
        else:
            return ksp, table

    def _choose_target_variable(self):
        try:
            columns = self.df.columns
        except:
            columns = []

        display(widgets.HTML(
            value="Choose a target variable or leave None if you are looking for an unsupervised algorithm:",
            placeholder='',
            description='',
        ))

        self.target_widget = widgets.Dropdown(
            options=["None"] + columns,
            value="None",
            description='',
            disabled=False,
            style={"description_width": "initial"}
        )

        display(self.target_widget)

    def _form_data_target(self):
        if self.data_source_widget.value == "Cassandra":
            display(widgets.HTML(
                value="Type a non existing keyspace and table:",
                placeholder='',
                description='',
            ))
            self.target_ksp_widget, self.target_table_widget = self._form_keyspace_table("Target")

    def _connect_button(self):
        def connect(b):
            self.error_message.value = ""
            self.error_box.children = []

            data_source_args = self._get_data_source()
            if data_source_args is None:
                self.error_message.value = "Please choose a data source and click Connect."
                self.error_box.children = [self.error_message]
                return
            else:
                self.data_source_args = data_source_args

            with self.debug:
                print("Connecting...")

            try:
                self.preparation = self.framework()
            except Exception as ex:
                with self.debug:
                    raise ex
                return
            with self.debug:
                print("Connected!")

            try:
                self.df = self.preparation.get_df(self.data_source_widget.value, *self.data_source_args)
                self.target_widget.options = ["None"] + self.df.columns
                self.target_widget.value = self.target_widget.options[0]
                self.args_widgets["scaling_w"].options = self.framework.get_scaling_options()
                self.args_widgets["scaling_w"].value = self.args_widgets["scaling_w"].options[0]
            except Exception as ex:
                with open("UI_preparation_log.txt", "a") as f:
                    f.write(str(ex))
                with self.debug:
                    raise ex
                return

        connect_button = widgets.Button(
            description='Connect',
            disabled=False,
            button_style='',
            tooltip='Run'
        )

        display(connect_button, self.debug)

        connect_button.on_click(connect)

    def _show_run(self):
        def run(b):
            self.error_message.value = ""
            self.error_box.children = []

            try:
                if self.data_source_args is None:
                    self.error_message.value = "Please choose a data source and click Connect."
                    self.error_box.children = [self.error_message]
                    return

                data_target_args = self._get_data_target()
                if data_target_args is None:
                    self.error_message.value = "Please choose a data target."
                    self.error_box.children = [self.error_message]
                    return
                else:
                    self.data_target_args = data_target_args
            except Exception as ex:
                with self.debug2:
                    raise ex
                return

            try:
                args = self._parse_input()
                self._init_progress(args.values())

                self.description.value = "Initializing data source..."
                self.preparation.set_args(**args)
                self.progress.value += 1

                self.df = self.preparation.automated_data_preparation(self.df, self.description, self.progress)
                self.description.value = "Saving data..."
                self.preparation.save_df(self.df, self.data_source_widget.value, self.data_target_args)
                self.description.value = "Completed!"
                self.progress.value += 1
            except Exception as ex:
                with self.debug2:
                    print(self.data_target_args)
                    raise ex
                return

            self.callback(self.df)

        run_button = widgets.Button(
            description='Run',
            disabled=False,
            button_style='',
            tooltip='Run'
        )

        display(run_button, self.debug2)

        run_button.on_click(run)

    def display(self, on_finished: Callable = None):

        # output to debug
        self.debug = widgets.Output()
        self.debug2 = widgets.Output()

        self._choose_data_source()
        self._form_data_source()

        self._choose_framework()
        self._set_framework()

        self._connect_button()

        self._choose_target_variable()

        self._form_options()

        self._form_data_target()

        self._progress_bar()

        self._error_item()

        self._show_run()
