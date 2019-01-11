import _ from "lodash";
import { SELECTED_DIET_PLAN } from "../actions";

export default function(state = null, action) {
  switch (action.type) {
    case SELECTED_DIET_PLAN:
      return action.payload.data.my_diet_plans;
    default:
      return state;
  }
}
