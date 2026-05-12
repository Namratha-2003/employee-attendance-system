import React, { useEffect, useState } from 'react';
import { api, getCurrentLocation, formatDateTimeIndian } from '../services/api.js';
import { UserNav } from '../components/Nav.jsx';

export default function UserDashboard() {
  const [data, setData] = useState(null);
  const [geo, setGeo] = useState(null);
  const [message, setMessage] = useState('');

  async function load() {
    const now = new Date();
    setData(await api(`/user/dashboard?month=${now.getMonth() + 1}&year=${now.getFullYear()}`));
  }

  useEffect(() => { load(); }, []);
  useEffect(() => { getCurrentLocation().then(setGeo).catch((e) => setMessage(e.message)); }, []);

  async function mark(type) {
    setMessage('Getting location...');
    try {
      const location = await getCurrentLocation();
      setGeo(location);
      const res = await api(`/attendance/${type}`, { method: 'POST', body: JSON.stringify(location) });
      setMessage(res.message);
      await load();
    } catch (err) { setMessage(err.message); }
  }

  if (!data) return <div className="page">Loading...</div>;

  return <div className="page">
    <div className="topbar"><div><h1>User Dashboard</h1><p className="muted">Geo Location: {geo?.location || 'Allow browser location permission'}</p></div></div>
    <UserNav />
    {message && <div className="info">{message}</div>}
    <div className="grid three">
      <div className="card"><h2>Today Status</h2><p className="big">{data.today?.status || 'Not Logged In'}</p></div>
      <div className="card"><h2>Login Time</h2><p>{formatDateTimeIndian(data.today?.login_time)}</p></div>
      <div className="card"><h2>Total Month Hours</h2><p className="big">{data.total_month_hours}</p></div>
    </div>
    <div className="card">
      <h2>Mark Attendance</h2>
      <p>Attendance will not be recorded on weekends and Indian holiday calendar days.</p>
      <div className="actions"><button onClick={() => mark('login')}>Login</button><button onClick={() => mark('logout')}>Logout</button></div>
    </div>
  </div>;
}
