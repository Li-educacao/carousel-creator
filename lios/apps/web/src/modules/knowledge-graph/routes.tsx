import { lazy } from 'react';
import { Route } from 'react-router-dom';

const KnowledgeGraphDashboard = lazy(() => import('./pages/KnowledgeGraphDashboard'));

export const knowledgeGraphRoutes = (
  <>
    <Route index element={<KnowledgeGraphDashboard />} />
  </>
);
