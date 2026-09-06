document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('[data-theme-toggle]')
  if (!toggles.length) return

  const storageKey = 'vcn-theme'
  const root = document.documentElement
  const media = window.matchMedia('(prefers-color-scheme: dark)')

  const setTheme = theme => {
    root.setAttribute('data-theme', theme)
    toggles.forEach(toggle => {
      toggle.setAttribute('aria-pressed', String(theme === 'dark'))
      toggle.setAttribute('aria-label', theme === 'dark' ? 'Activer le thème clair' : 'Activer le thème sombre')
    })
  }

  setTheme(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light')

  toggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
      setTheme(next)
      try {
        localStorage.setItem(storageKey, next)
      } catch {
        // Storage can be unavailable (private browsing, disabled cookies): the choice just won't persist.
      }
    })
  })

  // Follow the OS preference live, but only until the visitor picks a theme explicitly themselves.
  media.addEventListener('change', event => {
    let hasStoredChoice = true
    try {
      hasStoredChoice = localStorage.getItem(storageKey) !== null
    } catch {
      hasStoredChoice = false
    }
    if (!hasStoredChoice) setTheme(event.matches ? 'dark' : 'light')
  })
})
