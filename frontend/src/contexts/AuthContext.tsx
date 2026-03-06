import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

interface AuthContextType {
    isAuthenticated: boolean;
    user: string | null;
    login: (token: string, username: string) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [user, setUser] = useState<string | null>(null);
    const navigate = useNavigate();

    // Check localStorage on mount to persist session
    useEffect(() => {
        const token = localStorage.getItem('episense_token');
        const storedUser = localStorage.getItem('episense_user');
        if (token) {
            setIsAuthenticated(true);
            setUser(storedUser);
        }
    }, []);

    const login = (token: string, username: string) => {
        localStorage.setItem('episense_token', token);
        localStorage.setItem('episense_user', username);
        setIsAuthenticated(true);
        setUser(username);
    };

    const logout = () => {
        localStorage.removeItem('episense_token');
        localStorage.removeItem('episense_user');
        setIsAuthenticated(false);
        setUser(null);
        toast('Logged out successfully', { icon: '👋', duration: 3000 });
        navigate('/auth');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
