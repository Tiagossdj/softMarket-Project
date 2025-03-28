const filterButtons = document.querySelectorAll('.filter-btn');

filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

// nome no inicio

// tirar informação do token
// Função para decodificar o token JWT e extrair as claims
function decodeJWT(token) {
    const payloadBase64 = token.split('.')[1];  // O payload está na segunda parte do token
    const decodedPayload = atob(payloadBase64);  // Decodifica a parte base64
    return JSON.parse(decodedPayload);  // Converte o JSON do payload em um objeto
}

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");

    if (token) {
        const decoded = decodeJWT(token);
        const username = decoded.username;  // O nome do usuário está no campo 'username'

        // Verifica se o elemento existe antes de tentar acessar
        const welcomeMessageElement = document.getElementById("welcome-message");
        if (welcomeMessageElement) {
            welcomeMessageElement.innerText = `Bem-vindo de volta, ${username} !`;
        }

        // Exibe as iniciais do usuário no ícone (exemplo: "João" → "JO")
        const initials = username.slice(0, 2).toUpperCase();
        const userIconElement = document.getElementById("user-icon");
        if (userIconElement) {
            userIconElement.innerText = initials;
        }
    } else {
        console.log("Token não encontrado.");
    }
});
