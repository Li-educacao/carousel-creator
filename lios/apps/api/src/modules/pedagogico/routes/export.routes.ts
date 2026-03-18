import { Router, Request, Response } from 'express';
import { requirePermission } from '../../../middleware/rbac.js';
import { googleSheetsService } from '../services/google-sheets.service.js';

const router = Router();

/**
 * POST /api/v1/pedagogico/export/sheets
 * Export all students to Google Sheets (or return data for download).
 */
router.post('/sheets', requirePermission('pedagogico', 'write'), async (_req: Request, res: Response): Promise<void> => {
  try {
    const result = await googleSheetsService.exportConsolidated();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: { message: (err as Error).message, code: 'EXPORT_ERROR' } });
  }
});

/**
 * POST /api/v1/pedagogico/export/sheets/:classId
 * Export students from a specific class.
 */
router.post('/sheets/:classId', requirePermission('pedagogico', 'write'), async (req: Request, res: Response): Promise<void> => {
  try {
    const result = await googleSheetsService.exportByClass(req.params.classId as string);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: { message: (err as Error).message, code: 'EXPORT_ERROR' } });
  }
});

/**
 * GET /api/v1/pedagogico/export/csv
 * Download all students as CSV.
 */
router.get('/csv', async (_req: Request, res: Response): Promise<void> => {
  try {
    const rows = await googleSheetsService.buildExportData();
    const csv = googleSheetsService.toCSV(rows);

    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
    res.setHeader('Content-Disposition', 'attachment; filename=alunos-consolidado.csv');
    res.send('\uFEFF' + csv); // BOM for Excel UTF-8
  } catch (err) {
    res.status(500).json({ error: { message: (err as Error).message, code: 'EXPORT_ERROR' } });
  }
});

/**
 * GET /api/v1/pedagogico/export/csv/:classId
 * Download students from a specific class as CSV.
 */
router.get('/csv/:classId', async (req: Request, res: Response): Promise<void> => {
  try {
    const rows = await googleSheetsService.buildExportData(req.params.classId as string);
    const csv = googleSheetsService.toCSV(rows);

    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
    res.setHeader('Content-Disposition', `attachment; filename=alunos-turma-${req.params.classId as string}.csv`);
    res.send('\uFEFF' + csv);
  } catch (err) {
    res.status(500).json({ error: { message: (err as Error).message, code: 'EXPORT_ERROR' } });
  }
});

export default router;
