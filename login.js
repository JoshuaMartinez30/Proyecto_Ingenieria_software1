const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
let failedAttempts = 0; // Contador de intentos fallidos

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (failedAttempts >= 3) {
        alert('Has sido bloqueado después de 3 intentos fallidos.');
        return; // Bloquear el acceso después de 3 intentos fallidos
    }

    if (email === 'grupo123@gmail.com' && password === '12345') {
        window.location.href = 'http://127.0.0.1:5501/index.html';
    } else {
        failedAttempts++;
        alert(`Correo o contraseña incorrectos. Intentos fallidos: ${failedAttempts}`);
        if (failedAttempts >= 3) {
            alert('Has sido bloqueado después de 3 intentos fallidos.');
        }
    }
});

