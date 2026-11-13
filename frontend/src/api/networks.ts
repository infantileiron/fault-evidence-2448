import {request} from './client';export const list=()=>request('/networks');export const create=(body:unknown)=>request('/networks','POST',body);
