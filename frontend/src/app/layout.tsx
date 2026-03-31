import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'OrchestraFlow - Airflow Orchestration Dashboard',
  description: 'Production Data Pipeline Orchestration showcasing Apache Airflow capabilities.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#02000f] text-gray-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
