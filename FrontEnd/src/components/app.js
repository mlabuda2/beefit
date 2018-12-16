import React, { Component } from 'react';
import NavbarMenu from "../components/navbar_menu";
import FavoriteFood from "../components/favorite_food";
import FooterMenu from "./footer_menu";
import CalorieBurner from "./CalorieBurner";
import StartWithUs from "./start_with_us";
import BMR from "./BMR";


export default class App extends Component {
  render() {
    return (
      <div>
        <NavbarMenu/>
        <StartWithUs/>
        <FavoriteFood/>
        <CalorieBurner/>
        <BMR/>
        <FooterMenu/>
      </div>
    );
  }
}
