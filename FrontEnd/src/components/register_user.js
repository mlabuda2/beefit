import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { Field, reduxForm } from "redux-form";
import { connect } from "react-redux";
import { registerUser } from "../actions";

class RegisterUser extends Component {
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
    this.props.registerUser(values, () => {
      this.props.history.push("/");
    });
  }

  render() {
    const { handleSubmit } = this.props;

    return (
      <form className="form-inline" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
        <Field
          label="Username"
          name="username"
          component={this.renderField}
        />
        <Field
          label="Password"
          name="password"
          component={this.renderField}
        />
        <Field
          label="Email"
          name="email"
          component={this.renderField}
        />
        <button type="submit" className="btn btn-primary">Register your account</button>
      </form>
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
  form: "RegisterUserForm"
})(connect(null, { registerUser })(RegisterUser)));
