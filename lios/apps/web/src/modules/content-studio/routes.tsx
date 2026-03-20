import { lazy } from 'react';
import { Route } from 'react-router-dom';

const ContentPage = lazy(() => import('./pages/ContentPage'));

export const contentStudioRoutes = (
  <>
    <Route index element={<ContentPage />} />
  </>
);
