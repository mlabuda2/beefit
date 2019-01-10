import _ from "lodash";
import { FETCH_DIET_PLANS } from "../actions";

export default function(state = {}, action) {
  switch (action.type) {
    case FETCH_DIET_PLANS:
      let dietPlans = _.mapKeys(action.payload.data.my_diet_plans, "id_plan")
      console.log(dietPlans);
      // return action.payload.data.my_diet_plans;
      return dietPlans;
    default:
      return state;
  }
}
