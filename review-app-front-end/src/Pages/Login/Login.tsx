import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../components/context/AuthProvider';

export default function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState<boolean>(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(username, password);
      setError('');
      navigate('/dashboard');
    } catch {
      setError('Invalid Credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gradient-to-b from-gray-950 via-gray-900 to-gray-800">
      {/* Login Card */}
      <div className="w-full max-w-md p-8 bg-gray-900/80 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-700 text-center">
        <h2 className="text-3xl font-bold text-white mb-6 drop-shadow-lg">
          Welcome Back
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full px-4 py-3 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:border-blue-500 placeholder-gray-400"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-3 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:border-blue-500 placeholder-gray-400"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg shadow-md transition-colors disabled:bg-gray-500"
          >
            {loading ? 'Logging in…' : 'Login'}
          </button>
        </form>

        {error && <p className="text-red-500 mt-4">{error}</p>}

        {/* Optional small secondary options */}
        <div className="flex justify-between mt-6 text-gray-400 text-sm">
          <button
            type="button"
            onClick={() => navigate('/register')}
            className="hover:text-white transition-colors"
          >
            Register
          </button>
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="hover:text-white transition-colors"
          >
            Continue as Guest
          </button>
        </div>
      </div>
    </div>
  );
}
