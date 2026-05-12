import React, { useEffect, useState } from 'react';
import { api, formatDateIndian } from '../services/api.js';
import { AdminNav } from '../components/Nav.jsx';

export default function AdminEmployees() {
  const [employees, setEmployees] = useState([]);
  const [message, setMessage] = useState('');
  const [form, setForm] = useState({ employee_id: '', name: '', email: '', phone: '', role: 'employee', department: '' });

  async function loadEmployees() { setEmployees(await api('/admin/employees')); }
  useEffect(() => { loadEmployees(); }, []);

  async function createEmployee(e) {
    e.preventDefault();
    setMessage('');
    try {
      const res = await api('/admin/employees', { method: 'POST', body: JSON.stringify(form) });
      setMessage(`Employee created. Email sent: ${res.email_sent ? 'Yes' : 'No'}. Temporary password: ${res.temporary_password_for_testing}`);
      setForm({ employee_id: '', name: '', email: '', phone: '', role: 'employee', department: '' });
      loadEmployees();
    } catch (err) { setMessage(err.message); }
  }

  return <div className="page">
    <div className="topbar"><div><h1>Employees</h1><p className="muted">Admin can create employee and password will be mailed.</p></div></div>
    <AdminNav />
    {message && <div className="info">{message}</div>}
    <div className="grid two">
      <form className="card" onSubmit={createEmployee}>
        <h2>Create New Employee</h2>
        <input placeholder="Employee ID" value={form.employee_id} onChange={(e) => setForm({ ...form, employee_id: e.target.value })} required />
        <input placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <input placeholder="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        <input placeholder="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        <input placeholder="Role" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} />
        <input placeholder="Department" value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })} />
        <button>Create Employee & Send Password</button>
      </form>
      <div className="card">
        <h2>Employee List</h2>
        <table><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Created</th></tr></thead>
          <tbody>{employees.map(e => <tr key={e.id}><td>{e.employee_id}</td><td>{e.name}</td><td>{e.email}</td><td>{e.role}</td><td>{formatDateIndian(e.created_at)}</td></tr>)}</tbody>
        </table>
      </div>
    </div>
  </div>;
}
