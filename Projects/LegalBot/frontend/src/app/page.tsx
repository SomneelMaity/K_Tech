import { ChatInterface } from "@/components/chat/chat-interface";
import { SegmentSelector } from "@/components/segments/segment-selector";
import { EmergencyBanner } from "@/components/safety/emergency-banner";
import { Header } from "@/components/layout/header";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <Header />
      <EmergencyBanner />
      
      <div className="flex-1 container mx-auto px-4 py-8 max-w-6xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-4">
            ⚖️ LegalBot
          </h1>
          <p className="text-lg text-gray-600 mb-2">
            Your AI Legal Assistant for India
          </p>
          <p className="text-sm text-gray-500">
            Free, multilingual legal information • Not legal advice • Consult NALSA/DLSA for free legal aid
          </p>
        </div>

        <SegmentSelector />
        
        <div className="mt-8">
          <ChatInterface />
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold mb-2">🌐 10+ Languages</h3>
            <p className="text-gray-600">
              Get legal information in your language - Hindi, Bengali, Telugu, Tamil, and more
            </p>
          </div>
          <div className="p-4 bg-green-50 rounded-lg">
            <h3 className="font-semibold mb-2">📄 Document Generation</h3>
            <p className="text-gray-600">
              Generate legal notices, complaints, RTI applications, and more
            </p>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg">
            <h3 className="font-semibold mb-2">🆓 Free Legal Aid</h3>
            <p className="text-gray-600">
              Connect with NALSA/DLSA, Tele-Law, and helplines (1930/181/1098)
            </p>
          </div>
        </div>
      </div>

      <footer className="border-t mt-12 py-6 text-center text-sm text-gray-500">
        <p>
          Built to bridge India's justice gap • 5.39 crore+ pending cases • 
          <span className="font-semibold"> Everyone deserves legal information</span>
        </p>
      </footer>
    </main>
  );
}
