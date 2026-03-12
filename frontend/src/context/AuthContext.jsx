import { createContext, useContext, useState, useEffect } from 'react';
import API from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('lexram_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      API.get('/auth/me')
        .then((res) => setUser(res.data))
        .catch(() => {
          setToken(null);
          localStorage.removeItem('lexram_token');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    const res = await API.post('/auth/login', { email, password });
    const t = res.data.access_token;
    localStorage.setItem('lexram_token', t);
    setToken(t);
    const me = await API.get('/auth/me');
    setUser(me.data);
    return me.data;
  };

  const signup = async (username, email, password) => {
    await API.post('/auth/signup', { username, email, password });
    return login(email, password);
  };

  const logout = () => {
    localStorage.removeItem('lexram_token');
    localStorage.removeItem('lexram_user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
