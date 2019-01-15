import _ from "lodash";
import React, { Component } from "react";

class DayList extends Component {
  renderXYZ() {
    const dayMeals = {
      "id_plan": 0,
      "name": "PLAN DZIKA",
      "plan_details": [

        {
          "day": "Monday",
          "meals": [
            {
              "time": "8:30",
              "products": [
                {
                  "name": "jajko",
                  "weight": "400"
                }
              ]
            }
          ]
        },

        {
          "day": "Tuesday",
          "meals": [
            {
              "time": "9:30",
              "products": [
                {
                  "name": "chleb",
                  "weight": "400"
                }
              ]
            }
          ]
        },

      ]
    }
    return dayMeals.plan_details.map(day_details => {
      return (
        <li key={day_details.day} className="list-group-item">
          { day_details.day }
        </li>
      );
    });
  }

  renderNewDayList() {
    const daysOfWeek = {
      "0": "Monday",
      "1": "Tuesday",
      "2": "Wednesday",
      "3": "Thursday",
      "4": "Friday",
      "5": "Saturday",
      "6": "Sunday"
    }
    const { dayMeals } = this.props;
    console.log("dayMeals.length: " + dayMeals.length)
    dayMeals.map(dayPlan => {
      for (const [day, dietPlan] of Object.entries(dayPlan)) {
        console.log(`Dzień Tygodnia: ${daysOfWeek[day]} ${dietPlan}`);
        for (const [mealTime, meal] of Object.entries(dietPlan)) {
          console.log(`Godzina: ${mealTime}`)
          meal.map(product => {
            console.log(product.name)
          });
        }
      }
    });
  }

  renderDayList() {
    const daysOfWeek = {
      "0": "Monday",
      "1": "Tuesday",
      "2": "Wednesday",
      "3": "Thursday",
      "4": "Friday",
      "5": "Saturday",
      "6": "Sunday"
    }
    const { dayMeals } = this.props;

    return dayMeals.map(dayPlan => {
      return _.map(dayPlan, (dietPlan, day) => {
        // console.log(`Dzień Tygodnia: ${daysOfWeek[day]} ${dietPlan}`);
        return (
          <div>
            <li className="list-group-item">{daysOfWeek[day]}</li>
            {
              _.map(dietPlan, (meal, mealTime) => {
                return (
                  <ul key={mealTime}>
                    <li className="list-group-item">{mealTime}</li>
                    <ul>
                    {
                      meal.map(product => {
                        return <li className="list-group-item" key={product.name}>{product.name}: {product.weight}</li>
                      })  // END .map
                    }
                    </ul>
                  </ul>
                )
              })  // END _.map
            }
          </div>
        )
      })  // END _.map
    });
  }

  render() {
    return (
      <ul className="list-group col-sm-4">
        {this.renderDayList()}
      </ul>
    );
  }
}

export default DayList;
