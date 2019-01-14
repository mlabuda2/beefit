import _ from "lodash";
import React, { Component } from "react";

class DayList extends Component {
  renderDayList() {
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
    // console.log("dayMeals.keys: " + Object.keys(dayMeals));
    // console.log(dayMeals.id_plan)
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
    dayMeals.map(dayPlan => {
      // console.log('@@@');
      // console.log(day);
      // console.log('@@@');
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

  render() {
    console.log('ee')
    return (
      <div>
        daymeals:
        {this.renderNewDayList()}
      </div>
    );
  }
}

export default DayList;
