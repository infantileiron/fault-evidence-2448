import {request} from './client';export const list=()=>request('/reviews');export const create=(body:unknown)=>request('/reviews','POST',body);
