document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-email]').forEach(el => {
    const address = atob(el.dataset.email)
    const link = document.createElement('a')
    link.href = `mailto:${address}`
    link.textContent = address
    el.replaceWith(link)
  })
})
