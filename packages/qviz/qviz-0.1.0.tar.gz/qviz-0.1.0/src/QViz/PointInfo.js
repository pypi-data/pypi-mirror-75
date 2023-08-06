import React from "react";
import {PureComponent} from "react";
import Button from '@material-ui/core/Button';
import Autosuggest from "react-autosuggest";
//import ReactDataGrid from "react-data-grid";
import "./autosuggest.css";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import ListItemText from "@material-ui/core/ListItemText";
import ListItem from "@material-ui/core/ListItem";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import Badge from "@material-ui/core/Badge";
import Axios from "axios";
//import IconButton from "@material-ui/core/IconButton";

const basic_suggestions = [
    {
        label: "fraud",
    },
    {
        label: "normal"
    }
];

const getSuggestionValue = suggestion => suggestion.label;

// Use your imagination to render suggestions.
const renderSuggestion = suggestion => (
    <div>
        {suggestion.label}
    </div>
);

class PointInfo extends PureComponent {
    constructor(props) {
        super(props);
        const server = props.apiURL;
        this.state = {
            globalFeedback: [],
            pointFeedback: [],
            submissionValue: "",
            suggestions: []
        };

        this.getGlobalFeedback = () => {
            const {currentModel} = this.props;
            Axios.get(`${server}${currentModel}/feedback`)
                .then(({data}) => {
                    this.setState({globalFeedback: data})
                });

        };
        this.submitFeedback = (arg) => {
            const {item, currentModel} = this.props;
            Axios.post(`${server}${currentModel}/point/${item.id}/feedback`, JSON.stringify({label: arg})
            ).then(_ => {
                this.getGlobalFeedback();
                this.getPointFeedback();
            });
        };
        this.getPointFeedback = (arg) => {
            const {item, currentModel} = this.props;

            const body = {
                "label": arg,
            };
            console.log(body);
            Axios.get(`${server}${currentModel}/point/${item.id}/feedback`)
                .then(({data}) => {
                    this.setState({pointFeedback: data});
                });
        };
        this.handleSubmit = (event) => {
            if (event) event.preventDefault();
            this.submitFeedback(this.state.submissionValue);
            this.setState({submissionValue: ""});
        };
        this.onSuggestionsFetchRequested = (value) => {
            const inputValue = value.value.trim().toLowerCase();
            const inputLength = inputValue.length;
            const {currentModel} = this.props;

            Axios.get(`${server}${currentModel}/feedback`)
                .then(
                    (res) => {
                        const suggestions = res.data.length > 0 ? res.data : basic_suggestions;
                        const result = inputLength === 0 ? [] : suggestions.filter(suggestion =>
                            suggestion.label.toLowerCase().slice(0, inputLength) === inputValue
                        );
                        this.setState({suggestions: result});
                    }
                );
        };
        this.onSuggestionsClearRequested = () => this.setState({suggestions: []});
        this.onChangeSubmission = (event, {newValue}) => this.setState({submissionValue: newValue});
        this.maybeUpdate = () => {
            const {item, schema} = this.props;
            if (this.item !== item || this.schema !== schema) {
                this.item = item;
                this.schema = schema;
                this.getGlobalFeedback();
                this.getPointFeedback();
            }


        }

    }


    render() {
        const {item, schema} = this.props;
        if (item) {
            this.maybeUpdate();
            const {suggestions, submissionValue, globalFeedback, pointFeedback} = this.state;


            const columns_point = Object.values(schema).filter(a => a.kind !== 'regular').map(k => {
                const name = k.column_name;
                const value = item[name];
                return (<ListItem key={name} component="li">
                    <ListItemText>
                        <Typography variant="overline"
                                    style={{width: 100, display: 'inline-block', fontWeight: 'bold'}} gutterBottom>
                            {name}
                        </Typography>
                        <Typography variant="body1" display="inline">
                            {value}
                        </Typography>
                    </ListItemText>
                </ListItem>)
            });
            const pointFB = Object.values(pointFeedback).map(({label, count}) => {

                return (<ListItem key={label} component="li">
                    <ListItemText>
                        <Typography variant="overline"
                                    style={{width: 100, display: 'inline-block', fontWeight: 'bold'}} gutterBottom>
                            {label}
                        </Typography>
                        <Typography variant="body1" display="inline">
                            {count}
                        </Typography>
                    </ListItemText>
                </ListItem>)
            });

            return (
                <Container id="point-info" style={{margin: "auto"}}>
                    <List>
                        {columns_point}
                        <Divider/>
                        {pointFB}
                        <ListItem key="custom" component="li">
                            <form onSubmit={this.handleSubmit}>
                                <Autosuggest
                                    margin="normal"
                                    variant="outlined"
                                    suggestions={suggestions}
                                    onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
                                    onSuggestionsClearRequested={this.onSuggestionsClearRequested}
                                    getSuggestionValue={getSuggestionValue}
                                    renderSuggestion={renderSuggestion}
                                    inputProps={{
                                        value: submissionValue,
                                        placeholder: 'Use custom label',
                                        onChange: this.onChangeSubmission
                                    }}
                                />
                                <Button variant="contained" color="primary"
                                        onClick={() => this.handleSubmit()}>
                                    Submit
                                </Button>
                            </form>
                        </ListItem>
                        {globalFeedback.sort((a, b) => b.count - a.count)
                            .slice(0, 5)
                            .map((elem) => (
                                <ListItem>
                                    <Badge badgeContent={elem.count}>
                                        <Button variant="contained" color="secondary"
                                                onClick={(e) => {
                                                    this.submitFeedback(elem.label);
                                                    e.preventDefault();
                                                }}>{elem.label}
                                        </Button>
                                    </Badge>


                                </ListItem>))}
                    </List>

                </Container>);
        } else {
            return (<div/>);
        }

    }

}

export default PointInfo;