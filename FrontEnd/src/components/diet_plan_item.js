import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchDietPlans, deleteDietPlan } from "../actions";
import DayList from "./day_list";

class DietPlanItem extends Component {
  componentDidMount() {
    const { diet_plans } = this.props;
    // if (diet_plans === null || diet_plans.length == 0) {
    if (Object.keys(diet_plans).length == 0) {
      this.props.fetchDietPlans();
      console.log("DietPlan - componentDidMount: " + diet_plans);
    }
  }

  onDeleteClick() {
    console.log("Inside of: onDeleteClick()");
    const { id } = this.props.match.params;

    this.props.deleteDietPlan(id, () => {
      this.props.history.push("/home/diet-plans");
    });
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
        <button type="submit" className="btn btn-danger pull-xs-right" onClick={this.onDeleteClick.bind(this)}>DELETE</button>
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

export default connect(mapStateToProps, { fetchDietPlans, deleteDietPlan })(DietPlanItem);
