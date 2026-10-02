/** @type {import('next').NextConfig} */
const rawBackendUrl = process.env.NEXT_PUBLIC_API_URL || "https://spectra-v1nc.onrender.com";
// Strip trailing slashes and trailing /api to ensure destination is cleanly `${cleanBackendUrl}/api/:path*`
const cleanBackendUrl = rawBackendUrl.replace(/\/+$/, "").replace(/\/api$/, "");

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${cleanBackendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
