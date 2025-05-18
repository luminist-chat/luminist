import { useState } from 'react'
import './App.css'

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: { file: string; page: number; link: string }[];
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [entities, setEntities] = useState<string[]>([]);

  const send = async () => {
    if (!input.trim()) return;
    const question = input;
    setMessages([...messages, { role: 'user', content: question }]);
    setInput('');
    setLoading(true);
    const res = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    setMessages(m => [...m, { role: 'assistant', content: data.answer, citations: data.citations }]);
    if (data.entities) setEntities(data.entities);
    setLoading(false);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">💡 Luminist</h1>
      <div className="space-y-4 mb-4">
        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'text-right' : 'text-left'}>
            <div className="border p-2 inline-block bg-gray-100 text-black">
              {m.content}
              {m.role === 'assistant' && m.citations && (
                <div className="mt-2 text-xs">
                  {m.citations.map((c, idx) => (
                    <a key={idx} href={c.link} target="_blank" className="mr-2 underline">{c.file}:{c.page}</a>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      {entities.length > 0 && (
        <div className="mb-4">
          {entities.map((e, idx) => (
            <span key={idx} className="inline-block bg-blue-200 text-black px-2 py-1 mr-2 rounded">
              {e}
            </span>
          ))}
        </div>
      )}
      <div className="flex space-x-2">
        <input
          className="flex-1 border text-black p-2"
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
        />
        <button className="border px-4" onClick={send} disabled={loading}>Send</button>
      </div>
    </div>
  );
}

export default App
