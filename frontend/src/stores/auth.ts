import {reactive} from 'vue';import {request} from '../api/client';import type {User} from '../types/domain';
export const auth=reactive({user:JSON.parse(localStorage.getItem('evidence-user')||'null') as User|null,error:''});
export async function login(email:string,password:string){const r=await request('/auth/login','POST',{email,password});localStorage.setItem('evidence-token',r.token);localStorage.setItem('evidence-user',JSON.stringify(r.user));auth.user=r.user}
export function logout(){localStorage.removeItem('evidence-token');localStorage.removeItem('evidence-user');auth.user=null;location.hash='#/login'}
export const canWrite=()=>auth.user?.role!=='viewer';export const isAdmin=()=>auth.user?.role==='admin';
