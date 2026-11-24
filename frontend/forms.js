import {notice} from './base.js'

export function wire(form, save, after, onError) {
  if (!form) return
  form.onsubmit = async event => {
    event.preventDefault()
    const button = event.currentTarget.querySelector('button')
    const status = form.querySelector('[role=status]')
    button.disabled = true
    try {
      const result = await save(Object.fromEntries(new FormData(form)))
      notice(status, result?.message || '已保存')
      if (after) await after(result)
    } catch (error) {
      notice(status, error.message, true)
      if (onError) await onError(error)
    } finally {
      button.disabled = false
    }
  }
}
export const canEdit = session => ['operator','reviewer'].includes(session.role)
