import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { fetchDietPlans } from "../actions"

class DietPlanList extends Component {
  componentDidMount() {
    this.props.fetchDietPlans();
  }

  renderList() {
    return this.props.products.map(product => {
      return (
        <li
          key={product.name}
          className="list-group-item"
        >
          {product.name}
        </li>
      );
    });
  }
  render() {
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
    products: state.products
  };
}

export default connect(mapStateToProps, { fetchDietPlans })(DietPlanList);
