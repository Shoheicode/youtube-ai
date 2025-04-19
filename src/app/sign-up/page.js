// pages/login.js
"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { initializeApp } from 'firebase/app';
import { auth,signInWithEmailAndPassword, signUpWithEmail } from '../firebase/firebase';

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSignUp = async (e) => {
        e.preventDefault();
        setLoading(true);
        setErrorMsg("");

        try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        console.log("Signed up as:", user.email);

        router.push("/"); // Redirect to homepage after successful signup
        } catch (error) {
        // console.error("Signup error:", error.code);

        switch (error.code) {
            case "auth/email-already-in-use":
                setErrorMsg("An account with this email already exists.");
                break;
            case "auth/invalid-email":
                setErrorMsg("Please enter a valid email address.");
                break;
            case "auth/weak-password":
                setErrorMsg("Password must be at least 6 characters.");
                break;
            default:
                setErrorMsg("Something went wrong. Please try again.");
                break;
        }
        }

        setLoading(false);
    };
  
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100">
        <form
          onSubmit={handleSignUp}
          className="bg-white p-8 rounded-lg shadow-lg w-96 space-y-4"
        >
          <h2 className="text-2xl font-bold text-center">Sign-Up</h2>
          {/* {error && <p className="text-red-500 text-sm">{error}</p>} */}
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
          {errorMsg && <p className="text-red-600 text-sm">{errorMsg}</p>}
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