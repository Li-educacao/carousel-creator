import { Router, Request, Response } from 'express';
import { supabaseAdmin } from '../../../lib/supabase.js';

const router = Router();

/**
 * GET /api/v1/pedagogico/metrics
 * Rich dashboard metrics.
 */
router.get('/', async (_req: Request, res: Response): Promise<void> => {
  try {
    // All students with metadata
    const { data: students } = await supabaseAdmin
      .from('ped_students')
      .select('id, status, metadata, created_at');

    // All enrollments with class info
    const { data: enrollments } = await supabaseAdmin
      .from('ped_enrollments')
      .select('id, status, amount_paid, payment_method, purchase_date, class_id, ped_classes(abbreviation, name, product_name, status)');

    // All classes
    const { data: classes } = await supabaseAdmin
      .from('ped_classes')
      .select('id, abbreviation, name, product_name, status, start_date, ped_enrollments(count)');

    const allStudents = students ?? [];
    const allEnrollments = enrollments ?? [];
    const allClasses = classes ?? [];

    // ─── Students by status ──────────────────────────────────────────────
    const studentsByStatus: Record<string, number> = {};
    for (const s of allStudents) {
      studentsByStatus[s.status] = (studentsByStatus[s.status] || 0) + 1;
    }

    // ─── Climatrônico level distribution ─────────────────────────────────
    const climatronicoLevels: Record<string, number> = {};
    for (const s of allStudents) {
      const level = (s.metadata as Record<string, unknown>)?.climatronico_level as string || 'Sem info';
      climatronicoLevels[level] = (climatronicoLevels[level] || 0) + 1;
    }

    // ─── Plan distribution ───────────────────────────────────────────────
    const planDistribution: Record<string, number> = {};
    for (const s of allStudents) {
      const plan = (s.metadata as Record<string, unknown>)?.plan as string || 'Sem info';
      planDistribution[plan] = (planDistribution[plan] || 0) + 1;
    }

    // ─── Revenue ─────────────────────────────────────────────────────────
    let totalRevenue = 0;
    const revenueByProduct: Record<string, number> = {};
    const paymentMethods: Record<string, number> = {};

    for (const e of allEnrollments) {
      const amount = Number(e.amount_paid) || 0;
      totalRevenue += amount;

      const cls = e.ped_classes as unknown as Record<string, string> | null;
      const product = cls?.product_name || 'Outros';
      revenueByProduct[product] = (revenueByProduct[product] || 0) + amount;

      const method = e.payment_method || 'Não informado';
      paymentMethods[method] = (paymentMethods[method] || 0) + 1;
    }

    // ─── Enrollments by product ──────────────────────────────────────────
    const enrollmentsByProduct: Record<string, number> = {};
    for (const e of allEnrollments) {
      const cls = e.ped_classes as unknown as Record<string, string> | null;
      const product = cls?.product_name || 'Outros';
      enrollmentsByProduct[product] = (enrollmentsByProduct[product] || 0) + 1;
    }

    // ─── Monthly trend (last 12 months) ──────────────────────────────────
    const monthlyEnrollments: Record<string, number> = {};
    const now = new Date();
    for (let i = 11; i >= 0; i--) {
      const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
      monthlyEnrollments[key] = 0;
    }
    for (const e of allEnrollments) {
      if (!e.purchase_date) continue;
      const d = new Date(e.purchase_date as string);
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
      if (key in monthlyEnrollments) {
        monthlyEnrollments[key]++;
      }
    }

    // ─── Students expiring soon (next 30 days) ──────────────────────────
    const expiringStudents: Array<{ name: string; email: string; days: number; access_until: string }> = [];
    for (const s of allStudents) {
      const meta = s.metadata as Record<string, unknown>;
      const accessUntil = meta?.access_until as string;
      const daysRemaining = meta?.days_remaining as number;
      if (accessUntil && daysRemaining !== undefined && daysRemaining > 0 && daysRemaining <= 30) {
        expiringStudents.push({
          name: '', // will be filled below
          email: '',
          days: daysRemaining,
          access_until: accessUntil,
        });
      }
    }

    // ─── Top classes by student count ────────────────────────────────────
    const topClasses = allClasses
      .map(c => ({
        abbreviation: c.abbreviation,
        name: c.name,
        product_name: c.product_name,
        student_count: ((c.ped_enrollments as Array<{ count: number }>)?.[0]?.count) ?? 0,
        status: c.status,
        start_date: c.start_date,
      }))
      .sort((a, b) => b.student_count - a.student_count)
      .slice(0, 10);

    // ─── Students with upcoming renewals ─────────────────────────────────
    let renewalsDue = 0;
    for (const s of allStudents) {
      const meta = s.metadata as Record<string, unknown>;
      const renewal = meta?.renewal_date as string;
      if (renewal) {
        const renewalDate = new Date(renewal);
        const diff = (renewalDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24);
        if (diff >= 0 && diff <= 60) renewalsDue++;
      }
    }

    res.json({
      students: {
        total: allStudents.length,
        byStatus: studentsByStatus,
        climatronicoLevels,
        planDistribution,
        renewalsDue,
      },
      classes: {
        total: allClasses.length,
        active: allClasses.filter(c => c.status === 'active').length,
        topClasses,
      },
      enrollments: {
        total: allEnrollments.length,
        byProduct: enrollmentsByProduct,
        monthlyTrend: monthlyEnrollments,
        paymentMethods,
      },
      revenue: {
        total: totalRevenue,
        byProduct: revenueByProduct,
      },
    });
  } catch (err) {
    res.status(500).json({ error: { message: (err as Error).message, code: 'METRICS_ERROR' } });
  }
});

export default router;
