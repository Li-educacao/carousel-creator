import { Router } from 'express';
import { authMiddleware } from '../../middleware/auth.js';
import { requireRole } from '../../middleware/rbac.js';
import userRoutes from './routes/user.routes.js';

const adminRouter = Router();

// All admin routes require authentication + admin role
adminRouter.use(authMiddleware);
adminRouter.use(requireRole('admin'));

// Mount sub-routes
adminRouter.use('/users', userRoutes);

export default adminRouter;
