import  React from 'react';
import {Component} from 'react';
import LoginUser from "../components/login_user";

export default class NavbarMenu extends Component{

    render(){
        return(
            <nav className="navbar navbar-light bg-light">
              {/* <a className="navbar-brand" href="#">Navbar</a> */}
              {/* <a className="navbar-brand" href="/register/">Register</a> */}
              <div>
                <a className="navbar-brand" href="#">Navbar</a>
                <a className="navbar-brand" href="/register/">Register</a>
                <a className="navbar-brand" href="/login/">Login</a>
              </div>
              <LoginUser />
            </nav>
        );
    }

}
