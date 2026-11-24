import {h} from './base.js'
export function badges(seats){return `<ul class="seats-mini">${seats.map(s=>`<li>${h(s)}</li>`).join('')}</ul>`}
