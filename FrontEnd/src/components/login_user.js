import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { Field, reduxForm } from "redux-form";
import { connect } from "react-redux";
import { loginUser, isAuthenticated } from "../actions";

class LoginUser extends Component {
  // componentDidMount() {
  //   this.props.isAuthenticated((response) => {
  //     console.log("Status: " + response.data['message']);
  //     this.props.history.push("/home");
  //   }, (error) => console.log("Status: " + error.response.data['message']))
  // }

  renderField(field) {
    const { meta: { touched, error } } = field;
    const className = `form-group ${touched && error ? "has-danger" : ""}`;

    return (
      <div className={className}>
        <label>{field.label}</label>
        <input className="form-control" type={this.type} {...field.input} />
        <div className="text-help">
          {touched ? error : ""}
        </div>
      </div>
    );
  }

  onSubmit(values) {
    this.props.loginUser(values, (response) => {
      // console.log(response.data['token']);
      localStorage.setItem('t8k3n', response.data['token']);
      this.props.history.push("/home");
    });
  }

  checkToken() {
    let token = localStorage.getItem('t8k3n');
    if (token) {
      this.props.history.push("/home");
    }
  }

  render() {
    const { handleSubmit } = this.props;
    this.checkToken()

    return (
      <form className="form-inline" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
        <Field
          type="text"
          label="Username"
          name="username"
          component={this.renderField}
        />
        <Field
          type="password"
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
  // console.log(values) -> { username: 'asdf', password: 'asdf' }
  const errors = {};

  // Validate the inputs from 'values'
  if (!values.username) {
    errors.username = "Enter a username";
  }
  if (!values.password) {
    errors.password = "Enter a password";
  }

  // If errors is empty, the form is fine to submit
  // If errors has *any* properties, redux form assumes form is invalid
  return errors;
}

export default withRouter(reduxForm({
  validate,
  form: "LoginUserForm"
})(connect(null, { loginUser, isAuthenticated })(LoginUser)));
