import {mount} from './base.js'
import {render as seats} from './seats.js'
import {render as listening} from './listening.js'
import {render as acoustics} from './acoustics.js'
import {render as residencies} from './residencies.js'

const pages = {
  seats: '座席定位',
  listening: '双段试听',
  acoustics: '座席分组',
  residencies: '驻演布置'
}
const renderers = {seats, listening, acoustics, residencies}
mount({title: '堂音 · 曲艺驻演会堂听感分组', kicker: '南棚曲艺馆 · 堂音座席图', pages, render: (key, root, session) => renderers[key](root, session)})
