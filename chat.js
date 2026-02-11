/**
 * Modern Mestri - Interactive Chat Assistant (Drawer Edition)
 */

// DOM Elements
const chatElements = {
    trigger: document.getElementById('chatToggle'),
    panel: document.getElementById('chatInterface'),
    close: document.getElementById('closeChat'),
    messages: document.getElementById('chatMessages'),
    input: document.getElementById('chatInput'),
    sendBtn: document.getElementById('chatSendBtn')
};

// ========================================
// Initialization
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    setupChatListeners();
});

function setupChatListeners() {
    // Open chat
    chatElements.trigger.addEventListener('click', () => {
        chatElements.panel.classList.toggle('hidden');
        if (!chatElements.panel.classList.contains('hidden')) {
            chatElements.input.focus();
        }
    });

    // Close chat
    chatElements.close.addEventListener('click', () => {
        chatElements.panel.classList.add('hidden');
    });

    // Send message
    chatElements.sendBtn.addEventListener('click', processSendMessage);

    // Enter key press
    chatElements.input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') processSendMessage();
    });
}

// ========================================
// Message Processing
// ========================================
async function processSendMessage() {
    const text = chatElements.input.value.trim();
    if (!text) return;

    // Add User Message
    addChatMessage('user', text);
    chatElements.input.value = '';

    // Show AI Typing
    const typingId = showTypingStatus();

    try {
        const response = await fetch(`${window.ModernMestri.API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                context: getProjectContext()
            })
        });

        const data = await response.json();
        removeTypingStatus(typingId);

        if (data.success) {
            addChatMessage('assistant', data.response);
        } else {
            addChatMessage('assistant', "I'm sorry, I'm having trouble processing that right now. Please try again later.");
        }
    } catch (error) {
        removeTypingStatus(typingId);
        addChatMessage('assistant', "I'm offline right now. Please make sure the backend server is running.");
    }
}

function addChatMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${role}`;
    msgDiv.style.display = 'flex';
    msgDiv.style.gap = '0.75rem';
    msgDiv.style.justifyContent = role === 'user' ? 'flex-end' : 'flex-start';

    const content = document.createElement('div');
    content.className = 'msg-content';
    content.style.background = role === 'user' ? 'var(--primary)' : 'var(--slate-100)';
    content.style.color = role === 'user' ? 'white' : 'var(--slate-800)';
    content.style.padding = '0.75rem 1rem';
    content.style.borderRadius = '12px';
    content.style.fontSize = '0.95rem';
    content.style.maxWidth = '85%';
    content.style.boxShadow = 'var(--shadow-soft)';
    content.innerHTML = text.replace(/\n/g, '<br>');

    msgDiv.appendChild(content);
    chatElements.messages.appendChild(msgDiv);

    // Auto Scroll
    chatElements.messages.scrollTop = chatElements.messages.scrollHeight;
}

function showTypingStatus() {
    const typingId = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.id = typingId;
    typingDiv.className = 'chat-message assistant';
    typingDiv.innerHTML = `
        <div style="background: var(--slate-100); padding: 0.5rem 1rem; border-radius: 12px; font-size: 0.85rem; color: var(--slate-500); font-style: italic;">
            AI Assistant is thinking...
        </div>
    `;
    chatElements.messages.appendChild(typingDiv);
    chatElements.messages.scrollTop = chatElements.messages.scrollHeight;
    return typingId;
}

function removeTypingStatus(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function getProjectContext() {
    if (!window.currentProject) return null;
    return {
        project: window.currentProject,
        plan: window.currentPlan
    };
}
