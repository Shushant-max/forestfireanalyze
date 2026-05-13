const AUTH_API_BASE = 'http://localhost:5000/auth';
const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID';

function postJSON(url, payload) {
    return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).then(async (resp) => {
        const data = await resp.json();
        if (!resp.ok) {
            throw new Error(data.error || 'Authentication failed');
        }
        return data;
    });
}

function saveUserSession(user) {
    localStorage.setItem('forestFireUser', JSON.stringify(user));
}

function getUserSession() {
    try {
        return JSON.parse(localStorage.getItem('forestFireUser')) || null;
    } catch {
        return null;
    }
}

function clearUserSession() {
    localStorage.removeItem('forestFireUser');
}

function logout() {
    clearUserSession();
    window.location.href = 'login.html';
}

function showAuthError(message) {
    const errorElement = document.getElementById('authError');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearAuthError() {
    const errorElement = document.getElementById('authError');
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

async function handleSignup(event) {
    event.preventDefault();
    clearAuthError();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!name || !email || !password) {
        showAuthError('Please enter name, email, and password.');
        return;
    }

    try {
        const response = await postJSON(`${AUTH_API_BASE}/signup`, { name, email, password });
        saveUserSession(response.user);
        window.location.href = 'index.html';
    } catch (error) {
        showAuthError(error.message);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    clearAuthError();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
        showAuthError('Please enter your email and password.');
        return;
    }

    try {
        const response = await postJSON(`${AUTH_API_BASE}/login`, { email, password });
        saveUserSession(response.user);
        window.location.href = 'index.html';
    } catch (error) {
        showAuthError(error.message);
    }
}

async function handleGoogleCredentialResponse(response) {
    clearAuthError();
    if (!response.credential) {
        showAuthError('Google sign in failed.');
        return;
    }

    try {
        const data = await postJSON(`${AUTH_API_BASE}/google`, { id_token: response.credential });
        saveUserSession(data.user);
        window.location.href = 'index.html';
    } catch (error) {
        showAuthError(error.message);
    }
}

function initGoogleSignIn() {
    if (GOOGLE_CLIENT_ID === 'YOUR_GOOGLE_CLIENT_ID') {
        showAuthError('Google login requires a valid GOOGLE_CLIENT_ID. Update auth.js with your client ID to enable sign in.');
        return;
    }

    if (typeof google === 'undefined' || !google.accounts || !google.accounts.id) {
        showAuthError('Google Identity Services is not loaded yet.');
        return;
    }

    google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true
    });

    const googleButton = document.getElementById('googleButton');
    if (googleButton) {
        google.accounts.id.renderButton(googleButton, {
            theme: 'outline',
            size: 'large',
            width: '100%'
        });
    }
}

function initAuthPage(mode) {
    const currentUser = getUserSession();
    if (currentUser) {
        window.location.href = 'index.html';
        return;
    }

    const form = document.getElementById(`${mode}Form`);
    if (form) {
        form.addEventListener('submit', mode === 'signup' ? handleSignup : handleLogin);
    }

    if (document.getElementById('googleButton')) {
        if (typeof google === 'undefined' || !google.accounts || !google.accounts.id) {
            window.addEventListener('load', initGoogleSignIn);
        } else {
            initGoogleSignIn();
        }
    }
}

function loadUserProfile() {
    const authBar = document.getElementById('authBar');
    const user = getUserSession();
    if (!authBar) return;

    if (user) {
        authBar.innerHTML = `
            <span class="auth-welcome">Welcome, ${user.name}</span>
            <button class="logout-btn" onclick="logout()">Logout</button>
        `;
    } else {
        authBar.innerHTML = `
            <a href="login.html">Login</a>
            <span class="auth-divider">|</span>
            <a href="signup.html">Sign Up</a>
        `;
    }
}

window.initAuthPage = initAuthPage;
window.loadUserProfile = loadUserProfile;
window.logout = logout;
window.handleGoogleCredentialResponse = handleGoogleCredentialResponse;
