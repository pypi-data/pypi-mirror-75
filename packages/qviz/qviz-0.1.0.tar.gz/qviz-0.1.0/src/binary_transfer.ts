import {DOMWidgetModel, ISerializers, WidgetModel} from "@jupyter-widgets/base";
import {MODULE_NAME, MODULE_VERSION} from "./version";
import {RecordBatch, Table} from "apache-arrow";

export class DataPipeModel extends WidgetModel {
    data: DatasetEntry = {}

    defaults() {
        return {
            ...super.defaults(),
            _model_name: DataPipeModel.model_name,
            _model_module: DataPipeModel.model_module,
            _model_module_version: DataPipeModel.model_module_version,
            port: 0
        };
    }

    static serializers: ISerializers = {
        ...DOMWidgetModel.serializers,
        // Add any extra serializers here,

    }

    static model_name = 'DataPipeModel';
    static model_module = MODULE_NAME;
    static model_module_version = MODULE_VERSION;
    socket: WebSocket;

    initialize(attributes: any, options: {
        model_id: string;
        comm?: any;
        widget_manager: any;
    }) {
        super.initialize(attributes, options);
        this.on("change:port", () => {
            this.connectTo(this.get('port'));
        }, this);

    }


    connectTo(port: number) {
        console.log(`Connecting to ${port}`);
        const socket = new WebSocket(`ws://localhost:${port}`);
        this.socket = socket;
        socket.onopen = () => {
            socket.send('{"body":"My name is John"}');
        };


        new Transfer(socket, this.data);


        socket.onclose = (event) => {
            if (event.wasClean) {
                console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            }
        };

        socket.onerror = (error: Event) => {
            console.log(`[error] ${error}`);
        };
    }

}


class Transfer {
    private _buffer: RecordBatch[] = [];
    private readonly _data: DatasetEntry;
    private _resolve: (value?: (PromiseLike<Table> | Table)) => void;
    private _reject: (reason?: any) => void;
    private _received = 0;
    private _current_obj: StartTransferMSG;
    private _socket: WebSocket;

    constructor(socket: WebSocket, data: DatasetEntry) {
        this._data = data;
        this._socket = socket;
        socket.onmessage = this.init_msg.bind(this);

    }

    init_msg(event: MessageEvent) {
        console.log(event);
        if (event.data instanceof Blob) {
            console.log("[DataPipe} received chunk");
            this._buffer[this._received] = event.data as unknown as RecordBatch;
            this._received += 1;
            if (this._received == this._current_obj.chunks) {
                console.log(`[DataPipe] transfer of chunks of object ${this._current_obj.id} completed`);
                const table = Table.from(this._buffer);
                this._resolve(table);
                console.log(this._buffer)
                console.log(table)
                this._received = 0;
            }
        } else {
            this._current_obj = JSON.parse(event.data);
            const {id, chunks} = this._current_obj;
            this._data[id] = new Promise<Table>((resolve, reject) => {
                this._resolve = resolve;
                this._socket.onerror = this._reject
            })
            this._buffer = new Array(chunks)
            this._received = 0;
            console.log(`[DataPipe} starting transmission ${id} chunk`);
        }


    }


}

interface DataPipeMSG {
    code: string,
    id: string
}

interface StartTransferMSG extends DataPipeMSG {
    size: number,
    chunks: number

}

interface DatasetEntry {
    [key: string]: Promise<Table>
}

