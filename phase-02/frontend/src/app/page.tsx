'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '../lib/auth';

export default function LandingPage() {
  const [authStatus, setAuthStatus] = useState<'checking' | 'authenticated' | 'unauthenticated'>('checking');
  const router = useRouter();

  useEffect(() => {
    const checkAuthStatus = () => {
      try {
        const authenticated = isAuthenticated();
        setAuthStatus(authenticated ? 'authenticated' : 'unauthenticated');
      } catch (error) {
        console.error('Error checking auth status:', error);
        setAuthStatus('unauthenticated');
      }
    };

    checkAuthStatus();
  }, []);

  if (authStatus === 'checking') {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#f5f8fa' }}>
        <div className="text-center">
          <div className="relative w-10 h-10 mx-auto mb-3">
            <div className="absolute inset-0 rounded-full border-2 border-gray-300"></div>
            <div className="absolute inset-0 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin"></div>
          </div>
          <p className="text-sm" style={{ color: '#828a93' }}>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#f5f8fa' }}>
      {/* Yahoo-style Navigation */}
      <nav className="bg-white border-b" style={{ borderColor: '#e0e4e9', height: '57px' }}>
        <div className="max-w-7xl mx-auto px-4 h-full flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-2xl font-semibold" style={{ color: '#7e1fff' }}>TaskFlow</h1>
          </div>
          <div className="flex items-center gap-2">
            {authStatus === 'authenticated' ? (
              <>
                <button
                  onClick={() => router.push('/dashboard')}
                  className="text-sm px-3 py-2 hover:bg-gray-50 rounded"
                  style={{ color: '#232a31' }}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => {
                    localStorage.removeItem('access_token');
                    setAuthStatus('unauthenticated');
                  }}
                  className="text-sm px-4 py-2 rounded"
                  style={{ backgroundColor: '#f0f3f5', color: '#232a31' }}
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => router.push('/auth/login')}
                  className="text-sm px-3 py-2 hover:bg-gray-50 rounded"
                  style={{ color: '#232a31' }}
                >
                  Sign In
                </button>
                <button
                  onClick={() => router.push('/auth/register')}
                  className="text-sm px-4 py-2 rounded font-medium"
                  style={{ backgroundColor: '#7e1fff', color: '#ffffff' }}
                >
                  Sign Up
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section - Yahoo Style */}
      <section className="py-10 bg-white">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <h1 className="text-3xl font-semibold mb-3" style={{ color: '#232a31' }}>
            Organize Your Tasks Efficiently
          </h1>
          <p className="text-base mb-6" style={{ color: '#6e7780' }}>
            Simple and powerful task management for everyone
          </p>

          <div className="flex gap-3 justify-center">
            {authStatus === 'authenticated' ? (
              <button
                onClick={() => router.push('/dashboard')}
                className="px-6 py-2.5 rounded font-medium text-sm"
                style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
              >
                Go to Dashboard
              </button>
            ) : (
              <>
                <button
                  onClick={() => router.push('/auth/register')}
                  className="px-6 py-2.5 rounded font-medium text-sm"
                  style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
                >
                  Get Started Free
                </button>
                <button
                  onClick={() => router.push('/auth/login')}
                  className="px-6 py-2.5 rounded font-medium text-sm border"
                  style={{ backgroundColor: '#ffffff', color: '#232a31', borderColor: '#e0e4e9', minHeight: '44px' }}
                >
                  Sign In
                </button>
              </>
            )}
          </div>

          <div className="mt-4 flex justify-center gap-6 text-xs" style={{ color: '#828a93' }}>
            <span>✓ Free Forever</span>
            <span>✓ No Credit Card</span>
            <span>✓ Secure</span>
          </div>
        </div>
      </section>

      {/* Features - Yahoo Grid Style */}
      <section className="py-10" style={{ backgroundColor: '#f5f8fa' }}>
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-xl font-semibold text-center mb-6" style={{ color: '#232a31' }}>
            Key Features
          </h2>

          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded" style={{ border: '1px solid #e0e4e9' }}>
              <h3 className="text-sm font-semibold mb-1" style={{ color: '#232a31' }}>
                ✓ Task Management
              </h3>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Create and organize tasks easily
              </p>
            </div>

            <div className="bg-white p-4 rounded" style={{ border: '1px solid #e0e4e9' }}>
              <h3 className="text-sm font-semibold mb-1" style={{ color: '#232a31' }}>
                ✓ Fast Performance
              </h3>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Lightning-fast and responsive
              </p>
            </div>

            <div className="bg-white p-4 rounded" style={{ border: '1px solid #e0e4e9' }}>
              <h3 className="text-sm font-semibold mb-1" style={{ color: '#232a31' }}>
                ✓ Secure & Private
              </h3>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                JWT authentication protection
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="py-8 bg-white">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <p className="text-xs font-semibold mb-3" style={{ color: '#828a93' }}>
            BUILT WITH
          </p>

          <div className="flex flex-wrap justify-center gap-3">
            {['Next.js', 'FastAPI', 'PostgreSQL', 'TypeScript'].map((tech) => (
              <span
                key={tech}
                className="px-3 py-1.5 rounded text-xs font-medium"
                style={{ backgroundColor: '#f0f3f5', color: '#232a31' }}
              >
                {tech}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-10" style={{ backgroundColor: '#f5f8fa' }}>
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-semibold mb-2" style={{ color: '#232a31' }}>
            Ready to Get Started?
          </h2>
          <p className="mb-6" style={{ color: '#6e7780' }}>
            Join now and start organizing your tasks
          </p>
          <button
            onClick={() => router.push(authStatus === 'authenticated' ? '/dashboard' : '/auth/register')}
            className="px-8 py-3 rounded font-medium text-sm"
            style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '48px' }}
          >
            {authStatus === 'authenticated' ? 'Go to Dashboard' : 'Get Started Free'}
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-6" style={{ backgroundColor: '#ffffff', borderColor: '#e0e4e9' }}>
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-xs mb-1" style={{ color: '#828a93' }}>
            <span className="font-semibold" style={{ color: '#7e1fff' }}>TaskFlow</span> - Modern Task Management
          </p>
          <p className="text-xs" style={{ color: '#828a93' }}>
            © 2025 TaskFlow. Built with Next.js, FastAPI & PostgreSQL
          </p>
        </div>
      </footer>
    </div>
  );
}
