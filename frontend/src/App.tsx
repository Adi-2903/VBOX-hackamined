import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import StoryInputPage from './pages/StoryInputPage';
import EpisodeBreakdownPage from './pages/EpisodeBreakdownPage';
import AnalyticsDashboardPage from './pages/AnalyticsDashboardPage';
import SuggestionsPage from './pages/SuggestionsPage';
import AuthPage from './pages/AuthPage';
import LandingPage from './pages/LandingPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/input" element={<StoryInputPage />} />
        <Route path="/breakdown" element={<EpisodeBreakdownPage />} />
        <Route path="/analytics" element={<AnalyticsDashboardPage />} />
        <Route path="/suggestions" element={<SuggestionsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
