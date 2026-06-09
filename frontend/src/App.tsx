// Root component — placeholder until auth + routing are wired up in Wave 1.3+
function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex items-center justify-center">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold text-blue-400">
          TI Investigation Platform
        </h1>
        <p className="text-gray-400">Wave 1 — Foundation in progress</p>
        <div className="inline-flex items-center gap-2 bg-green-900/30 text-green-400 px-4 py-2 rounded-lg border border-green-800">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          Frontend running
        </div>
      </div>
    </div>
  )
}

export default App
