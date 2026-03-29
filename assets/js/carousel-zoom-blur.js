document.addEventListener("DOMContentLoaded", function () {

  // Blur-up
  document.querySelectorAll(".blur-up").forEach(img => {
    img.addEventListener("load", () => {
      img.classList.add("loaded");
    });
  });

  // Zoom fullscreen
  document.querySelectorAll(".carousel-img-wrapper img").forEach(img => {
    img.addEventListener("click", () => {
      const src = img.dataset.full;

      const overlay = document.createElement("div");
      overlay.style.position = "fixed";
      overlay.style.top = 0;
      overlay.style.left = 0;
      overlay.style.width = "100%";
      overlay.style.height = "100%";
      overlay.style.background = "rgba(0,0,0,0.9)";
      overlay.style.display = "flex";
      overlay.style.alignItems = "center";
      overlay.style.justifyContent = "center";
      overlay.style.zIndex = 9999;

      const fullImg = document.createElement("img");
      fullImg.src = src;
      fullImg.style.maxWidth = "95%";
      fullImg.style.maxHeight = "95%";

      overlay.appendChild(fullImg);

      overlay.addEventListener("click", () => {
        overlay.remove();
      });

      document.body.appendChild(overlay);
    });
  });

});
