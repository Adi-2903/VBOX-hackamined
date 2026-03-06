import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import StoryInputPage from './pages/StoryInputPage';
import EpisodeBreakdownPage from './pages/EpisodeBreakdownPage';
import AnalyticsDashboardPage from './pages/AnalyticsDashboardPage';
import SuggestionsPage from './pages/SuggestionsPage';
import AuthPage from './pages/AuthPage';
import LandingPage from './pages/LandingPage';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Toaster />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/dashboard" element={
            <ProtectedRoute><DashboardPage /></ProtectedRoute>
          } />
          <Route path="/input" element={
            <ProtectedRoute><StoryInputPage /></ProtectedRoute>
          } />
          <Route path="/breakdown" element={
            <ProtectedRoute><EpisodeBreakdownPage /></ProtectedRoute>
          } />
          <Route path="/analytics" element={
            <ProtectedRoute><AnalyticsDashboardPage /></ProtectedRoute>
          } />
          <Route path="/suggestions" element={
            <ProtectedRoute><SuggestionsPage /></ProtectedRoute>
          } />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
