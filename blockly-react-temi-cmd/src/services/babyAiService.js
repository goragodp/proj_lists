import axios from "axios";

const BASE_URL = `http://babyai.org:5000/`;
const HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Content-Type": "text/plain",
  "Accept" : "*/*",
};

export const babyAiService = async (data) => {
  const response = await axios.post(BASE_URL + 'execute', data, {
    headers: HEADERS,
    withCredentials: true,
    credentials: "same-origin",
  });
  return response;
};

export const babyAiServiceTemi = async (data) => {
  const response = await axios.post(BASE_URL + 'temi-cmd', data, {
    headers: HEADERS,
    withCredentials: true,
    credentials: "same-origin",
  });
  return response;
};

export const exportWorkspace = async(data) => {
  const response = await axios.post(BASE_URL + 'workspace/export', data, {
    headers: HEADERS,
    withCredentials: true,
    credentials: "same-origin",
  });
  return response;
}

export const downloadSavedWorkspace = async(filename) => {
  const response = await axios.get(BASE_URL+ 'workspace/export/download/' + filename.replace(/'/g, ''), {
    headers:HEADERS,
    withCredentials: true,
    credentials: "same-origin",
  });
  return response;
}