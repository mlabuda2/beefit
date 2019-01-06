import _ from "lodash";
import { FETCH_DIET_PLANS } from "../actions";

export default function(state = [], action) {
  switch (action.type) {
    case FETCH_DIET_PLANS:
      return [action.payload.plan_details, ...state];
    default:
      return state;
  }
}
