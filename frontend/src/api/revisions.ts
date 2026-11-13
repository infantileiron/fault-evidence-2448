import {request} from './client';export const list=()=>request('/revisions');export const create=(body:unknown)=>request('/revisions','POST',body);
