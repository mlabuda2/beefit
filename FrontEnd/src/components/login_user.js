import React, { Component } from "react";
import { Field, reduxForm } from "redux-form";
import { connect } from "react-redux";
import { loginUser } from "../actions";

class LoginUser extends Component {
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
    this.props.loginUser(values, () => {
      this.props.history.push("/");
    });
  }

  render() {
    const { handleSubmit } = this.props;

    return (
      <form className="form-inline" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
        <Field
          label="Login"
          name="login"
          component={this.renderField}
        />
        <Field
          label="Password"
          name="password"
          component={this.renderField}
        />
        <button type="submit" className="btn btn-primary">Log In</button>
      </form>
    );
  }
}

function validate(values) {
  console.log(values)
  // console.log(values) -> { login: 'asdf', password: 'asdf' }
  const errors = {};

  // Validate the inputs from 'values'
  if (!values.login) {
    errors.login = "Enter a login";
  }
  if (!values.password) {
    errors.password = "Enter a password";
  }

  // If errors is empty, the form is fine to submit
  // If errors has *any* properties, redux form assumes form is invalid
  return errors;
}

export default reduxForm({
  validate,
  form: "LoginUserForm"
})(connect(null, { loginUser })(LoginUser));
