import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { Field, reduxForm } from "redux-form";
import { connect } from "react-redux";
import { createDietPlans } from "../actions";

class AddNewDietPlan extends Component {
    renderField(field) {
        const { meta: { touched, error } } = field;
        const className = `form-group ${touched && error ? "has-danger" : ""}`;

        return (
            <div className={className}>
                <label>{field.label}</label>
                <input className="form-control" type="text" {...field.input} />
                <div className="text-help">
                    {touched ? error : ""}
                </div>
            </div>
        );
    }

    onSubmit(values) {
        this.props.createDietPlans(values, () => {
            this.props.history.push("/home/diet-plans");
        });
    }

    render() {
        const { handleSubmit } = this.props;

        return (
            <div className="container diet-plan">
                <h2>Twój plan</h2>
                <p><input name="Wpisz nazwę swojego planu"/></p>
                <form className="form-inline" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                    <div className="form-group col-lg-10 col-md-10 col-xs-12">
                        <label htmlFor="sel1">Monday</label>
                        <select className="form-control col-lg-3 col-md-3" id="sel1">
                            <option>Kurczak</option>
                            <option>Ryż</option>
                            <option>Mango</option>
                            <option>Tuńczyk</option>
                            <option>Wieprzowina</option>
                            <option>Cielęcina</option>
                            <option>Banan</option>
                        </select>
                        <input type="time" name="usr_time" className="time-input"/>
                        <select className="form-control">
                            <option>50</option>
                            <option>100</option>
                            <option>150</option>
                            <option>200</option>
                            <option>300</option>
                            <option>400</option>
                            <option>500</option>
                        </select>
                    </div>
                    <div className="form-group col-lg-10 col-md-10 col-xs-12">
                    <label htmlFor="sel1">Tuesday</label>
                        <select className="form-control col-lg-3 col-md-3" id="sel1">
                            <option>Kurczak</option>
                            <option>Ryż</option>
                            <option>Mango</option>
                            <option>Tuńczyk</option>
                            <option>Wieprzowina</option>
                            <option>Cielęcina</option>
                            <option>Banan</option>
                        </select>
                        <input type="time" name="usr_time" className="time-input"/>
                        <select className="form-control">
                            <option>50</option>
                            <option>100</option>
                            <option>150</option>
                            <option>200</option>
                            <option>300</option>
                            <option>400</option>
                            <option>500</option>
                        </select>
                    </div>
                    <div className="form-group col-lg-10 col-md-10 col-xs-12">
                        <label htmlFor="sel1">Wednesday</label>
                        <select className="form-control col-lg-3 col-md-3" id="sel1">
                            <option>Kurczak</option>
                            <option>Ryż</option>
                            <option>Mango</option>
                            <option>Tuńczyk</option>
                            <option>Wieprzowina</option>
                            <option>Cielęcina</option>
                            <option>Banan</option>
                        </select>
                        <input type="time" name="usr_time" className="time-input"/>
                        <select className="form-control">
                            <option>50</option>
                            <option>100</option>
                            <option>150</option>
                            <option>200</option>
                            <option>300</option>
                            <option>400</option>
                            <option>500</option>
                        </select>
                    </div>
                    <div className="form-group col-lg-10 col-md-10 col-xs-12">
                    <label htmlFor="sel1">Thursday</label>
                        <select className="form-control col-lg-3 col-md-3" id="sel1">
                            <option>Kurczak</option>
                            <option>Ryż</option>
                            <option>Mango</option>
                            <option>Tuńczyk</option>
                            <option>Wieprzowina</option>
                            <option>Cielęcina</option>
                            <option>Banan</option>
                        </select>
                        <input type="time" name="usr_time" className="time-input"/>
                        <select className="form-control">
                            <option>50</option>
                            <option>100</option>
                            <option>150</option>
                            <option>200</option>
                            <option>300</option>
                            <option>400</option>
                            <option>500</option>
                        </select>
                    </div>
                    <div className="form-group col-lg-10 col-md-10 col-xs-12">
                    <label htmlFor="sel1">Friday</label>
                        <select className="form-control col-lg-3 col-md-3" id="sel1">
                            <option>Kurczak</option>
                            <option>Ryż</option>
                            <option>Mango</option>
                            <option>Tuńczyk</option>
                            <option>Wieprzowina</option>
                            <option>Cielęcina</option>
                            <option>Banan</option>
                        </select>
                        <input type="time" name="usr_time" className="time-input"/>
                        <select className="form-control">
                            <option>50</option>
                            <option>100</option>
                            <option>150</option>
                            <option>200</option>
                            <option>300</option>
                            <option>400</option>
                            <option>500</option>
                        </select>
                    </div>
                    <div className="form-group col-lg-10 col-md-10 col-xs-12">
                        <label htmlFor="sel1">Saturday</label>
                        <select className="form-control col-lg-3 col-md-3" id="sel1">
                            <option>Kurczak</option>
                            <option>Ryż</option>
                            <option>Mango</option>
                            <option>Tuńczyk</option>
                            <option>Wieprzowina</option>
                            <option>Cielęcina</option>
                            <option>Banan</option>
                        </select>
                        <input type="time" name="usr_time" className="time-input"/>
                        <select className="form-control">
                            <option>50</option>
                            <option>100</option>
                            <option>150</option>
                            <option>200</option>
                            <option>300</option>
                            <option>400</option>
                            <option>500</option>
                        </select>
                    </div>
                    <div className="form-group col-lg-10 col-md-10 col-xs-12">
                        <label htmlFor="sel1">Sunday</label>
                        <select className="form-control col-lg-3 col-md-3" id="sel1">
                            <option>Kurczak</option>
                            <option>Ryż</option>
                            <option>Mango</option>
                            <option>Tuńczyk</option>
                            <option>Wieprzowina</option>
                            <option>Cielęcina</option>
                            <option>Banan</option>
                        </select>
                        <input type="time" name="usr_time" className="time-input"/>
                        <select className="form-control">
                            <option>50</option>
                            <option>100</option>
                            <option>150</option>
                            <option>200</option>
                            <option>300</option>
                            <option>400</option>
                            <option>500</option>
                        </select>
                    </div>
                    <button type="submit" className="btn btn-primary">Dodaj nowy plan</button>
                </form>
            </div>
        );
    }
}

function validate(values) {
    console.log(values)
    // console.log(values) -> { username: 'asdf', password: 'asdf', email: 'asdf' }
    const errors = {};

    // Validate the inputs from 'values'
    if (!values.username || (values.username).length < 3) {
        errors.username = "Enter a username that has at least 3 characters";
    }
    if (!values.password || (values.password).length < 8) {
        errors.password = "Enter a password that has at least 8 characters";
    }
    if (!values.email) {
        errors.email = "Enter an email";
    }

    return errors;
}

export default withRouter(reduxForm({
    validate,
    form: "AddNewDietForm"
})(connect(null, { createDietPlans })(AddNewDietPlan)));
