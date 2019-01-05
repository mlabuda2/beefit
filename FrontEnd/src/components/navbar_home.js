import React, { Component } from 'react';
import LogoutUser from "../components/logout_user";
import DietPlan from "../components/diet_plan";

export default class NavbarHome extends Component{

    render(){
        return(
          <nav className="navbar navbar-light bg-light">
            <div>
              <a className="navbar-brand" href="/home/diet-plans">Diet Plans</a>
            </div>
            <LogoutUser />
          </nav>
        );
    }

}
