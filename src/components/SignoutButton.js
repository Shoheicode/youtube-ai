'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const SignOutButton = () => {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSignOut = async () => {
    setIsLoading(true);
    // Simulate API call
    try {
      await new Promise((resolve) => setTimeout(resolve, 1500));
      router.push('/sign-in'); // Redirect to dashboard after login
      // Handle successful login here
      console.log('Login successful');
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setIsLoading(false);
    }
  };
  

  return (
    <button
      onClick={handleSignOut}
      disabled={isLoading}
      className="relative flex items-center justify-center px-6 py-2 text-base font-medium text-white bg-blue-600 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 ease-in-out disabled:opacity-70"
    >
      {isLoading ? (
        <>
          <svg
            className="w-5 h-5 mr-2 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Logging in...
        </>
      ) : (
        <>
          <svg
            className="w-5 h-5 mr-2"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M3 3a1 1 0 011-1h12a1 1 0 011 1v12a1 1 0 01-1 1H4a1 1 0 01-1-1V3zm5 4a1 1 0 11-2 0 1 1 0 012 0zm6 5a1 1 0 100-2 1 1 0 000 2z"
              clipRule="evenodd"
            />
            <path d="M12 11a1 1 0 10-2 0v3a1 1 0 102 0v-3z" />
          </svg>
          Sign Out
        </>
      )}
    </button>
  );
};

export default LoginButton;