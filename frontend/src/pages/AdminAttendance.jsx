import React, { useEffect, useState } from 'react';
import { api, downloadFile, formatDateIndian, formatDateTimeIndian } from '../services/api.js';
import { AdminNav } from '../components/Nav.jsx';

export default function AdminAttendance() {
  const now = new Date();
  const [records, setRecords] = useState([]);
  const [message, setMessage] = useState('');
  const [filters, setFilters] = useState({ employee_id: '', name: '', day: '', month: now.getMonth() + 1, year: now.getFullYear() });

  function queryString() {
    const q = new URLSearchParams();
    Object.entries(filters).forEach(([k, v]) => { if (v) q.append(k, v); });
    return q.toString();
  }

  async function loadAttendance() {
    try { setRecords(await api(`/admin/attendance?${queryString()}`)); }
    catch (err) { setMessage(err.message); }
  }
  useEffect(() => { loadAttendance(); }, []);

  async function exportExcel() { await downloadFile(`/admin/attendance/export?${queryString()}`, 'attendance_report.xlsx'); }

  return <div className="page">
    <div className="topbar"><div><h1>Attendance Report</h1><p className="muted">Filter by employee ID, name, daily or monthly. Excel uses DD-MM-YYYY and IST.</p></div></div>
    <AdminNav />
    {message && <div className="info">{message}</div>}
    <div className="card">
      <h2>Filters</h2>
      <div className="filters">
        <input placeholder="Employee ID" value={filters.employee_id} onChange={(e) => setFilters({ ...filters, employee_id: e.target.value })} />
        <input placeholder="Name" value={filters.name} onChange={(e) => setFilters({ ...filters, name: e.target.value })} />
        <input type="date" value={filters.day} onChange={(e) => setFilters({ ...filters, day: e.target.value })} />
        <input type="number" min="1" max="12" value={filters.month} onChange={(e) => setFilters({ ...filters, month: e.target.value })} />
        <input type="number" value={filters.year} onChange={(e) => setFilters({ ...filters, year: e.target.value })} />
        <button onClick={loadAttendance}>Apply Filter</button>
        <button onClick={exportExcel}>Download Excel</button>
      </div>
    </div>
    <div className="card">
      <h2>All Attendance Records</h2>
      <table><thead><tr><th>Emp ID</th><th>Name</th><th>Date</th><th>Login</th><th>Logout</th><th>Hours</th><th>Status</th><th>Location</th></tr></thead>
        <tbody>{records.map((r) => <tr key={r.id}>
          <td>{r.employee_id}</td><td>{r.employee_name}</td><td>{formatDateIndian(r.attendance_date)}</td>
          <td>{formatDateTimeIndian(r.login_time)}</td><td>{formatDateTimeIndian(r.logout_time)}</td><td>{r.total_hours}</td><td>{r.status}</td>
          <td>{r.login_location || `${r.login_latitude || ''}, ${r.login_longitude || ''}`}</td>
        </tr>)}</tbody>
      </table>
    </div>
  </div>;
}
