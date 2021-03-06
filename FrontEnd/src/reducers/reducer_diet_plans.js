import _ from "lodash";
import { CREATE_DIET_PLANS, FETCH_DIET_PLANS, DELETE_DIET_PLAN } from "../actions";

export default function(state = {}, action) {
  switch (action.type) {
    case DELETE_DIET_PLAN:
      return _.omit(state, action.payload);
    case CREATE_DIET_PLANS:
      return [action.payload, ...state];
    case FETCH_DIET_PLANS:
      return _.mapKeys(action.payload.data.my_diet_plans, "id_plan")
    default:
      return state;
  }
}
