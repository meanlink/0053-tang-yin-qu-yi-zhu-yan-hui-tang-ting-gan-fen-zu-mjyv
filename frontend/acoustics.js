import {h,empty,badge} from './base.js'
import {heading,choices,feedback} from './view.js'
import {wire,canEdit} from './forms.js'
import {groups,fit} from './acoustics_store.js'
import {seats} from './seats_store.js'
import {badges} from './seat_tags.js'
const stamp=v=>v?new Date(v).toLocaleString('zh-CN',{hour12:false}):''
const band=r=>`<article class="acoustic-band">${badges(r.members)}<div><strong>${h(r.hall)}</strong><p>最远距离 ${r.max_distance.toFixed(3)} · 中位回声 ${r.medians.echo} ms</p></div><strong>${r.recommended_panels} 块吸声板</strong></article>`
export async function render(root,session,flash={}){
 const [rows,places]=await Promise.all([groups(),seats()])
 const halls=[...new Set(places.map(r=>r.hall))]
 const runIds=[...new Set(rows.map(r=>r.run_id))]
 root.innerHTML=heading('座席分组','同一分组内任何两张座位的距离均需达标。最远座席距离决定能否合并。补录试听后旧结果只供查阅，须整堂重算才能签核。')+`
 <div class="acoustics-board"><aside class="panel"><h2>聚类口径</h2><p>同一区域按物理座席连续约束合并。听感最差距离按清晰度、回声和声级三者取最大。过期分组只会出现在查阅区，不参与签核。</p>
 ${canEdit(session)?`<form class="compact-form"><label>会堂<select name="hall">${choices(halls,s=>s,s=>s)}</select></label><label>最远距离阈值<input name="threshold" type="number" value=".6" min=".01" max="10" step=".01" required></label><button>计算听感分组</button>${feedback}</form>`:''}${flash.text?`<p class="notice-bar" role="${flash.failure?'alert':'status'}">${h(flash.text)}</p>`:''}</aside>
 <section>${halls.map(hall=>{
   const mine=rows.filter(r=>r.hall===hall)
   const current=mine.filter(r=>r.current)
   const past=runIds.map(id=>mine.filter(r=>r.run_id===id&&!r.current)).filter(list=>list.length)
   return `<article class="hall-groups"><h2>${h(hall)}${current.length?badge('当前分组','approved'):badge('待重算','held')}</h2>
   ${current.map(band).join('')||empty(mine.length?'试听已补录，现有结果均已过期，请按最新试听重算整套分组。':'需至少两座席有完备说、唱双段才可聚类。')}
   ${past.length?`<details class="expired-groups"><summary>过期结果（${past.length} 组，仅供查阅）</summary>${past.map(list=>`<section><p class="muted">第 ${list[0].run_id} 次 · 阈值 ${list[0].threshold} · 试听版本 ${list[0].run_revision} · ${stamp(list[0].finished_at)}</p>${list.map(band).join('')}</section>`).join('')}</details>`:''}
   </article>`
 }).join('')}</section></div>`
 wire(root.querySelector('form'),fit,result=>render(root,session,{text:result.current?'分组已按最新试听重算，可继续签核。':(result.message||'已重算')}),
   error=>render(root,session,{text:error.message,failure:true}))
}
