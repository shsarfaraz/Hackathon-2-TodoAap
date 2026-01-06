import { useState, useEffect } from 'react';
import { useSession } from '../lib/auth';

export const useAuthStatus = () => {
  const [authStatus, setAuthStatus] = useState<'checking' | 'authenticated' | 'unauthenticated'>('checking');
  const { data: session, isLoading } = useSession();

  useEffect(() => {
    if (isLoading) {
      setAuthStatus('checking');
    } else {
      setAuthStatus(session?.user ? 'authenticated' : 'unauthenticated');
    }
  }, [session, isLoading]);

  return { authStatus, session };
};