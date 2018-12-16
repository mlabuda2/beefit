import axios from "axios";

export const LOGIN_USER = "login_user";

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
          username: 'mati',
          password: 'mati'
        }
    })
    .then(() => callback());

  return {
    type: LOGIN_USER,
    payload: request
  };
}
