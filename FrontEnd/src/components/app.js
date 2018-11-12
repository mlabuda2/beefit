import React, { Component } from 'react';
import NavbarMenu from "../containers/navbar_menu";
import FavoriteFood from "../components/favorite_food";
import FooterMenu from "../containers/footer_menu";
import CalorieBurner from "./CalorieBurner";


export default class App extends Component {
  render() {
    return (
      <div>
        <NavbarMenu/>
        <FavoriteFood/>
        <CalorieBurner/>
        <FooterMenu/>
      </div>
    );
  }
}
