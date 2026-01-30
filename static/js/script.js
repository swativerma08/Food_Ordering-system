let cart = [];

// Load cart from local storage on load
document.addEventListener('DOMContentLoaded', () => {
    const savedCart = localStorage.getItem('savoria_cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartUI();
    }
});

function toggleCart() {
    const modal = document.getElementById('cart-modal');
    modal.classList.toggle('active');
}

function addToCart(id, name, price) {
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: id,
            name: name,
            price: price,
            quantity: 1
        });
    }
    
    saveAndUpdate();
    showNotification(`Added ${name} to cart`);
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    saveAndUpdate();
}

function updateQuantity(id, change) {
    const item = cart.find(item => item.id === id);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(id);
        } else {
            saveAndUpdate();
        }
    }
}

function saveAndUpdate() {
    localStorage.setItem('savoria_cart', JSON.stringify(cart));
    updateCartUI();
}

function updateCartUI() {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    
    // Update count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    // Update total price
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    cartTotal.textContent = `₹${total}`;
    
    // Update list
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p class="empty-cart-msg">Your cart is empty.</p>';
        return;
    }
    
    cartItemsContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <div class="quantity-controls">
                    <button onclick="updateQuantity(${item.id}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="updateQuantity(${item.id}, 1)">+</button>
                </div>
            </div>
            <div class="cart-item-price">
                <span class="cart-item-total">₹${item.price * item.quantity}</span>
                <button onclick="removeFromCart(${item.id})" class="remove-btn" style="color:red; background:none; border:none; margin-left:10px; cursor:pointer;"><i class="fas fa-trash"></i></button>
            </div>
        </div>
    `).join('');
}

async function placeOrder() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }
    
    const checkoutBtn = document.querySelector('.checkout-btn');
    const originalText = checkoutBtn.textContent;
    checkoutBtn.textContent = 'Processing...';
    checkoutBtn.disabled = true;
    
    try {
        const response = await fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ cart: cart }),
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`Order Placed Successfully! Total: ₹${result.total_amount}`);
            cart = [];
            saveAndUpdate();
            toggleCart();
        } else {
            alert('Failed to place order. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please check your connection.');
    } finally {
        checkoutBtn.textContent = originalText;
        checkoutBtn.disabled = false;
    }
}

function showNotification(msg) {
    // Simple toast notification
    const div = document.createElement('div');
    div.className = 'toast';
    div.textContent = msg;
    div.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--primary-color);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        animation: fadeIn 0.5s, fadeOut 0.5s 2.5s forwards;
        z-index: 3000;
    `;
    document.body.appendChild(div);
    
    setTimeout(() => {
        div.remove();
    }, 3000);
}


// Profile editing functions
function showEditProfileForm() {
    document.getElementById('edit-profile-form').style.display = 'block';
    document.getElementById('edit-profile-btn').style.display = 'none';
}

function hideEditProfileForm() {
    document.getElementById('edit-profile-form').style.display = 'none';
    document.getElementById('edit-profile-btn').style.display = 'inline-block';
}

