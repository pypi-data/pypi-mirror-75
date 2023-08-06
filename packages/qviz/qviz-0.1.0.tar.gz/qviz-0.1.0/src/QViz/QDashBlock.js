import * as React from "react";
import {PureComponent} from "react";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import IconButton from "@material-ui/core/IconButton";
import {ZoomOutMap} from "@material-ui/icons";
import CardContent from "@material-ui/core/CardContent";

export default class QDashBlock extends PureComponent {
    constructor(props) {
        super(props);
        this.state = {onDrag: false};
        this.dragOn = () => this.setState({onDrag: true});
        this.dragOff = () => this.setState({onDrag: false});
    }

    render() {
        const {children, name, cardAction} = this.props;
        const {onDrag} = this.state;

        return (
            <Card className={onDrag ? 'drag-me' : ''}>
                <CardHeader title={name} className='box-title'
                            action={
                                <IconButton onMouseUp={this.dragOff}
                                            onMouseDown={this.dragOn}
                                >
                                    <ZoomOutMap color='secondary'/>
                                </IconButton>
                            }/>

                <CardContent className='box-content'>
                    {children}
                </CardContent>
                {cardAction}
            </Card>

        );

    }

}