import React, { useState } from 'react';
import { api, go } from '../services/api.js';

export default function ResetPassword() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token') || '';
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [message, setMessage] = useState('');

  async function submit(e) {
    e.preventDefault();
    if (password !== confirm) return setMessage('Passwords do not match');
    try {
      const res = await api('/auth/reset-password', { method: 'POST', body: JSON.stringify({ token, new_password: password }) });
      setMessage(res.message);
      setTimeout(() => go('/login'), 1200);
    } catch (err) {
      setMessage(err.message);
    }
  }

  return <div className="login-page">
    <form className="login-card" onSubmit={submit}>
      <h1>Reset Password</h1>
      {message && <div className="info">{message}</div>}
      <label>New Password</label>
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength="6" />
      <label>Confirm Password</label>
      <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} required minLength="6" />
      <button>Set Password</button>
    </form>
  </div>;
}
