// Copyright (c) Cesare Cugnasco
// Distributed under the terms of the Modified BSD License.

import {
    DOMWidgetModel, DOMWidgetView, ISerializers, unpack_models, WidgetModel, WidgetView
} from '@jupyter-widgets/base'
import {
    MODULE_NAME, MODULE_VERSION
} from './version'

// Import the CSS
import '../css/widget.css'
import {Qviz} from "./qviz_extras"


export class ExampleModel extends DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: ExampleModel.model_name,
            _model_module: ExampleModel.model_module,
            _model_module_version: ExampleModel.model_module_version,
            _view_name: ExampleModel.view_name,
            _view_module: ExampleModel.view_module,
            _view_module_version: ExampleModel.view_module_version,
            value: 'Hello World'
        }
    }

    static serializers: ISerializers = {
        ...DOMWidgetModel.serializers,
        // Add any extra serializers here
    }

    static model_name = 'ExampleModel'
    static model_module = MODULE_NAME
    static model_module_version = MODULE_VERSION
    static view_name = 'ExampleView'   // Set to null if no view
    static view_module = MODULE_NAME   // Set to null if no view
    static view_module_version = MODULE_VERSION
}


export class ExampleView extends DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget')

        this.value_changed()
        // Python -> JavaScript update
        this.model.on('change:value', this.value_changed, this)
    }

    value_changed() {
        this.el.textContent = this.model.get('value')
    }
}


export class SourceModel extends DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: SourceModel.model_name,
            _model_module: SourceModel.model_module,
            _model_module_version: SourceModel.model_module_version,
            _view_name: SourceModel.view_name,
            _view_module: SourceModel.view_module,
            _view_module_version: SourceModel.view_module_version,
            metadata: null,
            URI: null
        }
    }

    static serializers: ISerializers = {
        ...DOMWidgetModel.serializers,
        // Add any extra serializers here
    }

    static model_name = 'SourceModel'
    static model_module = MODULE_NAME
    static model_module_version = MODULE_VERSION
    static view_name = 'SourceView';
    static view_module = MODULE_NAME;
    static view_module_version = MODULE_VERSION;


}

export class QvizModel extends DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: QvizModel.model_name,
            _model_module: QvizModel.model_module,
            _model_module_version: QvizModel.model_module_version,
            _view_name: QvizModel.view_name,
            _view_module: QvizModel.view_module,
            _view_module_version: QvizModel.view_module_version,
            selected: {}
        }


    }

    static serializers: ISerializers = {
        ...DOMWidgetModel.serializers,
        source: {deserialize: unpack_models},
        query_space: {deserialize: unpack_models},
        // Add any extra serializers here
    }

    static model_name = 'QvizModel';
    static model_module = MODULE_NAME;
    static model_module_version = MODULE_VERSION;
    static view_name = 'QvizView';
    static view_module = MODULE_NAME;
    static view_module_version = MODULE_VERSION;
}

export class QvizView extends DOMWidgetView {
    private qviz: Qviz
    private _new_dataset = true

    initialize(parameters: WidgetView.InitializeParameters): void {

        console.log("Qviz initialized")
    }

    render() {
        console.log('loading TableView reader')

        const d = document.createElement("div")
        d.classList.add("resizable")
        this.el.appendChild(d)
        this.qviz = new Qviz(d, this.model as QvizModel)
        /*this.el.classList.add('custom-widget')
        this.red_div = document.createElement('p')
        this.red_div.style.backgroundColor = 'red'

        this.el.appendChild(this.red_div)

        this.value_changed()
        // Python -> JavaScript update
        this.model.on('change:source', this.value_changed, this)
        this.model.get('source').on('change:keyspace', this.value_changed, this)*/
        this.model.get('source').on('change:URI', this.table_changed, this)
        //this.model.get('source').on('change:metadata', this.data_changed, this)
        this.model.on('change:frontend_data', this.data_changed, this)
        if (this.model.get("source").get("URI") != null) {
            this.data_changed()
        }


    }

    data_changed() {
        const frontendData = this.model.get("frontend_data") as PandasSplitLayout
        const source = this.model.get("source") as SourceModel
        const metadata = source.get("metadata")
        if (metadata == null || !frontendData.columns) {
            console.warn("Called data_changed() on an inconsistent state: there is no data.")
            return;
        }
        const indexed_columns: string[] = metadata.indexed_columns
        const ic_index = indexed_columns.map(ic => frontendData.columns.indexOf(ic))
        const columns: string[] = metadata.columns
        const not_index_columns = columns.flatMap(c => indexed_columns.indexOf(c)).filter(a => a >= 0)
        const ic3d = ic_index.slice(0, 3)
        const positions = frontendData.data.map(row =>
            ic3d.map(i => row[i])
        )
        /**
         * We use here as a color either the 4th indexed dimension or any other numerical
         * columns not index or as a last the 3rd indexed dimension
         */

        const color_position = ic_index[3] || not_index_columns[0] || ic_index[2]
        if (!color_position) {
            console.warn("Undefined color, dropping update")
            return
        }

        const colors: number[] = frontendData.data.map(row => row[color_position])
        const [min, max] = colors.reduce((mm, e, ci, a) =>
            [e < mm[0] ? e : mm[0], e > mm[1] ? e : mm[1]], [Number.MAX_VALUE, Number.MIN_VALUE])
        const data: PointSource = {
            positions: positions,
            colors: colors.map(i => (i - min) / (max - min)),
            index: frontendData.index,
            source: this.model.get("source")
        }

        this.qviz.addData(data, this._new_dataset)
        this._new_dataset = false
    }

    table_changed() {
        this._new_dataset = true
        console.log("super! " + this.model.get('source').get('URI'))
    }
}

/**
 * This class represents the data format interface between the Python core and Javascript.
 * @param positions is a list of 3D points into the space. These value can have all real values.
 * @param colors is a list of scalars with value from 0 to 1 that have to be codified in a color.
 *
 */
export interface PointSource {
    positions: Array<Array<number>>,
    colors: Array<number>,
    index: Array<any>,
    source: SourceModel
}

interface PandasSplitLayout {
    index: Array<any>,
    columns: Array<string>,
    data: Array<Array<any>>

}


export class QuerySpaceModel extends WidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: QuerySpaceModel.model_name,
            _model_module: QuerySpaceModel.model_module,
            _model_module_version: QuerySpaceModel.model_module_version,
            from_point: [],
            to_point: [],
            precision: 1.0,
            limit: 100
        }
    }

    static serializers: ISerializers = {
        ...DOMWidgetModel.serializers,
        // Add any extra serializers here
    }

    static model_name = 'QuerySpaceModel'
    static model_module = MODULE_NAME
    static model_module_version = MODULE_VERSION
}

