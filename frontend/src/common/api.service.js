import { CSRF_TOKEN } from "./csrf_token.js";
import axios from "axios";

const axiosService = (
  endpoint,
  method,
  data,
  params = undefined,
  responseType = "json"
) => {
  const options = {
    method: method || "GET",
    url: endpoint,
    data: data !== undefined ? data : null,
    headers: {
      "X-CSRFToken": CSRF_TOKEN,
    },
    params: params !== undefined ? params : null,
    responseType: responseType,
  };
  return axios(options, params);
};

const catchAxiosError = (error, genericError = "Errore") => {
  if (error.response) {
    // Request made and server responded
    console.log(error.response.data);
    console.log(error.response.status);
    console.log(error.response.headers);
    return error.response.data !== "" ? error.response.data : genericError;
  } else if (error.request) {
    // The request was made but no response was received
    console.log(error.request);
    return error.request || genericError;
  } else {
    // Something happened in setting up the request that triggered an Error
    console.log(genericError, error.message);
    return genericError;
  }
};

export { axiosService, catchAxiosError };
