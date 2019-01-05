import React, { Component } from 'react';
import NavbarHome from "./navbar_home";
import FooterMenu from "./footer_menu";


export default class Home extends Component {
  render() {
    return (
      <div>
        <NavbarHome />
        <FooterMenu />
      </div>
    );
  }
}
