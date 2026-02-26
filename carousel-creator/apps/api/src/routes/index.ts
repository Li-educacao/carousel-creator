import { Router, Request, Response } from 'express';
import carouselRoutes from './carousel.routes.js';
import exportRoutes from './export.routes.js';
import feedbackRoutes from './feedback.routes.js';
import personaRoutes from './persona.routes.js';
import renderRoutes from './render.routes.js';
import templateRoutes from './template.routes.js';

const router = Router();

router.get('/', (_req: Request, res: Response): void => {
  res.json({ message: 'Carousel Creator API', version: '1.0.0' });
});

router.use('/v1/carousels', carouselRoutes);
router.use('/v1/carousels', renderRoutes);
router.use('/v1/carousels', exportRoutes);
router.use('/v1/feedback', feedbackRoutes);
router.use('/v1/personas', personaRoutes);
router.use('/v1/templates', templateRoutes);

export default router;
