import  React from 'react';
import {Component} from 'react';

export default class MainBody extends Component{
    render(){
        return(
            <div className="col-lg-10 col-md-10 col-xs-12 offset-lg-1 offset-md-1">
                <div id="start-with-us">
                    <a title="Poznaj kilka łatwych i przyjemnych kroków do bycia FIT!"><h1>START WITH US</h1></a>
                </div>
                <div id="favorite-food">
                    <a title="Ułożymy dla Ciebie indywidualna, dobrze wyliczoną dzietę!"><h1>EAT DELICIOUS AND HEALTHY FOOD</h1></a>
                </div>
                <div id="calorie-burner">
                    <a title="Przygotujemy dla Ciebie odpowiedni i efektywny trening!"><h1>STAY FIT</h1></a>
                </div>
            </div>
        );
    }
}
