import React, { Component } from 'react';
import NavbarHome from "./navbar_home";
import FooterMenu from "./footer_menu";
import BMR from "./BMR";

export default class Home extends Component {
  render() {
    return (
      <div>
        <NavbarHome />
            <BMR/>
        <FooterMenu />
      </div>
    );
  }
}
