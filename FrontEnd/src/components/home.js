import React, { Component } from 'react';
import NavbarHome from "./navbar_home";
import FooterMenu from "./footer_menu";
import BMR from "./BMR";
import BMR2 from "./BMR2";
import BMI from "./BMI";

export default class Home extends Component {
  render() {
    return (
      <div>
        <NavbarHome />
        <p><BMI/></p>
        <p><BMR/></p>
        <p><BMR2/></p>
        <br/><br/><br/><br/><br/><br/>
        <FooterMenu />
      </div>
    );
  }
}
