import {request} from './client';export const list=()=>request('/cases');export const create=(body:unknown)=>request('/cases','POST',body);
