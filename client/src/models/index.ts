import { browser } from '$app/environment';
import axios from 'axios';
import Cookies from 'js-cookie';


if (browser)
  var token = localStorage.getItem('token');
const ApiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': `Bearer ${Cookies.get('token')}`
  },
});



export {ApiClient};