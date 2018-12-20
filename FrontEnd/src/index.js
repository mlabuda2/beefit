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

const createStoreWithMiddleware = applyMiddleware()(createStore);


ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
  <BrowserRouter>
    <div>
      <Switch>
        <Route path="/register" component={RegisterUser} />
        <Route path="/login" component={LoginUser} />
        <Route path="/home" component={RegisterUser} />
        <Route path="/" component={App} />
      </Switch>
    </div>
  </BrowserRouter>
  </Provider>,
  document.querySelector('.container-fluid'));
