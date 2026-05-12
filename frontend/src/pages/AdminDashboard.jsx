import React, { useEffect, useState } from 'react';
import { api, formatDateTimeIndian } from '../services/api.js';
import { AdminNav } from '../components/Nav.jsx';

export default function AdminDashboard() {
  const [employees, setEmployees] = useState([]);
  const [records, setRecords] = useState([]);

  useEffect(() => {
    api('/admin/employees').then(setEmployees).catch(() => {});
    api('/admin/attendance').then(setRecords).catch(() => {});
  }, []);

  return <div className="page">
    <div className="topbar"><div><h1>Admin Dashboard</h1><p className="muted">Indian date format: DD-MM-YYYY | Time: IST</p></div></div>
    <AdminNav />
    <div className="grid three">
      <div className="card"><h2>Total Employees</h2><p className="big">{employees.length}</p></div>
      <div className="card"><h2>Total Attendance Records</h2><p className="big">{records.length}</p></div>
      <div className="card"><h2>Latest Login</h2><p>{records[0]?.login_time ? formatDateTimeIndian(records[0].login_time) : '-'}</p></div>
    </div>
  </div>;
}
