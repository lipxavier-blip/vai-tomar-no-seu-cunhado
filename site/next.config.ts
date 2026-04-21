import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'd3wo5wojvuv7l.cloudfront.net',
      },
    ],
  },
};

export default nextConfig;
