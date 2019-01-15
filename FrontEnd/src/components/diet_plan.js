import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchDietPlans } from "../actions";
import DayList from "./day_list";

class DietPlan extends Component {
  componentDidMount() {
    const { diet_plans } = this.props;
    // if (diet_plans === null || diet_plans.length == 0) {
    if (Object.keys(diet_plans).length == 0) {
      this.props.fetchDietPlans();
      console.log("DietPlan - componentDidMount: " + diet_plans);
    }
  }

  render() {
    const { diet_plan, diet_plans } = this.props;
    // console.log("render:" + diet_plan)
    if (!diet_plan) {
      return (
        <div></div>
      );
    }
    return (
      <div>
        <button type="submit" className="btn btn-primary" onClick={() => this.props.history.push("/home/diet-plans")}>Back</button>
        {diet_plan.name}
        {/* console.log(diet_plan) */}
        <DayList dayMeals={diet_plan.plan_details} />
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

export default connect(mapStateToProps, { fetchDietPlans })(DietPlan);
