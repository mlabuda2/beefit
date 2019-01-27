import axios from "axios";

export const LOGIN_USER = "login_user";
export const REGISTER_USER = "register_user";
export const FETCH_DIET_PLANS = "fetch_diet_plans";
export const CREATE_DIET_PLANS = "create_diet_plans";
export const DELETE_DIET_PLAN = "delete_diet_plan";
export const SELECTED_DIET_PLAN = "selected_diet_plan";

const ROOT_URL = "http://127.0.0.1:5000";

export function loginUser(values, callback) {
  const request = axios
    // .get("https://reqres.in/api/users?page=1")  // sample json api call
    // .get(`${ROOT_URL}/login`, values)
    // .get(`${ROOT_URL}/login`,  {headers: {Authorization : "mati:mati"}})
    // .get(`${ROOT_URL}/login`,  {headers: "mati:mati"})
    .get(`${ROOT_URL}/login`, {
        method: 'GET',
        mode: 'cors',
        headers: { 'Access-Control-Allow-Origin': true },
        auth: {
          username: values.username,
          password: values.password
        }
    })
    .then((response) => callback(response));

  return {
    type: LOGIN_USER,
    payload: request
  };
}

export function registerUser(values, callback) {
  const request = axios
  .post(`${ROOT_URL}/register`, values)
  .then(() => callback());

  return {
    type: REGISTER_USER,
    payload: request
  };
}

export function createDietPlans(values, callback) {
  let token = localStorage.getItem('t8k3n');
  // const request = axios
  //   .post(`${ROOT_URL}/assign_plan`,  values)
  //   .then(() => callback());
  sleep(1000);
  callback();

  return {
    type: CREATE_DIET_PLANS,
    payload: request
  };
}

export function fetchDietPlans() {
  let token = localStorage.getItem('t8k3n');
  const request = axios
    .get(`${ROOT_URL}/user_plans`, {
      headers: { 'x-access-token': token },
    });

  return {
    type: FETCH_DIET_PLANS,
    payload: request
  };
}

export function deleteDietPlan(id, callback) {
  let token = localStorage.getItem('t8k3n');
  const request = axios
    .post(`${ROOT_URL}/detach_plan`, { 'diet_plan_id': id }, {
      headers: { 'x-access-token': token },
    })
    .then(() => callback());

  return {
    type: DELETE_DIET_PLAN,
    payload: id
  };
}

// export function isAuthenticated(success_callback, error_callback) {
//   let token = localStorage.getItem('t8k3n');
//   if (!token) {
//     token = "token does not exist";
//   }
//   const request = axios
//     .get(`${ROOT_URL}/is_auth`, {
//         method: 'GET',
//         mode: 'cors',
//         headers: { 'x-access-token': token },
//     })
//     .then((response) => success_callback(response))
//     // .then((response) => console.log(response.data['message']))
//     .catch((error) => error_callback(error));
//     // .catch((error) => console.log(error.response.data['message']));
//   return {
//     type: LOGIN_USER,
//     payload: request
//   };
// }
