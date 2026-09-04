// Inlined into <head> (see layouts/_default/baseof.html) and run synchronously before first paint,
// so the correct theme applies immediately instead of flashing light before an external script loads.
const vcnStoredTheme = (() => {
  try {
    return localStorage.getItem('vcn-theme')
  } catch {
    // Storage can be unavailable (private browsing, disabled cookies): fall back to the OS preference.
    return null
  }
})()

const vcnPrefersDarkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
const vcnTheme = vcnStoredTheme === 'light' || vcnStoredTheme === 'dark' ? vcnStoredTheme : vcnPrefersDarkTheme ? 'dark' : 'light'

document.documentElement.setAttribute('data-theme', vcnTheme)
