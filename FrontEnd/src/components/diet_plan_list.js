import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { fetchDietPlans } from "../actions"

class DietPlanList extends Component {
  componentDidMount() {
    const { diet_plans } = this.props;
    // if (diet_plans === null || diet_plans.length == 0) {
    if (Object.keys(diet_plans).length == 0) {
      this.props.fetchDietPlans();
    }
  }
  // componentDidMount() {
  //   this.props.fetchDietPlans();
  // }

  renderList() {
    const { diet_plans } = this.props;
    return _.map(this.props.diet_plans, plan => {
    // const { diet_plans } = this.props;
    // return diet_plans.map(plan => {
      return (
        <li key={plan.name} className="list-group-item" style={{cursor: 'pointer'}} onClick={() =>
          this.props.history.push(`/home/diet-plans/${plan.id_plan}`)}>
          { plan.name }
        </li>
      );
    });
  }
  render() {
    // if (Object.keys(this.props.diet_plans).length == 0) {
    const { diet_plans } = this.props;
    if (diet_plans === null || diet_plans.length == 0) {
      return (
        <div>
          <button type="submit" className="btn btn-primary" onClick={() => this.props.history.push("/home")}>Back</button>
          <button type="submit" className="btn btn-success" onClick={() => this.props.history.push("/home/diet-plans/assign_plan")}>Create new plan</button>
        </div>
      );
    }
    return (
        <ul className="list-group col-sm-4">
          <button type="submit" className="btn btn-primary" onClick={() => this.props.history.push("/home")}>Back</button>
          <button type="submit" className="btn btn-success" onClick={() => this.props.history.push("/home/diet-plans/assign_plan")}>Create new plan</button>
            {/* console.log(diet_plans) */}
            {this.renderList()}
        </ul>
    );
  }
}

function mapStateToProps(state) {
  return {
    diet_plans: state.diet_plans
  };
}

export default connect(mapStateToProps, { fetchDietPlans })(DietPlanList);
