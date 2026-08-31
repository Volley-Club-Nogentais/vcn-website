document.addEventListener('DOMContentLoaded', () => {
  const fab = document.querySelector('[data-social-fab]')
  if (!fab) return

  const toggle = fab.querySelector('[data-social-fab-toggle]')
  const list = fab.querySelector('[data-social-fab-list]')

  const close = () => {
    list.hidden = true
    toggle.setAttribute('aria-expanded', 'false')
  }

  toggle.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true'
    list.hidden = isOpen
    toggle.setAttribute('aria-expanded', String(!isOpen))
  })

  document.addEventListener('click', event => {
    if (!fab.contains(event.target)) close()
  })

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') close()
  })
})
