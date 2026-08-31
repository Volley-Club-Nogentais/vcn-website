document.addEventListener('DOMContentLoaded', function () {
  const toggler = document.querySelector('[data-navbar-toggle]')
  const menu = toggler && document.getElementById(toggler.getAttribute('aria-controls'))

  if (!toggler || !menu) {
    return
  }

  toggler.addEventListener('click', function () {
    const expanded = toggler.getAttribute('aria-expanded') === 'true'
    toggler.setAttribute('aria-expanded', String(!expanded))
    menu.classList.toggle('hidden')
  })
})
