import React, { Component } from 'react';
import NavbarHome from "./navbar_home";
import BMR from "./BMR";
import BMI from "./BMI";

export default class Home extends Component {
  render() {
    return (
      <div>
        <NavbarHome />
        <BMI/>
        <BMR/>
        <br/><br/><br/><br/><br/><br/>
      </div>
    );
  }
}
