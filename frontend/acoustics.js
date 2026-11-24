import {h,empty} from './base.js'
import {heading,choices,feedback,table} from './view.js'
import {wire,canEdit} from './forms.js'
import {groups,fit} from './acoustics_store.js'
import {seats} from './seats_store.js'
import {badges} from './seat_tags.js'
export async function render(root,session){
 const [rows,places]=await Promise.all([groups(),seats()])
 root.innerHTML=heading('座席分组','同一分组内任何两张座位的距离均需达标。最远座席距离决定能否合并。')+`
 <div class="acoustics-board"><aside class="panel"><h2>聚类口径</h2><p>同一区域按物理座席连续约束合并。听感最差距离按清晰度、回声和声级三者取最大。</p>
 ${canEdit(session)?`<form class="compact-form"><label>会堂<select name="hall">${choices([...new Set(places.map(r=>r.hall))],s=>s,s=>s)}</select></label><label>最远距离阈值<input name="threshold" type="number" value=".6" min=".01" max="10" step=".01" required></label><button>计算听感分组</button>${feedback}</form>`:''}</aside>
 <section>${rows.map(r=>`<article class="acoustic-band">${badges(r.members)}<div><strong>${h(r.hall)}</strong><p>最远距离 ${r.max_distance.toFixed(3)} · 中位回声 ${r.medians.echo} ms</p></div><strong>${r.recommended_panels} 块吸声板</strong></article>`).join('')||empty('需至少两座席有完备说、唱双段才可聚类。')}</section></div>`
 wire(root.querySelector('form'),fit,()=>render(root,session))
}
