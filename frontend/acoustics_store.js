import {api,waitJob} from './base.js'
export const groups=()=>api('/api/acoustics')
export async function fit(data){
 const {job_id}=await api('/api/acoustics','POST',{...data,threshold:Number(data.threshold)})
 return waitJob(job_id)
}
