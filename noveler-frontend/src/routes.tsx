import React from 'react';
import { Route, Routes } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import BuildPage from './pages/BuildPage';
import PlayPage from './pages/PlayPage';

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<LandingPage />} />
    <Route path="/build" element={<BuildPage />} />
    <Route path="/play" element={<PlayPage />} />
  </Routes>
);

export default AppRoutes;