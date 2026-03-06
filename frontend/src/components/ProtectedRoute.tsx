import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useEffect } from 'react';
import toast from 'react-hot-toast';

export const ProtectedRoute = ({ children }: { children: React.ReactElement }) => {
    const { isAuthenticated } = useAuth();

    useEffect(() => {
        if (!isAuthenticated) {
            toast.error("Please login to access your studio", {
                duration: 4000,
                position: 'bottom-center',
                style: {
                    border: '4px solid #0A192F',
                    padding: '16px',
                    color: '#0A192F',
                    background: '#FF9E9E',
                    fontWeight: 900,
                    textTransform: 'uppercase',
                    borderRadius: '999px',
                    boxShadow: '4px 4px 0px #0A192F'
                },
                iconTheme: {
                    primary: '#0A192F',
                    secondary: '#FF9E9E',
                },
            });
        }
    }, [isAuthenticated]);

    if (!isAuthenticated) {
        return <Navigate to="/auth" replace />;
    }

    return children;
};
