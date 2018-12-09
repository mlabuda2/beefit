import  React from 'react';
import {Component} from 'react';

export default class BMR extends Component{
    render(){
      return(
        <div id="BMR">
              <h4>Twój kalkulator BMR</h4>
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
                            <label>Wzrost:</label>
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
                            <label htmlFor="Weight">Waga:</label>
                                <input className="form-control"
                                onChange={this.handleWeightChanged}
                                type="input"
                                id="Weight"
                                name="Weight"
                                placeholder="Podaj swoją wage"
                                value={this.state.Weight}
                                />
                    </div>
                    <div className="form-group">
                            <label>Twoje BMR:</label>
                                <input className="form-control"
                                id="BMR"
                                name="BMR"
                                value= {this.state.bmr}
                                />
                    </div>
                    <button className="btn btn-lg btn-primary btn-block" onClick={this.onClick.bind(this)}>Sprawdż swoje BMR</button> <br />
                </form>
            </div>
        );
    }
  }
