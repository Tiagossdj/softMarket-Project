window.addEventListener("DOMContentLoaded", () => {
  const tagline = document.getElementById("tagline");
  const text = "Sua solução completa de gestão";
  let index = 0;

  function typeEffect() {
      if (index < text.length) {
          tagline.textContent += text.charAt(index);
          index++;
          setTimeout(typeEffect, 50);
      }
  }

  typeEffect();
});
