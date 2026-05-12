import React, { useEffect, useState } from 'react';
import Login from './pages/Login.jsx';
import ForgotPassword from './pages/ForgotPassword.jsx';
import ResetPassword from './pages/ResetPassword.jsx';
import AdminDashboard from './pages/AdminDashboard.jsx';
import AdminEmployees from './pages/AdminEmployees.jsx';
import AdminAttendance from './pages/AdminAttendance.jsx';
import UserDashboard from './pages/UserDashboard.jsx';
import UserProfile from './pages/UserProfile.jsx';
import UserAttendance from './pages/UserAttendance.jsx';
import { getUser, go } from './services/api.js';

export default function App() {
  const [path, setPath] = useState(window.location.pathname);
  const user = getUser();

  useEffect(() => {
    const onChange = () => setPath(window.location.pathname);
    window.addEventListener('popstate', onChange);
    return () => window.removeEventListener('popstate', onChange);
  }, []);

  if (path === '/forgot-password') return <ForgotPassword />;
  if (path === '/reset-password') return <ResetPassword />;
  if (!user) return <Login />;

  if (user.is_admin) {
    if (path === '/' || path === '/login') go('/admin/dashboard');
    if (path === '/admin/employees') return <AdminEmployees />;
    if (path === '/admin/attendance') return <AdminAttendance />;
    return <AdminDashboard />;
  }

  if (path === '/' || path === '/login') go('/user/dashboard');
  if (path === '/user/profile') return <UserProfile />;
  if (path === '/user/attendance') return <UserAttendance />;
  return <UserDashboard />;
}
