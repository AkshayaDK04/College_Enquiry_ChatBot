document.addEventListener('DOMContentLoaded', function() {
    const chatbotWidget = document.getElementById('chatbotWidget');
    const closeChatbot = document.getElementById('closeChatbot');
    const sendMessage = document.getElementById('sendMessage');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    // Toggle mobile menu
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });

    // Show chatbot when clicking the chat button
    document.querySelectorAll('[href*="chatbot"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            chatbotWidget.style.display = 'block';
        });
    });

    // Close chatbot
    closeChatbot.addEventListener('click', () => {
        chatbotWidget.style.display = 'none';
    });

    // Send message
    sendMessage.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            appendMessage('user', message);
            userInput.value = '';
            // Simulate bot response
            setTimeout(() => {
                appendMessage('bot', 'Thank you for your message. I\'m here to help!');
            }, 1000);
        }
    });

    // Send message on Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage.click();
        }
    });

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.innerHTML = `
            <div class="message-content ${sender}">
                ${sender === 'bot' ? '<i class="fas fa-robot"></i>' : ''}
                <p>${text}</p>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});