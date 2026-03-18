import { Router, Request, Response } from 'express';
import { supabaseAdmin } from '../../../lib/supabase.js';

const router = Router();

/**
 * GET /api/v1/pedagogico/metrics
 * Dashboard metrics — counts by status, classes summary.
 */
router.get('/', async (_req: Request, res: Response): Promise<void> => {
  try {
    // Students by status
    const { data: students, error: studentsErr } = await supabaseAdmin
      .from('ped_students')
      .select('status');

    if (studentsErr) throw studentsErr;

    const studentCounts: Record<string, number> = {};
    let totalStudents = 0;
    for (const s of students ?? []) {
      studentCounts[s.status] = (studentCounts[s.status] || 0) + 1;
      totalStudents++;
    }

    // Classes with enrollment counts
    const { data: classes, error: classesErr } = await supabaseAdmin
      .from('ped_classes')
      .select('id, status, ped_enrollments(count)');

    if (classesErr) throw classesErr;

    const activeClasses = (classes ?? []).filter(c => c.status === 'active').length;
    const totalClasses = (classes ?? []).length;

    // Total enrollments
    const { count: totalEnrollments } = await supabaseAdmin
      .from('ped_enrollments')
      .select('id', { count: 'exact', head: true });

    res.json({
      students: {
        total: totalStudents,
        active: studentCounts['active'] || 0,
        inactive: studentCounts['inactive'] || 0,
        cancelled: studentCounts['cancelled'] || 0,
        refunded: studentCounts['refunded'] || 0,
      },
      classes: {
        total: totalClasses,
        active: activeClasses,
      },
      enrollments: {
        total: totalEnrollments ?? 0,
      },
    });
  } catch (err) {
    res.status(500).json({ error: { message: (err as Error).message, code: 'METRICS_ERROR' } });
  }
});

export default router;
