import axios from "axios";

export const LOGIN_USER = "login_user";

const ROOT_URL = "http://to.do";

export function loginUser(values, callback) {
  const request = axios
    // .post(`${ROOT_URL}/todo`, values)
    .get("https://reqres.in/api/users?page=1")  // sample json api call
    .then(() => callback());

  return {
    type: LOGIN_USER,
    payload: request
  };
}
