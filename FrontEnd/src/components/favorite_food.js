import  React from 'react';
import {Component} from 'react';

export default class FavoriteFood extends Component{
    render(){
        return(
            <div id="favorite-food" className="col-md-10 col-xs-12">
                <a>
                    <img src="src/img/losos.jpg"/>
                </a>
                <div className="content-list">
                    <h4>Twoje ulubione jedzenie</h4>
                    <ul>
                        <li>2 filety z łososia ze skórą (każdy po ok 300g)</li>
                        <li>450g liści szpinaku mrożonego</li>
                        <li>150g sera sałatkowo-kanapkowego</li>
                        <li>2 ząbki czosnku</li>
                        <li>pieprz cytrynowy</li>
                        <li>sól</li>
                        <li>sok z cytryny</li>
                        <li>suszone pomidory</li>
                    </ul>
                </div>
            </div>
        );
    }
}
