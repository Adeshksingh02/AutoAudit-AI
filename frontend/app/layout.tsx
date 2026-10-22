import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AutoAudit AI Pro",
  description: "Autonomous Multi-Agent Vulnerability Scanner",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-zinc-950">{children}</body>
    </html>
  );
}