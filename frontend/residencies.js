import {h,badge} from './base.js'
import {heading,choices,feedback,table} from './view.js'
import {wire} from './forms.js'
import {groups} from './acoustics_store.js'
import {badges} from './seat_tags.js'
import {shows,assign} from './residency_store.js'
export async function render(root,session,flash={}){
 const [board,listening]=await Promise.all([shows(),groups()])
 const candidates=listening.filter(g=>g.current)
 const stale=listening.some(g=>g.expired) && candidates.length===0
 root.innerHTML=heading('驻演布置','先对齐会堂，再查座位数、吸声板容量与通道禁布条件。签核只用当前试听算出的整套分组。')+`
 <div class="residency-ledger"><aside class="panel"><h2>可用布置</h2>${table(['会堂','方案','最大板数'],board.layouts.map(p=>[p.hall,p.title,p.panel_capacity]))}
 ${stale?`<p class="muted" role="note">试听已补录，过期分组不可签核；重算完成后请重新选择并确认新分组。</p>`:''}</aside>
 <section>${flash.text?`<p class="notice-bar" role="${flash.failure?'alert':'status'}">${h(flash.text)}</p>`:''}${board.slots.map(r=>`<article class="panel"><h2>${h(r.hall)} · ${h(r.event_on)}</h2><p>${h(r.code)} · ${h(r.producer)}</p>
 ${r.members?`${badge('已锁档','approved')}${badges(r.members)}<p>${r.panels} 块板 · ${h(r.rationale)}</p>`:session.role==='reviewer'?`<form class="compact-form"><input name="code" type="hidden" value="${h(r.code)}">
 <label>座席组<select name="group" required><option value="">选择当前座席组</option>${choices(candidates.filter(x=>x.hall===r.hall),x=>x.members.join(' / '),x=>x.run_id+'|'+x.key)}</select></label>
 <label>布置<select name="layout">${choices(board.layouts.filter(x=>x.hall===r.hall),x=>x.title)}</select></label>
 <label>说明<input name="rationale" required minlength="4"></label><button${candidates.some(x=>x.hall===r.hall)?'':' disabled'}>驻演签布置</button>${feedback}</form>${candidates.some(x=>x.hall===r.hall)?'':'<p class="muted">该会堂没有可签核的当前分组，请先在座席分组重算。</p>'}`:badge('待签')}</article>`).join('')}</section></div>`
 for(const form of root.querySelectorAll('form'))wire(form,assign,()=>render(root,session,{text:'已按当前分组签核布置'}),
   error=>render(root,session,{text:error.message,failure:true}))
}
