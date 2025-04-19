// pages/index.js
"use client";
import { useState, useEffect, use } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
// import { auth } from './firebase/firebase';
import LoginButton from '@/components/LoginButton';
// import { useAuth } from './hook/useAuth';
import SignOutButton from '@/components/SignoutButton';
import { addToDatabase } from '../firebase/firebase';
import { getDataFromDatabase } from '../firebase/firebase';
import { useAuth } from '../hook/useAuth';

export default function SavedHighlights() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      const data = await getDataFromDatabase();
      setResults(data);
    };
  
    if (user && !authLoading) {
      fetchData();
    }
  }, [user, authLoading]);
  


  // const {user} = useAuth();

  return (
    <div className="min-h-screen bg-gray-100">
      <nav>
        <div className="bg-blue-600 p-4">
          {user ?(
            <>
            <SignOutButton/>
           </>
          ): <>
            <LoginButton/>
          </>}
        </div>
      </nav>
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">Saved Youtube Highlights</h1>
        
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow p-6">
          {results && (
            <div className="mt-8">
              {/* <h2 className="text-2xl font-semibold mb-4">Results for "{results.query}"</h2> */}
              
              {results.length > 0 ? (
                <div className="space-y-6">
                  {results.map((appearance, index) => (
                    <div key={index} className="border rounded-lg overflow-hidden">
                      <div className="p-4">
                        <h3 className="text-xl font-medium mb-2">{appearance.title}</h3>
                        <p className="text-gray-600 mb-4">
                          {new Date(appearance.publishedAt).toLocaleDateString()} • {appearance.channelTitle}
                        </p>
                        <button className="mb-4 px-6 py-2 bg-blue-600 text-white font-medium rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200" onClick={()=>addToDatabase(appearance.title, appearance.channelTitle,appearance.publishedAt, appearance.highlights)}>Save</button>
                        
                        <h4 className="font-semibold mb-2">Key Highlights:</h4>
                        <div className="space-y-4">
                          {appearance.highlights.map((highlight, hIndex) => (
                            <div key={hIndex} className="bg-gray-50 p-4 rounded">
                              <div className="aspect-w-16 aspect-h-9 mb-3">
                                <iframe
                                  src={`https://www.youtube.com/embed/${appearance.videoId}?start=${highlight.startTime}&end=${highlight.endTime}`}
                                  title={`Highlight ${hIndex + 1}`}
                                  frameBorder="0"
                                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                  allowFullScreen
                                  className="w-full h-full rounded"
                                ></iframe>
                              </div>
                              <p>{highlight.text}</p>
                              <button onClick={
                                () => {
                                  const videoUrl = `https://www.youtube.com/watch?v=${appearance.videoId}&t=${highlight.startTime}`;
                                  window.open(videoUrl, '_blank');
                                }
                              } className="mt-2 text-blue-500 hover:underline" title="Open in YouTube">Watch on YouTube</button>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-700">No recent YouTube appearances found for this person.</p>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}