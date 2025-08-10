import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Gabarita.AI - Prepare-se para o CNU com Inteligência Artificial',
  description: 'A plataforma mais avançada para estudar para concursos públicos. Questões personalizadas, simulados inteligentes e correção automática de redações.',
  keywords: 'CNU, concurso público, inteligência artificial, questões, simulados, redação, estudos',
  authors: [{ name: 'Gabarita.AI' }],
  openGraph: {
    title: 'Gabarita.AI - Prepare-se para o CNU com IA',
    description: 'Revolucione seus estudos para concursos com nossa plataforma de IA avançada.',
    url: 'https://gabarita.ai',
    siteName: 'Gabarita.AI',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Gabarita.AI - Plataforma de estudos com IA',
      },
    ],
    locale: 'pt_BR',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Gabarita.AI - Prepare-se para o CNU com IA',
    description: 'Revolucione seus estudos para concursos com nossa plataforma de IA avançada.',
    images: ['/og-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}