document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".login-box"); // Formulário de registro
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm-password");
    const roleOptions = document.querySelectorAll('input[name="role"]');
    const registerButton = document.querySelector(".btn-login");
    
    // Função de validação
    function validateForm() {
        let isValid = true;
        let roleSelected = false;

        // Limpar mensagens anteriores
        const errorMessages = form.querySelectorAll(".error-message");
        errorMessages.forEach(message => message.remove());

        // Validar nome de usuário
        if (username.value.trim() === "") {
            showError(username, "Usuário é obrigatório.");
            isValid = false;
        }

        // Validar senha
        if (password.value.trim() === "") {
            showError(password, "Senha é obrigatória.");
            isValid = false;
        }

        // Validar confirmação de senha
        if (confirmPassword.value.trim() === "") {
            showError(confirmPassword, "Por favor, confirme sua senha.");
            isValid = false;
        } else if (password.value !== confirmPassword.value) {
            showError(confirmPassword, "As senhas não coincidem.");
            isValid = false;
        }

        // Validar role (gerente ou funcionário)
        roleOptions.forEach(option => {
            if (option.checked) {
                roleSelected = true;
            }
        });

        if (!roleSelected) {
            showError(roleOptions[0].parentElement, "Por favor, escolha um papel.");
            isValid = false;
        }

        return isValid;
    }

    // Função para exibir mensagens de erro
    function showError(element, message) {
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("error-message");
        errorMessage.textContent = message;
        element.parentElement.appendChild(errorMessage);
    }

    // Ao clicar no botão de registro
    registerButton.addEventListener("click", async function(event) {
        event.preventDefault(); // Evitar o envio do formulário padrão

        if (validateForm()) {
            const userData = {
                username: username.value.trim(),
                password: password.value.trim(),
                confirm_password: confirmPassword.value.trim(),
                role: document.querySelector('input[name="role"]:checked').value

            };
            
            const url = "http://127.0.0.1:5000/auth/register";  

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username.value,
                        password: password.value,
                        confirm_password: confirmPassword.value,
                        role: document.querySelector('input[name="role"]:checked').value

                    })
                });
            
                // Verifica se a resposta é bem-sucedida (status 200-299)
                if (!response.ok) {
                    throw new Error('Erro na requisição: ' + response.statusText);
                }
            
                // Verifica o tipo de conteúdo da resposta
                const contentType = response.headers.get('content-type');
                let result;
                if (contentType && contentType.includes('application/json')) {
                    result = await response.json();
                } else if (contentType && contentType.includes('text/html')) {
                    result = await response.text();
                } else {
                    throw new Error('Tipo de resposta inesperado');
                }
            
                // A partir daqui, você pode usar `result` para manipular a resposta
                console.log(result);  // Exibe o resultado no console
            
                // Se o resultado for bem-sucedido, redireciona para o login
                alert('Usuário registrado com sucesso!');
                window.location.href = "/frontend/login/login.html"; 
            } catch (error) {
                console.error('Erro:', error);
                alert('Ocorreu um erro. Por favor, tente novamente.');
         }
        }
})})