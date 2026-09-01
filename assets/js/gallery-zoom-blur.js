document.addEventListener('DOMContentLoaded', function () {
    // Blur-up
    document.querySelectorAll('.blur-up').forEach(img => {
        if (img.complete) {
            img.classList.add('loaded')
        } else {
            img.addEventListener('load', () => {
                img.classList.add('loaded')
            })
        }
    })

    // Zoom fullscreen with prev/next navigation
    const galleryImages = Array.from(document.querySelectorAll('[data-full]'))
    if (galleryImages.length === 0) return

    let currentIndex = 0
    let overlay = null
    let fullImg = null

    function showImage(index) {
        currentIndex = (index + galleryImages.length) % galleryImages.length
        fullImg.src = galleryImages[currentIndex].dataset.full
    }

    function closeOverlay() {
        if (!overlay) return
        document.removeEventListener('keydown', onKeydown)
        overlay.remove()
        overlay = null
        fullImg = null
    }

    function onKeydown(e) {
        if (e.key === 'Escape') closeOverlay()
        if (e.key === 'ArrowLeft') showImage(currentIndex - 1)
        if (e.key === 'ArrowRight') showImage(currentIndex + 1)
    }

    function openOverlay(index) {
        overlay = document.createElement('div')
        overlay.className = 'gallery-lightbox'
        overlay.addEventListener('click', closeOverlay)

        fullImg = document.createElement('img')
        fullImg.className = 'gallery-lightbox-img'
        fullImg.addEventListener('click', e => e.stopPropagation())
        overlay.appendChild(fullImg)

        const closeBtn = document.createElement('button')
        closeBtn.className = 'gallery-lightbox-close'
        closeBtn.type = 'button'
        closeBtn.setAttribute('aria-label', 'Fermer')
        closeBtn.textContent = '\u00D7'
        closeBtn.addEventListener('click', e => {
            e.stopPropagation()
            closeOverlay()
        })
        overlay.appendChild(closeBtn)

        if (galleryImages.length > 1) {
            const prevBtn = document.createElement('button')
            prevBtn.className = 'gallery-lightbox-prev'
            prevBtn.type = 'button'
            prevBtn.setAttribute('aria-label', 'Photo précédente')
            prevBtn.textContent = '\u2039'
            prevBtn.addEventListener('click', e => {
                e.stopPropagation()
                showImage(currentIndex - 1)
            })
            overlay.appendChild(prevBtn)

            const nextBtn = document.createElement('button')
            nextBtn.className = 'gallery-lightbox-next'
            nextBtn.type = 'button'
            nextBtn.setAttribute('aria-label', 'Photo suivante')
            nextBtn.textContent = '\u203A'
            nextBtn.addEventListener('click', e => {
                e.stopPropagation()
                showImage(currentIndex + 1)
            })
            overlay.appendChild(nextBtn)
        }

        document.body.appendChild(overlay)
        document.addEventListener('keydown', onKeydown)
        showImage(index)
    }

    galleryImages.forEach((img, index) => {
        img.addEventListener('click', () => openOverlay(index))
    })
})
