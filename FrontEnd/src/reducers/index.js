import { combineReducers } from 'redux';
import { reducer as formReducer } from "redux-form";
import ProductsReducer from "./reducer_products";
import DietPlansReducer from "./reducer_diet_plans";
import SelectedDietPlanReducer from "./reducer_selected_diet_plan";

const rootReducer = combineReducers({
  products: ProductsReducer,
  diet_plans: DietPlansReducer,
  selected_diet_plan: SelectedDietPlanReducer,
  form: formReducer
});

export default rootReducer;
