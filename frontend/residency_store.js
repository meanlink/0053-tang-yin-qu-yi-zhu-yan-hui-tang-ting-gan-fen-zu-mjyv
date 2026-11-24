import {api} from './base.js'
export const shows=()=>api('/api/residencies')
export function assign({code,group,...data}){
 const [run,key]=group.split('|')
 return api('/api/residencies/'+encodeURIComponent(code),'POST',{...data,run:Number(run),group:key})
}
