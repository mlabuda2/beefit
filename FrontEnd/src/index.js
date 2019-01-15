import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import promise from "redux-promise";

import reducers from './reducers';
import App from './components/app';
import RegisterUser from './components/register_user';
import LoginUser from './components/login_user';
import Home from './components/home';
import DietPlanList from './components/diet_plan_list';
import DietPlanItem from './components/diet_plan_item';

const createStoreWithMiddleware = applyMiddleware(promise)(createStore);


ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
  <BrowserRouter>
    <div>
      <Switch>
        <Route exact path="/register" component={RegisterUser} />
        <Route exact path="/home" component={Home} />
        <Route exact path="/home/diet-plans" component={DietPlanList} />
        <Route exact path="/home/diet-plans/:id" component={DietPlanItem} />
        <Route exact path="/" component={App} />
      </Switch>
    </div>
  </BrowserRouter>
  </Provider>,
  document.querySelector('.container-fluid'));
