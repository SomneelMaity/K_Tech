export function Header() {
  return (
    <header className="border-b bg-white">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold">⚖️ LegalBot</h1>
        </div>
        <div className="flex items-center space-x-4">
          <select className="px-3 py-1 border rounded">
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
            <option value="bn">বাংলা</option>
            <option value="te">తెలుగు</option>
            <option value="ta">தமிழ்</option>
          </select>
        </div>
      </div>
    </header>
  );
}
