import React, { useState } from 'react';
import { api, go } from '../services/api.js';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [resetLink, setResetLink] = useState('');

  async function submit(e) {
    e.preventDefault();
    setMessage('');
    setResetLink('');
    try {
      const res = await api('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) });
      setMessage(res.message);
      if (res.reset_link_for_testing) setResetLink(res.reset_link_for_testing);
    } catch (err) {
      setMessage(err.message);
    }
  }

  return <div className="login-page">
    <form className="login-card" onSubmit={submit}>
      <h1>Forgot Password</h1>
      <p>Enter your registered email. Reset link will be sent to email.</p>
      {message && <div className="info">{message}</div>}
      {resetLink && <div className="warning">Email is not configured. Test link:<br />{resetLink}</div>}
      <label>Email</label>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <button>Send Reset Link</button>
      <button type="button" className="linkbtn" onClick={() => go('/login')}>Back to login</button>
    </form>
  </div>;
}
