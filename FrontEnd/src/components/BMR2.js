import  React from 'react';
import {Component} from 'react';

export default class BMR extends Component{
      constructor(props) {
          super(props);
          this.state = {bmr: ''};

          this.handleGenderChange = this.handleGenderChange.bind(this);
          this.handleAgeChanged = this.handleAgeChanged.bind(this);
          this.handleHeightChanged = this.handleHeightChanged.bind(this);
          this.handleWeightChanged= this.handleWeightChanged.bind(this);
      }
    handleGenderChange = (event) => {
        this.setState({Gender: event.target.value});
    }

    handleAgeChanged = (event) => {
        this.setState({Age: event.target.value});
    }

    handleHeightChanged = (event) => {
        this.setState({Height: event.target.value});
    }

    handleWeightChanged = (event) => {
        this.setState({Weight: event.target.value});
    }

    onClick = (event) => {
      event.preventDefault();

      let BMR;
      let aktywne;
      let nieaktywne;

      if (this.state.Gender === 'Male') {
        BMR = (9.99 * Number(this.state.Weight)) + (6.25 * this.state.Height) - (4.92 * Number(this.state.Age)) + 5;
        this.setState({ bmr: BMR });
      } else if (this.state.Gender === 'Female') {
        BMR = (9.99 * Number(this.state.Weight)) + (6.25 * this.state.Height) - (4.92 * Number(this.state.Age)) - 161;
        this.setState({bmr: BMR});
      }
      this.setState({aktywne: BMR * 1.5});
      this.setState({nieaktywne: BMR * 0.85});
  }
    render(){
      return(
        <div id="BMR" className="col-lg-4 col-md-4 col-xs-12 className="kalkulator>
              <h4>Twój kalkulator BMR metoda Mifflin-St Jeor</h4>
                    <form>
                    <div className="form-group">
                      <select className="form-control" value={this.state.Gender} onChange={this.handleGenderChange}>
                        <option disabled selected value> -- Płeć-- </option>
                        <option value="Male">Mężczyzna</option>
                        <option value="Female">Kobieta</option>
                      </select>
                    </div>
                    <div className="form-group">
                           <label htmlFor="Age">Wiek</label>
                               <input className="form-control"
                               onChange={this.handleAgeChanged}
                               type="input"
                               id="Age"
                               name="Age"
                               placeholder="Podaj swój wiek"
                               value={this.state.Age}
                               />
                    </div>
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
                    <button className="btn btn-md btn-success btn-bm" onClick={this.onClick.bind(this)}>Sprawdż swoje BMR</button> <br />
                    <div className="form-group">
                            <label>Twoje BMR:</label>
                                <input className="form-control"
                                id="BMR"
                                name="BMR"
                                value= {this.state.bmr}
                                />
                    </div>
                    <div className="form-group">
                            <label>BMR dla osoby aktywnej:</label>
                                <input className="form-control"
                                id="BMR"
                                name="BMR"
                                value= {this.state.aktywne}
                                />
                    </div>
                    <div className="form-group">
                            <label>BMR dla osoby nie aktywnej:</label>
                                <input className="form-control"
                                id="BMR"
                                name="BMR"
                                value= {this.state.nieaktywne}
                                />
                    </div>
                </form>
            </div>
        );
    }
  }
