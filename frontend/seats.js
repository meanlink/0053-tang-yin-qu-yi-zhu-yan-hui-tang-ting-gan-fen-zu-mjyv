import {h,badge} from './base.js'
import {heading} from './view.js'
import {sections} from './hall_labels.js'
import {seats} from './seats_store.js'
export async function render(root){
 const rows=await seats()
 root.innerHTML=heading('座席定位','座席按会堂分列。相邻、同区、绑定素材的座席才可能并组。')+`<div class="hall-rooms">${Array.from(Map.groupBy(rows,r=>r.hall),([hall,list])=>`<section><h2>${h(hall)}</h2><p class="proscenium">台口方向</p>${Array.from(Map.groupBy(list,r=>r.section),([zone,places])=>`<div class="seat-line"><strong>${h(sections[zone])}</strong>${places.map(p=>`
 <article><b>${h(p.code)}</b><small>第 ${p.lane} 位 · ${p.clips} 段</small>${badge(p.mat_allowed?'可配板':'通道禁配',p.mat_allowed?'':'held')}</article>`).join('')}</div>`).join('')}</section>`).join('')}</div>`
}
