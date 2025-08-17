/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    unoptimized: true,
    domains: ['localhost', 'vercel.app', 'kjjorqly.manus.space'],
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'https://j6h5i7c0x703.manus.space',
    NEXT_PUBLIC_FRONTEND_URL: process.env.NEXT_PUBLIC_FRONTEND_URL || 'https://kjjorqly.manus.space',
  },
  // Removed typescript: { ignoreBuildErrors: true } to fix Vercel build
};

module.exports = nextConfig;
