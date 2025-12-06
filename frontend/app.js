const chatEl = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');

function appendMessage(sender, text) {
  const el = document.createElement('div');
  el.className = 'message ' + (sender === 'user' ? 'user' : 'bot');
  el.textContent = text;
  chatEl.appendChild(el);
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function sendMessage(message) {
  appendMessage('user', message);
  try {
    const resp = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_message: message })
    });
    const data = await resp.json();
    if (data && data.reply) {
      appendMessage('bot', data.reply);
    } else if (data && data.reply === undefined && data.error) {
      appendMessage('bot', 'Error: ' + data.error);
    } else {
      appendMessage('bot', JSON.stringify(data));
    }
  } catch (err) {
    appendMessage('bot', 'Network error: ' + err.message);
  }
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const val = input.value.trim();
  if (!val) return;
  input.value = '';
  sendMessage(val);
});

// welcome message
appendMessage('bot', 'Welcome to HardChews Support! Ask me anything about orders, refunds, or products.');
