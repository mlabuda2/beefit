import axios from "axios";

export const LOGIN_USER = "login_user";
export const REGISTER_USER = "register_user";
export const FETCH_DIET_PLANS = "fetch_diet_plans";

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

export function fetchDietPlans() {
  const request = axios.get(`${ROOT_URL}/user_plans`);

  return {
    type: FETCH_DIET_PLANS,
    payload: request
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
