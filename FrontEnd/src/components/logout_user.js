import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { Field, reduxForm } from "redux-form";
import { connect } from "react-redux";

class LogoutUser extends Component {
  logoutUser() {
    localStorage.removeItem('t8k3n');
    this.props.history.push("/");
  }

  render() {
    return (
        <button type="submit" className="btn btn-primary" onClick={this.logoutUser.bind(this)}>Log Out</button>
    );
  }
}

export default withRouter(LogoutUser);
