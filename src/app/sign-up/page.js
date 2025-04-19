// pages/login.js
"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { initializeApp } from 'firebase/app';
import { auth,signInWithEmailAndPassword, signUpWithEmail } from '../firebase/firebase';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();
    // const {user} = useAuth();
     
    const handleLogin = async (e) => {
      e.preventDefault();
      setLoading(true);
      setError('');
  
      try {
        await signInWithEmailAndPassword(auth, email, password);
        router.push('/'); // Redirect to dashboard after login
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    const handleSignUp = async (e) => {
      e.preventDefault();
      setLoading(true);
      setError('');
  
      const { user, error } = await signUpWithEmail(email, password);
      if (error) {
        setErrorMessage(error);  // Show user-friendly error message in UI
      } else {
        router.push("/");        // Redirect on success
      }
    };
  
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100">
        <form
          onSubmit={handleLogin}
          className="bg-white p-8 rounded-lg shadow-lg w-96 space-y-4"
        >
          <h2 className="text-2xl font-bold text-center">Login</h2>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-2 border rounded-md"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full px-4 py-2 border rounded-md"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
          <button
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
            disabled={loading}
            onClick={handleSignUp}
          >
            {loading ? 'Logging in...' : 'Sign Up'}
          </button>
        </form>
      </div>
    );
  }