const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Error de red' }));
    throw new Error(err.detail || `Error ${res.status}`);
  }
  return res.json();
}

export async function login(email, password) {
  const body = new URLSearchParams();
  body.append('username', email);
  body.append('password', password);
  return request('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
}

export async function logout() {
  return request('/logout', { method: 'POST' });
}

export async function predict(data) {
  return request('/predict/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}
