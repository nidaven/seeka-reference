/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    // fontLoaders: [
    //   {
    //     loader: "@next/font/google",
    //     options: { subsets: ["latin"] },
    //   },
    // ],
  },
  publicRuntimeConfig: {
    API_URL: process.env.API_URL || 'http://localhost:8080',
    DEBUG: true,
  },
}

export default nextConfig
