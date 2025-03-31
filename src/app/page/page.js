// pages/index.js
import { useState } from 'react';
import Head from 'next/head';

export default function Home() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch results');
      }
      
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Error fetching results: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>YouTube Appearance Finder</title>
        <meta name="description" content="Find recent YouTube appearances of notable people" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">YouTube Appearance Finder</h1>
        
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow p-6">
          <form onSubmit={handleSubmit} className="mb-6">
            <div className="mb-4">
              <label htmlFor="query" className="block text-gray-700 mb-2">
                Enter a person's identity (e.g., "Howard Marks, leading US investor")
              </label>
              <input
                type="text"
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Howard Marks, leading US investor"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200"
              disabled={loading}
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>

          {error && (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6">
              <p>{error}</p>
            </div>
          )}

          {results && (
            <div className="mt-8">
              <h2 className="text-2xl font-semibold mb-4">Results for "{results.query}"</h2>
              
              {results.appearances.length > 0 ? (
                <div className="space-y-6">
                  {results.appearances.map((appearance, index) => (
                    <div key={index} className="border rounded-lg overflow-hidden">
                      <div className="p-4">
                        <h3 className="text-xl font-medium mb-2">{appearance.title}</h3>
                        <p className="text-gray-600 mb-4">
                          {new Date(appearance.publishedAt).toLocaleDateString()} • {appearance.channelTitle}
                        </p>
                        
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