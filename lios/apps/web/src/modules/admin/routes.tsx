import { lazy } from 'react';
import { Route } from 'react-router-dom';

const UsersPage = lazy(() => import('./pages/UsersPage'));

export const adminRoutes = (
  <>
    <Route index element={<UsersPage />} />
    <Route path="usuarios" element={<UsersPage />} />
  </>
);
