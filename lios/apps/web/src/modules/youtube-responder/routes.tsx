import { lazy } from 'react';
import { Route } from 'react-router-dom';

const YouTubeDashboard = lazy(() => import('./pages/YouTubeDashboard'));

export const youtubeResponderRoutes = (
  <>
    <Route index element={<YouTubeDashboard />} />
  </>
);
