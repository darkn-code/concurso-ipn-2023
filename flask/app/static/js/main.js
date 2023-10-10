var script = document.querySelector('script[src="../static/js/main.js"]');
var username = script.getAttribute('username')
document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-button');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const chatBoxTyping = document.getElementById('chat-typing');
    let typingTimeout; 

       const socket = io.connect('https://' + document.domain + ':' + location.port);
       console.log(socket);
       socket.on('connect', function() {
           console.log('Conectado al servidor WebSocket');
           
           while (chatBox.firstChild) {
            chatBox.removeChild(chatBox.firstChild);
            }
            
           const botInitialMessage = "Hola, soy EduMentorBot. ¿En qué puedo ayudarte?";
           const botInitialMessageElement = document.createElement('div');
           botInitialMessageElement.className = 'message bot-message';
           botInitialMessageElement.style.color = 'black';
           const boldText = document.createElement('b');
           boldText.textContent = 'EduMentorBot: ' + botInitialMessage;
           botInitialMessageElement.appendChild(boldText);
           chatBox.appendChild(botInitialMessageElement);
           chatBox.scrollTop = chatBox.scrollHeight;
       });
   
       socket.on('bot_response', function(data) {
           const botMessage = data.response;
           clearTimeout(typingTimeout);
           while (chatBoxTyping.firstChild) {
            chatBoxTyping.removeChild(chatBoxTyping.firstChild);
            }
           addBotMessage(botMessage);
       });
    function sendMessage() {
        const message = userInput.value.trim();
        console.log(username);  
        if (message === '') {
            return; 
        }
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'message user-message';
        userMessageElement.style.color = 'blue';
        const boldText = document.createElement('b');
        boldText.textContent = username +': ' + message;
        userMessageElement.appendChild(boldText);
      
        chatBox.appendChild(userMessageElement);
        userInput.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        socket.emit('user_message', message);
        showTypingMessage();


    }
    function clearChatBox(){
        while (chatBox.firstChild) {
            chatBox.removeChild(chatBox.firstChild);
        }
    }

    function showTypingMessage() {
        const botTypingMessageElement = createBotMessageElement('Escribiendo...');
        chatBoxTyping.appendChild(botTypingMessageElement);
        chatBoxTyping.scrollTop = chatBoxTyping.scrollHeight;
        botTypingMessageElement.style.color = 'white';
        let dots = 0;
        typingTimeout = setInterval(function() {
            const typingText = 'Escribiendo' + '.'.repeat(dots);
            botTypingMessageElement.textContent = 'EduMentorBot: ' + typingText;
            dots = (dots + 1) % 4;
        }, 500); 
    }
    function createBotMessageElement(message) {
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'message bot-message';
        const boldText = document.createElement('b');
        boldText.textContent = 'EduMentorBot: ' + message;
        botMessageElement.appendChild(boldText);
        return botMessageElement;
    }
    function addBotMessage(message) {
        const botMessageElement = createBotMessageElement(message);
        botMessageElement.style.color = 'black';
        chatBox.appendChild(botMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendButton.addEventListener('click', sendMessage);
    clearButton.addEventListener('click', clearChatBox);

    userInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
            event.preventDefault(); 
        }
    });
});
