import React, { useEffect, useState } from 'react';
import { api, formatDateIndian, formatTimeIndian } from '../services/api.js';
import { UserNav } from '../components/Nav.jsx';

export default function UserAttendance() {
  const now = new Date();
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [year, setYear] = useState(now.getFullYear());
  const [data, setData] = useState(null);
  async function load() { setData(await api(`/user/dashboard?month=${month}&year=${year}`)); }
  useEffect(() => { load(); }, [month, year]);
  if (!data) return <div className="page">Loading...</div>;
  return <div className="page">
    <div className="topbar"><div><h1>My Attendance</h1><p className="muted">Date format: DD-MM-YYYY | Time: Indian Standard Time</p></div></div>
    <UserNav />
    <div className="card">
      <h2>Monthly Filter</h2>
      <div className="row"><input type="number" min="1" max="12" value={month} onChange={(e) => setMonth(e.target.value)} /><input type="number" value={year} onChange={(e) => setYear(e.target.value)} /></div>
      <p><b>Total Working Hours:</b> {data.total_month_hours}</p>
    </div>
    <div className="card">
      <h2>History</h2>
      <table><thead><tr><th>Date</th><th>Login</th><th>Logout</th><th>Hours</th><th>Status</th><th>Login Location</th></tr></thead>
        <tbody>{data.monthly_records.map((r) => <tr key={r.id}>
          <td>{formatDateIndian(r.attendance_date)}</td><td>{formatTimeIndian(r.login_time)}</td><td>{formatTimeIndian(r.logout_time)}</td><td>{r.total_hours}</td><td>{r.status}</td><td>{r.login_location || '-'}</td>
        </tr>)}</tbody>
      </table>
    </div>
  </div>;
}
