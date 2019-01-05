import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";

class DietPlan extends Component {
  render() {
    return (
        <button type="submit" className="btn btn-primary">Diet Plans</button>
    );
  }
}

export default withRouter(DietPlan);
