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
document.addEventListener("DOMContentLoaded", function () {
  const loginButton = document.querySelector(".btn-login");

  loginButton.addEventListener("click", async function (event) {
      event.preventDefault();

      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();

      if (!username || !password) {
          alert("Por favor, preencha usuário e senha.");
          return;
      }

      try {
          const response = await fetch("http://127.0.0.1:5000/auth/login", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify({
                  username: username,
                  password: password
              }),
          });

          if (!response.ok) {
              throw new Error("Erro no login: " + response.statusText);
          }

          const result = await response.json();

          if (result.access_token) {
              // Armazenar o token no localStorage
              localStorage.setItem("token", result.access_token);

              alert("Login realizado com sucesso!");

              // Redirecionar para o dashboard
              window.location.href = "/frontend/dashboard/dashboard.html";
          } else {
              alert("Login falhou. Verifique suas credenciais.");
          }
      } catch (error) {
          console.error("Erro:", error);
          alert("Ocorreu um erro ao fazer login.");
      }
  });
});
