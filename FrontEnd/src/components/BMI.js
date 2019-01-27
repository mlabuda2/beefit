import  React from 'react';
import {Component} from 'react';

export default class BMI extends Component{
      constructor(props) {
          super(props);
          this.state = {bmi: '',
                        showBMI:false};

          this.handleHeightChanged = this.handleHeightChanged.bind(this);
          this.handleWeightChanged= this.handleWeightChanged.bind(this);
      }

    handleHeightChanged = (event) => {
        this.setState({Height: event.target.value});
    }

    handleWeightChanged = (event) => {
        this.setState({Weight: event.target.value});
    }

    onClick = (event) => {
      event.preventDefault();

      let BMI;
      let text;

      BMI = ((this.state.Weight)/((this.state.Height)*(this.state.Height)))*10000;
      this.setState({bmi: BMI});
      if (BMI < 18.5){
        text = "Niedowaga !";
        this.setState({text: text});
      }
      else if (BMI >= 18.5 && BMI <= 24.9){
        text = "Waga prawidłowa :)";
        this.setState({text: text});
      }
      else if (BMI > 24.9 && BMI <= 29.9){
        text = "Nadwaga";
        this.setState({text: text});
      }
      else if (BMI > 29.9){
        text = "Otyłość !";
        this.setState({text: text});
      }
  }
  showBMI(){
    this.setState({
      showBMI:!this.state.showBMI
    })
  }
    render(){
      return(
        <div id="BMI" className="col-lg-4 col-md-4 col-xs-12">
        <button className="btn btn-lg btn-defoult btn-block" onClick={()=>this.showBMI()}>Kliknij aby obliczyć BMI</button>
        {
          this.state.showBMI?
          <div className="kalkulator">
              <h4>Twój kalkulator BMI</h4>
                    <form>
                    <div className="form-group">
                            <label>Wzrost (w cm):</label>
                            <input className="form-control"
                            onChange={this.handleHeightChanged}
                            type="input"
                            id="Height"
                            name="Height"
                            placeholder="Podaj swój wzrost"
                            value={this.state.Height}
                            />
                    </div>
                    <div className="form-group">
                            <label htmlFor="Weight">Waga (w kg):</label>
                                <input className="form-control"
                                onChange={this.handleWeightChanged}
                                type="input"
                                id="Weight"
                                name="Weight"
                                placeholder="Podaj swoją wage"
                                value={this.state.Weight}
                                />
                    </div>
                    <button className="btn btn-lg btn-primary btn-block" onClick={this.onClick.bind(this)}>Sprawdż swoje BMI</button> <br />
                    <div className="form-group">
                            <label>Twoje BMI:</label>
                                <input className="form-control"
                                id="BMI"
                                name="BMI"
                                value= {this.state.bmi}
                                />
                                <input className="form-control"
                                id="BMI"
                                name="BMI"
                                value= {this.state.text}
                                />
                    </div>
                </form>
              </div>
            :null
            }
            </div>
        );
    }
  }
