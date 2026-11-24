import {api} from './base.js'
import {keys} from './hall_labels.js'
export const listen=()=>api('/api/listening')
export function record(row){
 return api('/api/listening','POST',{...row,...Object.fromEntries(Object.keys(keys).map(k=>[k,Number(row[k])]))})
}
