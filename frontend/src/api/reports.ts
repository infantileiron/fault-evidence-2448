import {request} from './client';export const list=()=>request('/reports');export const create=(body:unknown)=>request('/reports','POST',body);
