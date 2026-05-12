import React from 'react';
import { go, logout } from '../services/api.js';

export function AdminNav() {
  return <div className="nav">
    <button onClick={() => go('/admin/dashboard')}>Dashboard</button>
    <button onClick={() => go('/admin/employees')}>Employees</button>
    <button onClick={() => go('/admin/attendance')}>Attendance Report</button>
    <button className="secondary" onClick={logout}>Logout</button>
  </div>;
}

export function UserNav() {
  return <div className="nav">
    <button onClick={() => go('/user/dashboard')}>Dashboard</button>
    <button onClick={() => go('/user/profile')}>Profile</button>
    <button onClick={() => go('/user/attendance')}>My Attendance</button>
    <button className="secondary" onClick={logout}>Logout</button>
  </div>;
}
