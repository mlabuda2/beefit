import React, { Component } from 'react';
import NavbarHome from "./navbar_home";
import BMR from "./BMR";
import BMR2 from "./BMR2";
import BMI from "./BMI";

export default class Home extends Component {
  render() {
    return (
      <div>
        <NavbarHome />
        <BMR/>
        <BMR2/>
        <BMI/>
        <br/><br/><br/><br/><br/><br/>
      </div>
    );
  }
}
