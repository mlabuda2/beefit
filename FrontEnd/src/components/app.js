import React, { Component } from 'react';
import NavbarMenu from "../containers/navbar_menu";
import FavoriteFood from "../components/favorite_food";
import FooterMenu from "./footer_menu";
import CalorieBurner from "./CalorieBurner";
import StartWithUs from "./start_with_us";


export default class App extends Component {
  render() {
    return (
      <div>
        <NavbarMenu/>
        <StartWithUs/>
        <FavoriteFood/>
        <CalorieBurner/>
        <FooterMenu/>
      </div>
    );
  }
}
