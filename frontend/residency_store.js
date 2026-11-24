import {api} from './base.js'
export const shows=()=>api('/api/residencies')
export const assign=({code,...data})=>api('/api/residencies/'+encodeURIComponent(code),'POST',data)
