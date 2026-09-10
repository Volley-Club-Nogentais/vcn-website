document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.sponsors-marquee').forEach(marquee => {
    const track = marquee.querySelector('.sponsors-marquee-track')
    const firstGroup = track && track.querySelector(':scope > :not([aria-hidden])')

    if (!track || !firstGroup) {
      return
    }

    const update = () => {
      marquee.classList.toggle('is-scrolling', firstGroup.offsetWidth > marquee.clientWidth)
    }

    update()
    window.addEventListener('resize', update)
  })
})
