import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { fetchDietPlans } from "../actions"

class DietPlanList extends Component {
  componentDidMount() {
    this.props.fetchDietPlans();
  }

  renderList() {
    return _.map(this.props.diet_plans, product => {
      return (
        <li
          key={product.name}
          className="list-group-item"
        >
          { product.name }
        </li>
      );
    });
  }
  render() {
    if (Object.keys(this.props.diet_plans).length == 0) {
      return (
        <div></div>
      );
    }
    return (
        <ul className="list-group col-sm-4">
          <button type="submit" className="btn btn-primary" onClick={() => this.props.history.push("/home")}>Back</button>
            {this.renderList()}
        </ul>
    );
  }
}

function mapStateToProps(state) {
  return {
    products: state.products,
    diet_plans: state.diet_plans
  };
}

export default connect(mapStateToProps, { fetchDietPlans })(DietPlanList);
