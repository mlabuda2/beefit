import { combineReducers } from 'redux';
import { reducer as formReducer } from "redux-form";
import ProductsReducer from "./reducer_products";

const rootReducer = combineReducers({
  products: ProductsReducer,
  form: formReducer
});

export default rootReducer;
