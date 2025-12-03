<!-- layout content -->
<!DOCTYPE html>
<html lang="en" class="h-full bg-gray-50">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@yield('title', 'Modern App')</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --primary-color: #4f46e5;
            --secondary-color: #6366f1;
            --error-color: #ef4444;
        }

        .input:focus {
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
        }

        .password-toggle {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: var(--primary-color);
            font-size: 0.875rem;
            cursor: pointer;
        }

        .error-message {
            transition: opacity 0.3s ease;
            opacity: 0;
            height: 0;
            overflow: hidden;
        }

        .error-message.show {
            opacity: 1;
            height: auto;
        }

        .loading-spinner {
            border: 2px solid #fff;
            border-top: 2px solid transparent;
            border-radius: 50%;
            width: 16px;
            height: 16px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="h-full font-inter">
    @yield('content')
    
    <script>
        const togglePassword = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const loginButton = document.getElementById('loginButton');
        const loginButtonText = document.getElementById('loginButtonText');
        const loginButtonSpinner = document.getElementById('loginButtonSpinner');
        const loginForm = document.getElementById('loginForm');
        const emailInput = document.getElementById('email');
        const emailError = document.getElementById('emailError');
        const passwordError = document.getElementById('passwordError');

        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePassword.textContent = type === 'password' ? 'Show' : 'Hide';
        });

        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = emailInput.value.trim();
            const password = passwordInput.value.trim();
            
            let isValid = true;
            
            if (!/\S+@\S+\.\S+/.test(email)) {
                emailError.classList.add('show');
                isValid = false;
            } else {
                emailError.classList.remove('show');
            }
            
            if (password.length < 8) {
                passwordError.classList.add('show');
                isValid = false;
            } else {
                passwordError.classList.remove('show');
            }
            
            if (isValid) {
                loginButton.disabled = true;
                loginButtonText.textContent = 'Logging in...';
                loginButtonSpinner.classList.remove('hidden');
                
                setTimeout(() => {
                    loginButton.disabled = false;
                    loginButtonText.textContent = 'Login';
                    loginButtonSpinner.classList.add('hidden');
                    alert('Login successful!');
                }, 2000);
            }
        });
    </script>
</body>
</html>