import React, { Component } from "react";
import { connect } from "react-redux";

class Meal extends Component {
  render() {
    console.log("render:" + diet_plan)
    if (!diet_plan) {
      return (
        <div></div>
      );
    }
    return (
      <div>

      </div>
    );
  }
}

function mapStateToProps({ diet_plans }, ownProps) {
  return {
    diet_plan: diet_plans[ownProps.match.params.id],
    diet_plans: diet_plans
  };
}

export default connect(mapStateToProps)(Meal);
