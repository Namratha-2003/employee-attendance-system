const API_BASE = 'https://employee-attendance-system-vwox.onrender.com/api';
export function getToken() {
  return localStorage.getItem('token');
}

export function getUser() {
  const raw = localStorage.getItem('user');
  return raw ? JSON.parse(raw) : null;
}

export function go(path) {
  window.history.pushState({}, '', path);
  window.dispatchEvent(new PopStateEvent('popstate'));
}

export function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  go('/login');
}

export function formatDateIndian(value) {
  if (!value) return '-';
  const d = new Date(value.includes('T') ? value : `${value}T00:00:00`);
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'Asia/Kolkata' }).replaceAll('/', '-');
}

export function formatDateTimeIndian(value) {
  if (!value) return '-';
  return new Date(value).toLocaleString('en-IN', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: true, timeZone: 'Asia/Kolkata'
  }).replace(',', '').replaceAll('/', '-');
}

export function formatTimeIndian(value) {
  if (!value) return '-';
  return new Date(value).toLocaleTimeString('en-IN', {
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true, timeZone: 'Asia/Kolkata'
  });
}

export async function api(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!response.ok) {
    let detail = 'Something went wrong';
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch {}
    throw new Error(detail);
  }
  return response.json();
}

export async function downloadFile(path, filename) {
  const token = getToken();
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error('Export failed');
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  window.URL.revokeObjectURL(url);
}

export async function getCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported in this browser'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        let location = `${latitude}, ${longitude}`;
        try {
          const res = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`);
          const data = await res.json();
          location = data.display_name || location;
        } catch {}
        resolve({ latitude, longitude, location });
      },
      () => reject(new Error('Please allow location permission')),
      { enableHighAccuracy: true, timeout: 15000 }
    );
  });
}
