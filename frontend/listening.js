import {h} from './base.js'
import {heading,choices,feedback,table} from './view.js'
import {wire,canEdit} from './forms.js'
import {passages,keys} from './hall_labels.js'
import {seats} from './seats_store.js'
import {listen,record} from './listening_store.js'
export async function render(root,session){
 const [rows,places]=await Promise.all([listen(),seats()])
 root.innerHTML=heading('双段试听','说段和唱段分开听检。归档素材编号，记录同座的声级、清晰度和回声。')+`
 <div class="listening-ledger"><section>${Array.from(Map.groupBy(rows,r=>r.passage),([passage,samples])=>`<details open><summary>${h(passages[passage])}</summary>${table(['座位',...Object.values(keys),'素材'],samples.map(x=>[x.seat,...Object.keys(keys).map(k=>x[k]),x.media_ref]))}</details>`).join('')}</section>
 ${canEdit(session)?`<form class="panel compact-form"><h2>记录试听凭证</h2><label>会堂座席<select name="seat">${choices(places,r=>r.code+' · '+r.hall)}</select></label><label>曲艺片段<select name="passage">${Object.entries(passages).map(([k,v])=>`<option value="${k}">${h(v)}</option>`).join('')}</select></label>
 ${Object.entries(keys).map(([k,v])=>`<label>${h(v)}<input type="number" name="${k}" required min="0"></label>`).join('')}<label>素材引用<input name="media_ref" required minlength="5"></label><button>保存听检</button>${feedback}</form>`:''}</div>`
 wire(root.querySelector('form'),record,()=>render(root,session))
}
