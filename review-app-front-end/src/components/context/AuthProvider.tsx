import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from 'react';

type User = {
  id: string;
  username: string;
  role: string;
  created_at: string;
};

type AuthContextType = {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const fetchCurrentUser = async () => {
    try {
      const res = await fetch('http://localhost:8000/auth/me', {
        method: 'GET',
        credentials: 'include',
      });

      if (res.ok) {
        const data: User = await res.json();
        setUser(data);
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    }
  };

  const login = async (username: string, password: string) => {
    const res = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) throw new Error('login failed');
    await fetchCurrentUser();
  };

  const register = async (username: string, password: string) => {
    const res = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) throw new Error('registration failed');
  };

  const logout = async () => {
    const res = await fetch('http://localhost:8000/auth/logout', {
      method: 'POST',
      credentials: 'include',
    });
    if (!res.ok) throw new Error('logout failed');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};
