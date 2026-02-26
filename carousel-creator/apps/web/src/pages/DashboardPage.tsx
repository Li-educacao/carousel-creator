import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import type { Carousel } from '@carousel/shared';
import { Button, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Badge } from '../components/ui';
import { useAuth } from '../contexts/AuthContext';
import { useCarousel } from '../hooks/useCarousel';
import { cn } from '../lib/utils';

const STATUS_LABELS: Record<string, string> = {
  draft: 'Rascunho',
  text_validated: 'Textos Validados',
  images_generated: 'Imagens Geradas',
  exported: 'Exportado',
};

const STATUS_VARIANTS: Record<string, 'default' | 'warning' | 'info' | 'success'> = {
  draft: 'default',
  text_validated: 'info',
  images_generated: 'warning',
  exported: 'success',
};

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

function CarouselCard({
  carousel,
  onEdit,
  onDelete,
}: {
  carousel: Carousel;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}) {
  return (
    <Card variant="elevated" className="flex flex-col">
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-base leading-tight">{carousel.title}</CardTitle>
          <Badge variant={STATUS_VARIANTS[carousel.status] ?? 'default'}>
            {STATUS_LABELS[carousel.status] ?? carousel.status}
          </Badge>
        </div>
        <CardDescription className="mt-1">
          {carousel.theme}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-4 text-xs font-body text-brand-gray">
          <span>{carousel.slide_count} slides</span>
          <span>{formatDate(carousel.created_at)}</span>
        </div>
      </CardContent>
      <CardFooter className="mt-auto">
        <Button size="sm" variant="secondary" onClick={() => onEdit(carousel.id)}>
          Editar
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => onDelete(carousel.id)}
          className="text-red-400 hover:text-red-300 hover:bg-red-500/10"
        >
          Excluir
        </Button>
      </CardFooter>
    </Card>
  );
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, signOut } = useAuth();
  const { getCarousels, deleteCarousel, loading } = useCarousel();

  const [carousels, setCarousels] = useState<Carousel[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const limit = 12;
  const pages = Math.ceil(total / limit);

  // Show success after validation
  useEffect(() => {
    const state = location.state as { validated?: string } | null;
    if (state?.validated) {
      setSuccessMessage('Textos validados com sucesso!');
      setTimeout(() => setSuccessMessage(null), 4000);
      navigate('/', { replace: true, state: null });
    }
  }, [location.state, navigate]);

  async function load(p: number) {
    const result = await getCarousels(p, limit);
    if (result) {
      setCarousels(result.data);
      setTotal(result.pagination.total);
    }
  }

  useEffect(() => {
    load(page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page]);

  async function handleDelete(id: string) {
    if (!window.confirm('Excluir este carrossel? Esta ação não pode ser desfeita.')) return;
    const ok = await deleteCarousel(id);
    if (ok) {
      setCarousels((prev) => prev.filter((c) => c.id !== id));
      setTotal((prev) => prev - 1);
    }
  }

  return (
    <div className="min-h-screen bg-brand-black">
      {/* Top bar */}
      <header className="border-b border-brand-gray/10 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-heading text-brand-blue">Carousel Creator</h1>
          <div className="flex items-center gap-3">
            <span className="text-sm font-body text-brand-gray hidden sm:block">{user?.email}</span>
            <Button size="sm" variant="ghost" onClick={() => navigate('/feedback')}>
              Aprendizado
            </Button>
            <Button size="sm" variant="ghost" onClick={() => navigate('/settings')}>
              Configuracoes
            </Button>
            <Button size="sm" variant="ghost" onClick={signOut}>
              Sair
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Page header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-heading text-white">Meus Carrosséis</h2>
            <p className="text-sm font-body text-brand-gray mt-1">
              {total === 0 ? 'Nenhum carrossel criado ainda' : `${total} carrossel${total !== 1 ? 'is' : ''}`}
            </p>
          </div>
          <Button variant="primary" onClick={() => navigate('/new')}>
            + Novo Carrossel
          </Button>
        </div>

        {/* Success message */}
        {successMessage && (
          <div className="mb-4 px-4 py-3 rounded-lg bg-green-500/10 border border-green-500/30 text-green-400 text-sm font-body">
            {successMessage}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-48 rounded-xl bg-white/5 animate-pulse" />
            ))}
          </div>
        )}

        {/* Empty state */}
        {!loading && carousels.length === 0 && (
          <div className="flex flex-col items-center justify-center py-24 text-center">
            <p className="text-brand-gray font-body mb-4">
              Crie seu primeiro carrossel para Instagram
            </p>
            <Button variant="primary" size="lg" onClick={() => navigate('/new')}>
              Criar Carrossel
            </Button>
          </div>
        )}

        {/* Grid */}
        {!loading && carousels.length > 0 && (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {carousels.map((c) => (
                <CarouselCard
                  key={c.id}
                  carousel={c}
                  onEdit={(id) => navigate(`/carousel/${id}`)}
                  onDelete={handleDelete}
                />
              ))}
            </div>

            {/* Pagination */}
            {pages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-8">
                <Button
                  size="sm"
                  variant="ghost"
                  disabled={page === 1}
                  onClick={() => setPage((p) => p - 1)}
                >
                  Anterior
                </Button>
                {Array.from({ length: pages }, (_, i) => i + 1).map((p) => (
                  <button
                    key={p}
                    onClick={() => setPage(p)}
                    className={cn(
                      'w-8 h-8 rounded-lg text-sm font-subtitle transition-colors',
                      p === page
                        ? 'bg-brand-blue text-white'
                        : 'text-brand-gray hover:text-white hover:bg-white/10'
                    )}
                  >
                    {p}
                  </button>
                ))}
                <Button
                  size="sm"
                  variant="ghost"
                  disabled={page === pages}
                  onClick={() => setPage((p) => p + 1)}
                >
                  Próxima
                </Button>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