async function updateProfile() {
    const userId = document.querySelector('#edit-profile-form input[name="user_id"]').value;
    const username = document.getElementById('edit-username').value;
    const fullName = document.getElementById('edit-full-name').value;
    const email = document.getElementById('edit-email').value;
    const phone = document.getElementById('edit-phone').value;
    const address = document.getElementById('edit-address').value;
    
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('username', username);
    formData.append('full_name', fullName);
    formData.append('email', email);
    formData.append('phone', phone);
    formData.append('address', address);
    
    // Debug logging
    console.log('Updating profile with:', {userId, username, fullName, email, phone, address});
    
    try {
        const response = await fetch('/update_profile', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        console.log('Server response:', result);
        
        if (result.success) {
            // Update the displayed values
            document.getElementById('edit-profile-btn').textContent = 'Welcome, ' + username;
            document.getElementById('full-name-display').textContent = fullName || 'Not provided';
            document.getElementById('email-display').textContent = email;
            document.getElementById('phone-display').textContent = phone || 'Not provided';
            document.getElementById('address-display').textContent = address || 'Not provided';
            
            // Hide the form and show success message
            hideEditProfileForm();
            showNotification('Profile updated successfully!');
        } else {
            showNotification('Error updating profile: ' + result.message);
        }
    } catch (error) {
        showNotification('Error updating profile: ' + error.message);
        console.error('Error:', error);
    }
}

// Add animation keyframes for toast via JS if not in CSS
const styleSheet = document.createElement("style");
styleSheet.innerText = `
@keyframes fadeOut {
   from { opacity: 1; }
   to { opacity: 0; }
}
.quantity-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 5px;
}
.quantity-controls button {
    background: #444;
    color: white;
    border: none;
    width: 25px;
    height: 25px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}
.quantity-controls button:hover {
    background: var(--primary-color);
}
.modal {
    display: none;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.4);
}
.modal-content {
    background-color: #fefefe;
    margin: 10% auto;
    padding: 20px;
    border: 1px solid #888;
    border-radius: 8px;
    width: 300px;
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}
.close {
    color: #aaa;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}
.close:hover,
.close:focus {
    color: black;
}
form div {
    margin-bottom: 15px;
}
form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}
form input[type="text"],
form input[type="email"],
form input[type="password"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}
form button {
    width: 100%;
    padding: 10px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
form button:hover {
    background-color: var(--secondary-color);
}
.message {
    margin: 10px 0;
    text-align: center;
}
`;
document.head.appendChild(styleSheet);


// Chatbot functionality
const chatbotToggle = document.getElementById('chatbotToggle');
const chatbotWindow = document.getElementById('chatbotWindow');
const chatbotMessages = document.getElementById('chatbotMessages');
const chatbotInput = document.getElementById('chatbotInput');
const chatbotSend = document.getElementById('chatbotSend');
const chatbotClose = document.getElementById('chatbotClose');

// Conversation state
let conversationState = {};

// Toggle chatbot window
chatbotToggle.addEventListener('click', function() {
    chatbotWindow.classList.add('active');
});

// Close chatbot window
chatbotClose.addEventListener('click', function() {
    chatbotWindow.classList.remove('active');
});

// Send message when clicking send button
chatbotSend.addEventListener('click', sendMessage);

// Send message when pressing Enter
chatbotInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const message = chatbotInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    chatbotInput.value = '';
    
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.textContent = 'Thinking...';
    chatbotMessages.appendChild(typingIndicator);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    
    try {
        const response = await fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_state: conversationState
            })
        });
        
        const data = await response.json();
        
        // Update conversation state
        conversationState = data.conversation_state;
        
        // Remove typing indicator
        typingIndicator.remove();
        
        // Add bot response
        addMessage(data.response, 'bot');
        
        // Add recommendations if present
        if (data.recommendations && data.recommendations.length > 0) {
            addRecommendations(data.recommendations);
        }
        
        // If the bot should ask another question, set up for next response
        if (data.should_ask_question && data.next_question_key) {
            // Clear input to prepare for next question
            chatbotInput.placeholder = 'Type your answer...';
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        typingIndicator.remove();
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender + '-message';
    messageDiv.textContent = text;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

function addRecommendations(recommendations) {
    const recommendationDiv = document.createElement('div');
    recommendationDiv.className = 'message bot-message recommendation-message';
    
    const title = document.createElement('div');
    title.textContent = 'Recommended for you:';
    title.style.fontWeight = 'bold';
    title.style.marginBottom = '10px';
    recommendationDiv.appendChild(title);
    
    recommendations.forEach(function(item) {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'recommendation-item';
        
        const infoDiv = document.createElement('div');
        infoDiv.className = 'recommendation-info';
        
        const nameSpan = document.createElement('div');
        nameSpan.className = 'recommendation-name';
        nameSpan.textContent = item.name;
        
        const categorySpan = document.createElement('div');
        categorySpan.className = 'recommendation-category';
        categorySpan.textContent = item.category + ' | \u20B9' + item.price;
        
        infoDiv.appendChild(nameSpan);
        infoDiv.appendChild(categorySpan);
        
        const priceDiv = document.createElement('div');
        priceDiv.className = 'recommendation-price';
        priceDiv.textContent = 'Confidence: ' + item.confidence + '%';
        
        itemDiv.appendChild(infoDiv);
        itemDiv.appendChild(priceDiv);
        
        // Add click event to add item to cart
        itemDiv.addEventListener('click', function() {
            addToCart(item.id, item.name, item.price);
            showNotification(item.name + ' added to cart!');
        });
        
        recommendationDiv.appendChild(itemDiv);
    });
    
    chatbotMessages.appendChild(recommendationDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

// Reset chatbot when opening
chatbotToggle.addEventListener('click', function() {
    if (!chatbotWindow.classList.contains('active')) {
        // Reset conversation when opening if it was closed
        resetChatbot();
    }
});

async function resetChatbot() {
    try {
        const response = await fetch('/chatbot/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        conversationState = data.conversation_state;
        
        // Clear chat messages except the welcome message
        chatbotMessages.innerHTML = '<div class="message bot-message">' + data.response + '</div>';
    } catch (error) {
        console.error('Error resetting chatbot:', error);
    }
}

// Close chatbot when clicking outside
window.addEventListener('click', function(e) {
    if (chatbotWindow.classList.contains('active') && 
        !chatbotWindow.contains(e.target) && 
        !chatbotToggle.contains(e.target)) {
        
        // Don't close if clicking on cart modal
        const cartModal = document.getElementById('cart-modal');
        if (!cartModal || !cartModal.contains(e.target)) {
            chatbotWindow.classList.remove('active');
        }
    }
});

// Initialize chatbot
resetChatbot();

// Theme Toggle Functionality
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-toggle i');
    
    if (body.classList.contains('light-theme')) {
        // Switch to dark theme
        body.classList.remove('light-theme');
        
        // Update icon to moon (dark mode)
        themeIcon.className = 'fas fa-moon';
        
        // Save theme preference
        localStorage.setItem('theme', 'dark');
    } else {
        // Switch to light theme
        body.classList.add('light-theme');
        
        // Update icon to sun (light mode)
        themeIcon.className = 'fas fa-sun';
        
        // Save theme preference
        localStorage.setItem('theme', 'light');
    }
}

// Check for saved theme preference or respect OS setting
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    if (savedTheme === 'light' || (!savedTheme && !prefersDarkScheme.matches)) {
        // Apply light theme
        document.body.classList.add('light-theme');
        document.querySelector('.theme-toggle i').className = 'fas fa-sun';
    } else {
        // Apply dark theme (default)
        document.querySelector('.theme-toggle i').className = 'fas fa-moon';
    }
});
