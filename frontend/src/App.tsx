import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { ClipLoader } from "react-spinners";

function LoadingSpinner() {
  return <div className="spinner"></div>
}

function App() {
  let [loading, setLoading] = useState(false);

  let [query, setQuery] = useState("");

  let [result, setResult] = useState("");

  return (
    <div>
      <h1>💡 Luminist</h1>
      <div className="input-container p-5 flex flex-row">
        <div className="flex flex-col justify-center">
          <span className="text-white">Query:</span>
          <textarea className="bg-white text-black m-5" value={query} onChange={(e) => setQuery(e.target.value)} disabled={loading} />
        </div>
        <div className="flex flex-col justify-center">
        <button onClick={() => {
          setLoading(true);
          setResult("");
          fetch("http://localhost:8000/query", {
            method: "POST",
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ query: query }),
          }).then((res) => res.json()).then((data) => {
            setResult(data.result);
            setLoading(false);
          });
        }}
        disabled={loading}
        >Submit</button>
        </div>
      </div>
      <div className="loading-container">
        <ClipLoader
        color="#00AAFF"
        loading={loading}
      />
      </div>
      <div>{result}</div>
    </div>
  )
}

export default App
