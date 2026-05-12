import React, { useEffect, useState } from 'react';
import { api, formatDateIndian } from '../services/api.js';
import { UserNav } from '../components/Nav.jsx';

export default function UserProfile() {
  const [data, setData] = useState(null);
  useEffect(() => {
    const now = new Date();
    api(`/user/dashboard?month=${now.getMonth() + 1}&year=${now.getFullYear()}`).then(setData);
  }, []);
  if (!data) return <div className="page">Loading...</div>;
  const p = data.profile;
  return <div className="page">
    <div className="topbar"><div><h1>My Profile</h1><p className="muted">Employee details</p></div></div>
    <UserNav />
    <div className="card profile-card">
      <h2>{p.name}</h2>
      <p><b>Employee ID:</b> {p.employee_id}</p>
      <p><b>Email:</b> {p.email}</p>
      <p><b>Role:</b> {p.role}</p>
      <p><b>Department:</b> {p.department || '-'}</p>
      <p><b>Created:</b> {formatDateIndian(p.created_at)}</p>
    </div>
  </div>;
}
