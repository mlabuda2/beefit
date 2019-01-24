import React, { Component } from 'react';
import NavbarMenu from "../components/navbar_menu";
import MainBody from "../components/main_body";





export default class App extends Component {
  render() {
    return (
      <div>
        <NavbarMenu/>
        <MainBody/>
      </div>
    );
  }
}
