import { combineReducers } from 'redux';
import { reducer as formReducer } from "redux-form";
import ProductsReducer from "./reducer_products";
import DietPlansReducer from "./reducer_diet_plans";

const rootReducer = combineReducers({
  products: ProductsReducer,
  diet_plans: DietPlansReducer,
  form: formReducer
});

export default rootReducer;
