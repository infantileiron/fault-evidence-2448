import {request} from './client';export const list=()=>request('/runs');export const create=(body:unknown)=>request('/runs','POST',body);
