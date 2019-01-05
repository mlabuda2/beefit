import  React from 'react';
import {Component} from 'react';

export default class MainBody extends Component{
    render(){
        return(
            <div className="col-lg-10 col-md-10 col-xs-12 offset-lg-1 offset-md-1">
                <div id="start-with-us">
                    <h1>START WITH US</h1>
                </div>
                <div id="favorite-food">
                    <h1>EAT DELICIOUS AND HEALTHY FOOD</h1>
                </div>
                <div id="calorie-burner">
                    <h1>STAY FIT</h1>
                </div>
            </div>
        );
    }
}
