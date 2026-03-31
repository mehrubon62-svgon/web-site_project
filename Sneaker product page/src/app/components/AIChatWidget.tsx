import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Bot } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const aiResponses = [
  "I'd recommend the Intel Core i9-13900K for gaming builds. It offers excellent performance with 24 cores and a 5.8GHz boost clock.",
  "For a mid-range gaming PC, consider pairing the RTX 4070 with a Ryzen 5 7600X. Great price-to-performance ratio!",
  "Make sure your PSU has at least 25% overhead above your total system power consumption for stability and longevity.",
  "DDR5 is recommended for AM5 platform builds, while DDR4 still works great for Intel 12th/13th gen.",
  "For 4K gaming, the RTX 4080 or RX 7900 XTX would be ideal choices. They handle 4K at high framerates with ease.",
  "I can help you choose compatible components. What's your budget and primary use case?",
  "Your CPU and motherboard sockets must match — LGA1700 for Intel 12th/13th gen, AM5 for AMD Ryzen 7000 series.",
];

export function AIChatWidget() {
  const { isDark } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m BuildBot, your AI PC building consultant. How can I help you today?',
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  const sendMessage = () => {
    if (!input.trim()) return;
    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      const response = aiResponses[Math.floor(Math.random() * aiResponses.length)];
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1200 + Math.random() * 800);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      {/* Chat panel */}
      {isOpen && (
        <div
          className="flex flex-col rounded-lg overflow-hidden"
          style={{
            width: '360px',
            height: '480px',
            background: isDark ? '#1F2937' : '#FFFFFF',
            border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
            boxShadow: '0 10px 25px rgba(0,0,0,0.15)',
          }}
        >
          {/* Header */}
          <div
            className="flex items-center justify-between px-4 py-3 flex-shrink-0"
            style={{
              background: isDark ? '#111827' : '#F9FAFB',
              borderBottom: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
            }}
          >
            <div className="flex items-center gap-2">
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center"
                style={{ background: '#FBBF24' }}
              >
                <Bot size={16} style={{ color: '#111827' }} />
              </div>
              <div>
                <div className="text-sm font-semibold" style={{ color: isDark ? '#F9FAFB' : '#111827' }}>
                  BuildBot
                </div>
                <div className="text-xs" style={{ color: '#10B981' }}>● Online</div>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="hover:opacity-60 transition-opacity"
              style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
            >
              <X size={18} />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className="max-w-[80%] rounded-lg px-3 py-2 text-sm"
                  style={
                    msg.role === 'user'
                      ? { background: '#FBBF24', color: '#111827', borderRadius: '12px 12px 4px 12px' }
                      : {
                          background: isDark ? '#374151' : '#F3F4F6',
                          color: isDark ? '#F9FAFB' : '#111827',
                          borderRadius: '12px 12px 12px 4px',
                        }
                  }
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <div
                  className="px-4 py-3 rounded-lg"
                  style={{
                    background: isDark ? '#374151' : '#F3F4F6',
                    borderRadius: '12px 12px 12px 4px',
                  }}
                >
                  <div className="flex gap-1 items-center">
                    {[0, 1, 2].map(i => (
                      <div
                        key={i}
                        className="w-2 h-2 rounded-full"
                        style={{
                          background: '#9CA3AF',
                          animation: `bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
                        }}
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div
            className="flex items-center gap-2 px-3 py-3 flex-shrink-0"
            style={{ borderTop: `1px solid ${isDark ? '#374151' : '#E5E7EB'}` }}
          >
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about PC builds..."
              className="flex-1 text-sm outline-none bg-transparent"
              style={{ color: isDark ? '#F9FAFB' : '#111827' }}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim()}
              className="flex items-center justify-center w-8 h-8 rounded-full transition-opacity disabled:opacity-40"
              style={{ background: '#FBBF24' }}
            >
              <Send size={14} style={{ color: '#111827' }} />
            </button>
          </div>
        </div>
      )}

      {/* Floating button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-center w-12 h-12 rounded-full transition-opacity hover:opacity-90"
        style={{ background: '#FBBF24', boxShadow: '0 4px 12px rgba(251,191,36,0.4)' }}
      >
        {isOpen ? <X size={20} style={{ color: '#111827' }} /> : <MessageCircle size={20} style={{ color: '#111827' }} />}
      </button>

      <style>{`
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-6px); }
        }
      `}</style>
    </div>
  );
}
