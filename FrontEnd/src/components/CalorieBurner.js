import  React from 'react';
import {Component} from 'react';

export default class CalorieBurner extends Component{
    render(){
        return(
            <div id="calorie-burner" className="col-md-10 col-xs-12">
                <a>
                    <img className="run" src="src/img/run.jpg"/>
                </a>
                <div className="content-list">
                    <h4>Twój trening</h4>
                    <ul>
                        <li>rozgrzewka</li>
                        <li>10 pompek</li>
                        <li>20 przysiadów</li>
                        <li>20 brzuszków</li>
                        <li>minuta planka</li>
                        <li>10 martwych ciągów</li>
                        <li>10 barpies</li>
                        <li>5 military push</li>
                    </ul>
                </div>
            </div>
        );
    }
}
