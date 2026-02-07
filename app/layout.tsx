import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'HealthForge — Proactive Wellness Kit Builder',
  description: 'AI-powered wellness kit builder. Get personalized workout plans, supplements, gear, and meal plans tailored to your goals, allergies, and preferences.',
  openGraph: {
    title: 'HealthForge — Proactive Wellness Kit Builder',
    description: 'Build your perfect wellness kit with AI. Personalized exercises, supplements, gear, and meal plans.',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="bg-gray-50 text-gray-900 antialiased">{children}</body>
    </html>
  )
}
