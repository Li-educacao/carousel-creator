import { supabaseAdmin } from '../../../lib/supabase.js';

/**
 * Google Sheets Export Service.
 * Exports student data to Google Sheets as a redundancy layer.
 * Requires GOOGLE_SERVICE_ACCOUNT_JSON env var to be configured.
 * Without credentials, export generates data but skips Sheets upload.
 */

interface SheetRow {
  nome: string;
  email: string;
  telefone: string;
  cpf: string;
  turma: string;
  sigla: string;
  produto: string;
  data_compra: string;
  valor: string;
  status: string;
  data_cadastro: string;
}

export const googleSheetsService = {
  /**
   * Check if Google Sheets integration is configured.
   */
  isConfigured(): boolean {
    return !!process.env.GOOGLE_SERVICE_ACCOUNT_JSON;
  },

  /**
   * Export all students to a consolidated sheet.
   * Returns the data that would be/was exported.
   */
  async exportConsolidated(): Promise<{ rows: SheetRow[]; exported: boolean; message: string }> {
    const rows = await this.buildExportData();

    if (!this.isConfigured()) {
      return {
        rows,
        exported: false,
        message: 'Google Sheets não configurado. Dados gerados mas não exportados. Configure GOOGLE_SERVICE_ACCOUNT_JSON para habilitar.',
      };
    }

    // TODO: Implement actual Google Sheets API upload when credentials are available
    // const sheets = google.sheets({ version: 'v4', auth });
    // await sheets.spreadsheets.values.update({ ... });

    return {
      rows,
      exported: false,
      message: 'Google Sheets API integration pendente de implementação. Dados disponíveis para download.',
    };
  },

  /**
   * Export students from a specific class.
   */
  async exportByClass(classId: string): Promise<{ rows: SheetRow[]; exported: boolean; className: string; message: string }> {
    const rows = await this.buildExportData(classId);

    const { data: cls } = await supabaseAdmin
      .from('ped_classes')
      .select('name, abbreviation')
      .eq('id', classId)
      .single();

    const className = cls ? `[${cls.abbreviation}] ${cls.name}` : 'Turma desconhecida';

    if (!this.isConfigured()) {
      return {
        rows,
        exported: false,
        className,
        message: 'Google Sheets não configurado. Dados gerados para download.',
      };
    }

    return {
      rows,
      exported: false,
      className,
      message: 'Google Sheets API integration pendente. Dados disponíveis para download.',
    };
  },

  /**
   * Build export data from database.
   */
  async buildExportData(classId?: string): Promise<SheetRow[]> {
    let query = supabaseAdmin
      .from('ped_enrollments')
      .select(`
        *,
        ped_students ( full_name, email, phone, cpf, created_at ),
        ped_classes ( name, abbreviation, product_name )
      `)
      .order('enrolled_at', { ascending: false });

    if (classId) {
      query = query.eq('class_id', classId);
    }

    const { data: enrollments, error } = await query;

    if (error) throw new Error(`Failed to fetch export data: ${error.message}`);

    return (enrollments ?? []).map((e: Record<string, unknown>) => {
      const student = e.ped_students as Record<string, string> | null;
      const cls = e.ped_classes as Record<string, string> | null;

      return {
        nome: student?.full_name ?? '',
        email: student?.email ?? '',
        telefone: student?.phone ?? '',
        cpf: student?.cpf ?? '',
        turma: cls?.name ?? '',
        sigla: cls?.abbreviation ?? '',
        produto: cls?.product_name ?? '',
        data_compra: e.purchase_date ? new Date(e.purchase_date as string).toLocaleDateString('pt-BR') : '',
        valor: e.amount_paid ? `R$ ${Number(e.amount_paid).toFixed(2)}` : '',
        status: String(e.status ?? ''),
        data_cadastro: student?.created_at ? new Date(student.created_at).toLocaleDateString('pt-BR') : '',
      };
    });
  },

  /**
   * Convert rows to CSV string for download.
   */
  toCSV(rows: SheetRow[]): string {
    const headers = ['Nome', 'Email', 'Telefone', 'CPF', 'Turma', 'Sigla', 'Produto', 'Data Compra', 'Valor', 'Status', 'Data Cadastro'];
    const csvRows = rows.map(r => [
      r.nome, r.email, r.telefone, r.cpf, r.turma, r.sigla, r.produto, r.data_compra, r.valor, r.status, r.data_cadastro,
    ].map(v => `"${(v ?? '').replace(/"/g, '""')}"`).join(';'));

    return [headers.join(';'), ...csvRows].join('\n');
  },
};
