from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from datetime import datetime
import json
import random
from collections import defaultdict
import math
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key in production

# Database initialization
DATABASE = 'restaurant.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_summary TEXT,
            total_amount REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Check if default user exists, if not create one
    cursor.execute("SELECT * FROM users WHERE email = ?", ("guest@example.com",))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (username, full_name, email, phone, address) 
            VALUES (?, ?, ?, ?, ?)
        """, ("Guest User", "", "guest@example.com", "", ""))
    
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'full_name': user[2],
            'email': user[3],
            'phone': user[4],
            'address': user[5],
            'created_at': user[6],
            'updated_at': user[7]
        }
    return None


def update_user_profile(user_id, username, full_name, email, phone, address):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users SET username = ?, full_name = ?, email = ?, phone = ?, address = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (username, full_name, email, phone, address, user_id))
    
    conn.commit()
    conn.close()


def get_user_orders(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    orders = cursor.fetchall()
    conn.close()
    
    order_list = []
    for order in orders:
        order_list.append({
            'id': order[0],
            'user_id': order[1],
            'order_summary': json.loads(order[2]) if order[2] else [],
            'total_amount': order[3],
            'timestamp': order[4]
        })
    return order_list


def save_order(user_id, order_summary, total_amount):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO orders (user_id, order_summary, total_amount) 
        VALUES (?, ?, ?)
    """, (user_id, json.dumps(order_summary), total_amount))
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Initialize global variables
user_profile = get_user_by_email('guest@example.com') or {
    'id': 1,
    'username': 'Guest User',
    'full_name': '',
    'email': 'guest@example.com',
    'phone': '',
    'address': '',
    'created_at': str(datetime.now().date()),
    'updated_at': str(datetime.now().date())
}

order_history = get_user_orders(user_profile['id'])

# Mock Database - Menu Items
menu_items = [
    {
        "id": 1,
        "name": "Margherita Pizza",
        "category": "Pizza",
        "price": 299,
        "image": "pizza.png", # Placeholder, will be generated
        "description": "Classic delight with 100% Real Mozzarella Cheese."
    },
    {
        "id": 2,
        "name": "Farmhouse Pizza",
        "category": "Pizza",
        "price": 399,
        "image": "farmhouse_pizza.png",
        "description": "Delightful combination of onion, capsicum, tomato & grilled mushroom."
    },
    {
        "id": 3,
        "name": "Paneer Butter Masala",
        "category": "Main Course",
        "price": 250,
        "image": "paneer.png",
        "description": "Rich and creamy dish made with paneer, spices, onions, tomatoes, cashews and butter."
    },
    {
        "id": 4,
        "name": "Hyderabadi Biryani",
        "category": "Rice",
        "price": 350,
        "image": "biryani.png",
        "description": "Flavorful aromatic rice dish with perfectly cooked spices."
    },
    {
        "id": 5,
        "name": "Hakka Noodles",
        "category": "Chinese",
        "price": 180,
        "image": "noodles.png",
        "description": "Stir fried noodles with fresh vegetables and chinese sauces."
    },
    {
        "id": 6,
        "name": "Choco Lava Cake",
        "category": "Dessert",
        "price": 99,
        "image": "cake.png",
        "description": "Molten chocolate cake, perfect for a sweet ending."
    }
]

# Enhanced menu items with additional attributes for recommendation
menu_items_enhanced = [
    {
        "id": 1,
        "name": "Margherita Pizza",
        "category": "Pizza",
        "price": 299,
        "image": "pizza.png",
        "description": "Classic delight with 100% Real Mozzarella Cheese.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["lunch", "dinner"],
        "suitable_time": ["afternoon", "evening", "night"],
        "taste_profile": ["filling", "comfort"]
    },
    {
        "id": 2,
        "name": "Farmhouse Pizza",
        "category": "Pizza",
        "price": 399,
        "image": "farmhouse_pizza.png",
        "description": "Delightful combination of onion, capsicum, tomato & grilled mushroom.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["lunch", "dinner"],
        "suitable_time": ["afternoon", "evening", "night"],
        "taste_profile": ["filling", "comfort"]
    },
    {
        "id": 3,
        "name": "Paneer Butter Masala",
        "category": "Main Course",
        "price": 250,
        "image": "paneer.png",
        "description": "Rich and creamy dish made with paneer, spices, onions, tomatoes, cashews and butter.",
        "veg": True,
        "spice_level": "medium",
        "meal_type": ["lunch", "dinner"],
        "suitable_time": ["afternoon", "evening", "night"],
        "taste_profile": ["rich", "filling"]
    },
    {
        "id": 4,
        "name": "Hyderabadi Biryani",
        "category": "Rice",
        "price": 350,
        "image": "biryani.png",
        "description": "Flavorful aromatic rice dish with perfectly cooked spices.",
        "veg": False,
        "spice_level": "medium",
        "meal_type": ["lunch", "dinner"],
        "suitable_time": ["afternoon", "evening", "night"],
        "taste_profile": ["rich", "filling"]
    },
    {
        "id": 5,
        "name": "Hakka Noodles",
        "category": "Chinese",
        "price": 180,
        "image": "noodles.png",
        "description": "Stir fried noodles with fresh vegetables and chinese sauces.",
        "veg": True,
        "spice_level": "medium",
        "meal_type": ["lunch", "dinner", "snack"],
        "suitable_time": ["afternoon", "evening"],
        "taste_profile": ["filling", "moderate"]
    },
    {
        "id": 6,
        "name": "Choco Lava Cake",
        "category": "Dessert",
        "price": 99,
        "image": "cake.png",
        "description": "Molten chocolate cake, perfect for a sweet ending.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["snack", "dessert"],
        "suitable_time": ["afternoon", "evening"],
        "taste_profile": ["sweet", "rich"]
    },
    {
        "id": 7,
        "name": "Masala Chai",
        "category": "Beverages",
        "price": 30,
        "image": "chai.jpg",
        "description": "Authentic Indian tea with spices and milk.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["beverage"],
        "suitable_time": ["morning", "afternoon"],
        "taste_profile": ["warm", "comfort"]
    },
    {
        "id": 8,
        "name": "Fresh Lime Water",
        "category": "Beverages",
        "price": 45,
        "image": "limewater.jpg",
        "description": "Refreshing lime water with salt and mint.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["beverage", "snack"],
        "suitable_time": ["afternoon", "evening"],
        "taste_profile": ["fresh", "light"]
    },
    {
        "id": 9,
        "name": "Filter Coffee",
        "category": "Beverages",
        "price": 35,
        "image": "coffee.jpg",
        "description": "Strong South Indian filter coffee served in traditional tumbler.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["beverage", "breakfast"],
        "suitable_time": ["morning"],
        "taste_profile": ["strong", "energizing"]
    },
    {
        "id": 10,
        "name": "Idli Sambar",
        "category": "Breakfast",
        "price": 80,
        "image": "idli.jpg",
        "description": "Soft and fluffy steamed rice cakes served with authentic South Indian sambar and coconut chutney.",
        "veg": True,
        "spice_level": "medium",
        "meal_type": ["breakfast"],
        "suitable_time": ["morning"],
        "taste_profile": ["savory", "healthy"]
    },
    {
        "id": 11,
        "name": "Masala Dosa",
        "category": "Breakfast",
        "price": 120,
        "image": "dosa.jpg",
        "description": "Crispy fermented crepe filled with spiced potato filling, served with sambar and chutneys.",
        "veg": True,
        "spice_level": "medium",
        "meal_type": ["breakfast"],
        "suitable_time": ["morning"],
        "taste_profile": ["crispy", "spicy"]
    },
    {
        "id": 12,
        "name": "Upma",
        "category": "Breakfast",
        "price": 70,
        "image": "upma.jpg",
        "description": "Semolina porridge cooked with vegetables and spices, a perfect healthy breakfast option.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["breakfast"],
        "suitable_time": ["morning"],
        "taste_profile": ["healthy", "light"]
    },
    {
        "id": 13,
        "name": "Poha",
        "category": "Breakfast",
        "price": 60,
        "image": "poha.jpg",
        "description": "Flattened rice flakes cooked with onions, mustard seeds, and turmeric, garnished with coriander.",
        "veg": True,
        "spice_level": "mild",
        "meal_type": ["breakfast"],
        "suitable_time": ["morning"],
        "taste_profile": ["light", "traditional"]
    },
    {
        "id": 14,
        "name": "Vada Sambar",
        "category": "Breakfast",
        "price": 90,
        "image": "vada.jpg",
        "description": "Deep-fried savory doughnuts made from urad dal batter, served with tangy sambar.",
        "veg": True,
        "spice_level": "medium",
        "meal_type": ["breakfast"],
        "suitable_time": ["morning"],
        "taste_profile": ["crispy", "savory"]
    }
]


import re
from collections import Counter
import math


class ChatbotRecommender:
    def __init__(self, menu_items):
        self.menu_items = menu_items
        self.feedback_data = []  # Store feedback for learning
        self.user_interaction_history = {}  # Track user preferences over time
        
    def preprocess_text(self, text):
        """Preprocess user input for NLP analysis"""
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # Tokenize
        tokens = text.split()
        return tokens
    
    def detect_intent(self, user_input):
        """Detect user intent using pattern matching and keyword analysis"""
        user_input_lower = user_input.lower()
        
        # Define intent patterns
        intents = {
            'greeting': [r'hello', r'hi', r'hey', r'good morning', r'good afternoon', r'good evening'],
            'food_recommendation': [r'mood for', r'craving', r'want to eat', r'looking for', r'suggest', r'recommend', r'food', r'eat', r'hungry', r'what should i eat', r'what to order'],
            'order_status': [r'order', r'status', r'delivery', r'where is', r'when will', r'arrive', r'pickup', r'eta', r'expected time'],
            'menu_inquiry': [r'menu', r'options', r'available', r'what do you have', r'list items', r'what is there'],
            'pricing': [r'price', r'cost', r'how much', r'budget', r'expensive', r'cheap', r'rate', r'rates'],
            'feedback': [r'good', r'bad', r'tasty', r'yummy', r'awful', r'love', r'hate', r'excellent', r'amazing', r'perfect', r'fantastic', r'terrific'],
            'bye': [r'thank you', r'thanks', r'bye', r'goodbye', r'exit', r'quit', r'end']
        }
        
        detected_intent = None
        max_score = 0
        
        for intent, patterns in intents.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    score += 1
            if score > max_score:
                max_score = score
                detected_intent = intent
        
        return detected_intent if detected_intent else 'unknown'
    
    def get_current_time_period(self):
        """Determine the time of day based on current hour"""
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return "morning"
        elif 12 <= current_hour < 15:
            return "afternoon"
        elif 15 <= current_hour < 18:
            return "evening"
        else:
            return "night"
    
    def calculate_similarity_score(self, user_preferences, menu_item):
        """Calculate similarity score between user preferences and menu item"""
        score = 0
        max_score = 0
        
        # Veg preference match
        if "food_preference" in user_preferences:
            pref_veg = user_preferences["food_preference"].lower() == "veg"
            if pref_veg == menu_item["veg"]:
                score += 20  # High weight for dietary preference
            max_score += 20
        
        # Spice level match
        if "spice_level" in user_preferences:
            if user_preferences["spice_level"].lower() == menu_item["spice_level"].lower():
                score += 15
            max_score += 15
        
        # Meal type match
        if "meal_type" in user_preferences:
            meal_type = user_preferences["meal_type"].lower()
            # Handle different meal type variations
            if "breakfast" in meal_type:
                meal_type = "breakfast"
            elif "lunch" in meal_type:
                meal_type = "lunch"
            elif "dinner" in meal_type:
                meal_type = "dinner"
            elif "snack" in meal_type or "anytime" in meal_type:
                meal_type = "snack"
            elif "dessert" in meal_type:
                meal_type = "dessert"
            elif "beverage" in meal_type:
                meal_type = "beverage"
            else:
                # Default to lunch/dinner if not clearly identified
                meal_type = "lunch"  # default
            
            if meal_type in menu_item["meal_type"]:
                score += 15
            max_score += 15
        
        # Time of day match
        current_time = self.get_current_time_period()
        if current_time in menu_item["suitable_time"]:
            score += 10
        max_score += 10
        
        # Budget match
        if "budget_range" in user_preferences:
            budget_input = user_preferences["budget_range"].lower()
            price = menu_item["price"]
            max_score += 20  # Budget matching is important
            
            # Handle different budget input formats
            if "low" in budget_input or "under" in budget_input or "less" in budget_input:
                budget = "low"
            elif "high" in budget_input or "above" in budget_input or "more" in budget_input:
                budget = "high"
            elif "medium" in budget_input or "mid" in budget_input:
                budget = "medium"
            else:
                # Try to extract numeric range
                budget = "medium"  # default
                if any(char.isdigit() for char in budget_input):
                    try:
                        # Extract numbers from the budget range
                        nums = [int(x) for x in re.findall(r'\d+', budget_input)]
                        if nums:
                            avg_budget = sum(nums) // len(nums)
                            if avg_budget <= 200:
                                budget = "low"
                            elif avg_budget <= 500:
                                budget = "medium"
                            else:
                                budget = "high"
                    except:
                        budget = "medium"  # fallback
            
            if budget == "low" and price <= 200:
                score += 20
            elif budget == "medium" and 200 < price <= 350:
                score += 20
            elif budget == "high" and price > 350:
                score += 20
            elif budget == "low" and price > 200:
                score += max(0, 20 - (price - 200) // 20)  # Partial score for close budget
            elif budget == "medium" and (price <= 200 or price > 350):
                score += max(0, 10 - abs(price - 275) // 30)  # Partial score
            elif budget == "high" and price <= 350:
                score += max(0, 10 - (350 - price) // 40)  # Partial score
        else:
            max_score += 20  # Budget is important but optional
        
        # Taste preference match
        if "taste_preference" in user_preferences:
            taste = user_preferences["taste_preference"].lower()
            # Match taste preference to taste_profile in menu items
            if "light" in taste:
                if "light" in menu_item.get("taste_profile", []):
                    score += 15
                # Light foods might be salads, soups, etc.
                elif menu_item["category"].lower() in ["salad", "soup", "starter", "snack"]:
                    score += 10
                max_score += 15
            elif "healthy" in taste:
                # Healthy foods could be grilled, steamed, etc.
                if "healthy" in menu_item.get("taste_profile", []):
                    score += 15
                score += 5  # Add some score for any item (general healthy assumption)
                max_score += 15
            elif "rich" in taste or "filling" in taste:
                if "rich" in menu_item.get("taste_profile", []) or "filling" in menu_item.get("taste_profile", []):
                    score += 15
                elif menu_item["category"].lower() in ["main course", "rice", "biryani"]:
                    score += 10
                max_score += 15
            elif "sweet" in taste:
                if "sweet" in menu_item.get("taste_profile", []):
                    score += 15
                elif menu_item["category"].lower() in ["dessert"]:
                    score += 10
                max_score += 15
            else:
                max_score += 15  # Taste preference is optional
        else:
            max_score += 15  # Taste preference is optional
        
        # Add historical feedback adjustment
        avg_feedback = self.get_item_feedback_score(menu_item['id'])
        if avg_feedback > 0:
            score *= (1 + avg_feedback * 0.1)  # Boost score based on positive feedback
        elif avg_feedback < 0:
            score *= (1 + avg_feedback * 0.1)  # Reduce score based on negative feedback
        
        # Calculate normalized score
        if max_score > 0:
            return (score / max_score) * 100
        else:
            return 0
    
    def calculate_nlp_similarity(self, user_input, item):
        """Calculate similarity between user input and menu item using NLP techniques"""
        user_tokens = set(self.preprocess_text(user_input))
        item_features = set()
        
        # Add various features of the item to the feature set
        if 'name' in item:
            item_features.update(self.preprocess_text(item['name']))
        if 'category' in item:
            item_features.update(self.preprocess_text(item['category']))
        if 'description' in item:
            item_features.update(self.preprocess_text(item['description']))
        if 'taste_profile' in item:
            for taste in item['taste_profile']:
                item_features.update(self.preprocess_text(str(taste)))
        if 'meal_type' in item:
            for meal in item['meal_type']:
                item_features.update(self.preprocess_text(str(meal)))
        
        # Calculate Jaccard similarity
        intersection = len(user_tokens.intersection(item_features))
        union = len(user_tokens.union(item_features))
        
        if union == 0:
            return 0
        
        return intersection / union
    
    def recommend_items(self, user_preferences, num_recommendations=3):
        """Recommend menu items based on user preferences"""
        # Calculate scores for all items
        scored_items = []
        
        for item in self.menu_items:
            score = self.calculate_similarity_score(user_preferences, item)
            
            # If user provided initial input, calculate NLP similarity
            if 'initial_input' in user_preferences:
                nlp_score = self.calculate_nlp_similarity(user_preferences['initial_input'], item) * 50  # Weight NLP score
                score = (score + nlp_score) / 2  # Average the scores
            
            scored_items.append({
                "item": item,
                "score": score
            })

        # Sort by score in descending order
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top recommendations
        recommendations = []
        for i, scored_item in enumerate(scored_items):
            if i >= num_recommendations:
                break
            if scored_item["score"] > 0:  # Only include items with positive score
                recommendations.append(scored_item)
        
        return recommendations
    
    def get_next_question(self, conversation_state):
        """Determine the next question to ask based on conversation state"""
        # Detect intent from the initial user message if not already detected
        if 'intent' not in conversation_state and 'initial_input' in conversation_state:
            detected_intent = self.detect_intent(conversation_state['initial_input'])
            conversation_state['intent'] = detected_intent
        
        # Handle different intents
        intent = conversation_state.get('intent', 'food_recommendation')
        
        if intent == 'order_status':
            # If user is asking about order status, provide appropriate response
            return 'I can help with order status. Could you please provide your order ID?', 'order_id'
        elif intent == 'menu_inquiry':
            # If user is asking about menu, provide menu information
            return f'We offer a variety of cuisines including {len(self.menu_items)} delicious items. Would you like me to recommend something?', 'menu_exploration'
        elif intent == 'pricing':
            # If user is asking about prices, provide pricing information
            avg_price = sum(item["price"] for item in self.menu_items) / len(self.menu_items)
            return f'Our menu items range from ₹{min(item["price"] for item in self.menu_items)} to ₹{max(item["price"] for item in self.menu_items)}, with an average of ₹{round(avg_price)}. What type of food are you interested in?', 'price_exploration'
        elif intent == 'food_recommendation':
            # Standard food recommendation flow
            questions = [
                {"key": "food_preference", "question": "Do you prefer vegetarian or non-vegetarian food?"},
                {"key": "spice_level", "question": "How spicy do you like your food? (Mild / Medium / Spicy)"},
                {"key": "meal_type", "question": "What are you looking for right now — breakfast, lunch, dinner, snacks, or beverages?"},
                {"key": "budget_range", "question": "What is your preferred budget range (in ₹)?"},
                {"key": "taste_preference", "question": "Do you prefer something light, healthy, or rich and filling?"}
            ]
            
            for q in questions:
                if q["key"] not in conversation_state or conversation_state[q["key"]] is None:
                    return q["question"], q["key"]
        
        # If all preferences are collected, provide recommendations
        return None, None
    
    def get_item_feedback_score(self, item_id):
        """Calculate average feedback score for an item"""
        item_feedback = [fb for fb in self.feedback_data if fb['item_id'] == item_id]
        if not item_feedback:
            return 0
        
        total_score = sum(fb['score'] for fb in item_feedback)
        return total_score / len(item_feedback)
    
    def record_feedback(self, item_id, user_rating):
        """Record user feedback for learning"""
        # Convert user rating to numerical score
        if isinstance(user_rating, str):
            if 'positive' in user_rating.lower() or 'good' in user_rating.lower() or 'like' in user_rating.lower() or 'excellent' in user_rating.lower() or 'amazing' in user_rating.lower():
                score = 1
            elif 'negative' in user_rating.lower() or 'bad' in user_rating.lower() or 'dislike' in user_rating.lower() or 'terrible' in user_rating.lower() or 'awful' in user_rating.lower():
                score = -1
            else:
                score = 0
        else:
            score = user_rating
        
        self.feedback_data.append({
            'item_id': item_id,
            'score': score,
            'timestamp': datetime.now()
        })
        
        # Keep only recent feedback (last 100 entries)
        if len(self.feedback_data) > 100:
            self.feedback_data = self.feedback_data[-100:]
    
    def learn_from_interaction(self, user_id, preferences, selected_items):
        """Learn from user interactions to improve future recommendations"""
        if user_id not in self.user_interaction_history:
            self.user_interaction_history[user_id] = {
                'preferences': [],
                'selected_items': [],
                'feedback': []
            }
        
        self.user_interaction_history[user_id]['preferences'].append(preferences.copy())
        self.user_interaction_history[user_id]['selected_items'].extend(selected_items)
    
    def get_personalized_recommendations(self, user_id, current_preferences):
        """Provide personalized recommendations based on user history"""
        if user_id not in self.user_interaction_history:
            # If no history, use standard recommendation
            return self.recommend_items(current_preferences)
        
        # Combine current preferences with historical preferences
        user_history = self.user_interaction_history[user_id]
        historical_prefs = user_history['preferences']
        
        # Create a weighted combination of current and historical preferences
        combined_preferences = current_preferences.copy()
        
        # Add weights based on historical data
        for hist_pref in historical_prefs[-3:]:  # Consider last 3 interactions
            for key, value in hist_pref.items():
                if key not in combined_preferences:
                    combined_preferences[key] = value

        return self.recommend_items(combined_preferences)

# Initialize the recommender
recommender = ChatbotRecommender(menu_items_enhanced)

@app.route('/')
def home():
    return render_template('index.html', user=user_profile, orders=order_history)

@app.route('/profile')
def profile():
    return render_template('profile.html', user=user_profile, orders=order_history)

# Global variable to hold current user profile
user_profile = None

@app.route('/update_profile', methods=['POST'])
def update_profile():
    global user_profile
    # Update the user profile in database
    user_id = request.form.get('user_id', user_profile['id'] if user_profile else 1)
    username = request.form.get('username', user_profile['username'] if user_profile else 'Guest User')
    full_name = request.form.get('full_name', user_profile['full_name'] if user_profile else '')
    email = request.form.get('email', user_profile['email'] if user_profile else 'guest@example.com')
    phone = request.form.get('phone', user_profile['phone'] if user_profile else '')
    address = request.form.get('address', user_profile['address'] if user_profile else '')
    
    try:
        update_user_profile(user_id, username, full_name, email, phone, address)
        
        # Refresh the user profile from database
        refreshed_user = get_user_by_email(email) or get_user_by_email('guest@example.com')
        user_profile = refreshed_user
        
        print(f"Profile updated: {user_profile}")  # Debug
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return jsonify({'success': False, 'message': 'Error updating profile'})

# No authentication needed - these are just for compatibility
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('index.html', user=user_profile, orders=order_history)

@app.route('/login', methods=['POST'])
def login():
    return jsonify({'success': True, 'message': 'Login successful'})

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/menu')
def menu():
    # Get the category from query parameters
    category = request.args.get('category', 'all')
    
    if category == 'all':
        selected_menu = menu_items
    else:
        # Special handling for each category based on actual data
        if category == 'breakfast':
            # Items suitable for breakfast
            selected_menu = [item for item in menu_items_enhanced if 'breakfast' in item.get('meal_type', [])]
            # If no specific breakfast items found, include beverages that are also suitable for breakfast
            if not selected_menu:
                selected_menu = [item for item in menu_items_enhanced if 'breakfast' in item.get('meal_type', []) or ('beverage' in item.get('meal_type', []) and 'morning' in item.get('suitable_time', []))]
        elif category == 'lunch':
            # Items suitable for lunch
            selected_menu = [item for item in menu_items_enhanced if 'lunch' in item.get('meal_type', [])]
        elif category == 'dinner':
            # Items suitable for dinner
            selected_menu = [item for item in menu_items_enhanced if 'dinner' in item.get('meal_type', [])]
        elif category == 'snacks':
            # Items suitable as snacks
            selected_menu = [item for item in menu_items_enhanced if 'snack' in item.get('meal_type', [])]
        elif category == 'beverages':
            # Items categorized as beverages
            selected_menu = [item for item in menu_items_enhanced if 'beverage' in item.get('meal_type', [])]
        else:
            # Default case - return all items
            selected_menu = menu_items
    
    return render_template('menu.html', menu=selected_menu)


@app.route('/menu/filter/<category>')
def filter_menu(category):
    # Filter menu items based on category
    if category == 'all':
        filtered_items = menu_items_enhanced
    else:
        # Special handling for each category based on actual data
        if category == 'breakfast':
            # Items suitable for breakfast
            filtered_items = [item for item in menu_items_enhanced if 'breakfast' in item.get('meal_type', [])]
            # If no specific breakfast items found, include beverages that are also suitable for breakfast
            if not filtered_items:
                filtered_items = [item for item in menu_items_enhanced if 'breakfast' in item.get('meal_type', []) or ('beverage' in item.get('meal_type', []) and 'morning' in item.get('suitable_time', []))]
        elif category == 'lunch':
            # Items suitable for lunch
            filtered_items = [item for item in menu_items_enhanced if 'lunch' in item.get('meal_type', [])]
        elif category == 'dinner':
            # Items suitable for dinner
            filtered_items = [item for item in menu_items_enhanced if 'dinner' in item.get('meal_type', [])]
        elif category == 'snacks':
            # Items suitable as snacks
            filtered_items = [item for item in menu_items_enhanced if 'snack' in item.get('meal_type', [])]
        elif category == 'beverages':
            # Items categorized as beverages
            filtered_items = [item for item in menu_items_enhanced if 'beverage' in item.get('meal_type', [])]
        else:
            # Default case - return all items
            filtered_items = menu_items_enhanced
    
    return jsonify({'success': True, 'items': filtered_items})

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    data = request.json
    user_message = data.get('message', '').strip()
    conversation_state = data.get('conversation_state', {})
    
    # Store initial input if this is the first message
    if 'initial_input' not in conversation_state and user_message:
        conversation_state['initial_input'] = user_message
    
    # Define acknowledgment keywords that indicate user is done
    ack_keywords = ['ok', 'okay', 'thank you', 'thanks', 'perfect', 'great', 'awesome', 'excellent', 'done', 'bye', 'goodbye', "that's great", 'sounds good', 'exactly', 'yes', 'yep', 'sure']
    
    # Get next question based on conversation state
    next_question, question_key = recommender.get_next_question(conversation_state)
    
    # Check if user is acknowledging recommendations (not asking a new question)
    # If we have already provided recommendations and user says thanks/ok
    if user_message and not next_question and any(keyword in user_message.lower() for keyword in ack_keywords):
        # User is acknowledging the recommendations
        response_text = "You're welcome! Enjoy your meal! 😊"
        return jsonify({
            'response': response_text,
            'conversation_state': conversation_state,
            'should_ask_question': False
        })
    
    if next_question is None:
        # All preferences collected, provide recommendations
        recommendations = recommender.recommend_items(conversation_state)
        
        # Format recommendations for response
        formatted_recs = []
        for rec in recommendations:
            item = rec['item']
            formatted_recs.append({
                'id': item['id'],
                'name': item['name'],
                'category': item['category'],
                'price': item['price'],
                'description': item['description'],
                'veg': item['veg'],
                'confidence': round(rec['score'], 2)
            })
        
        return jsonify({
            'response': 'Based on your preferences, I recommend these items:',
            'recommendations': formatted_recs,
            'conversation_state': conversation_state,
            'should_ask_question': False
        })
    
    # Handle initial greetings if conversation hasn't started properly
    greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'help', 'start', 'begin']
    
    if user_message and next_question and question_key:
        # Check if this is likely a greeting at the start
        if not conversation_state and any(keyword in user_message.lower() for keyword in greeting_keywords):
            # Just return the first question without storing the greeting as an answer
            return jsonify({
                'response': next_question,
                'conversation_state': conversation_state,
                'should_ask_question': True,
                'next_question_key': question_key
            })
        else:
            # Store user's response
            conversation_state[question_key] = user_message
            
            # Get next question
            next_question, next_key = recommender.get_next_question(conversation_state)
            
            if next_question:
                return jsonify({
                    'response': next_question,
                    'conversation_state': conversation_state,
                    'should_ask_question': True,
                    'next_question_key': next_key
                })
            else:
                # All preferences collected
                recommendations = recommender.recommend_items(conversation_state)
                
                # Format recommendations for response
                formatted_recs = []
                for rec in recommendations:
                    item = rec['item']
                    formatted_recs.append({
                        'id': item['id'],
                        'name': item['name'],
                        'category': item['category'],
                        'price': item['price'],
                        'description': item['description'],
                        'veg': item['veg'],
                        'confidence': round(rec['score'], 2)
                    })
                
                return jsonify({
                    'response': 'Based on your preferences, I recommend these items:',
                    'recommendations': formatted_recs,
                    'conversation_state': conversation_state,
                    'should_ask_question': False
                })
    
    # If no specific user response or no next question, return the next question
    if next_question:
        return jsonify({
            'response': next_question,
            'conversation_state': conversation_state,
            'should_ask_question': True,
            'next_question_key': question_key
        })
    else:
        return jsonify({
            'response': 'Hello! How can I help you today?',
            'conversation_state': {},
            'should_ask_question': True,
            'next_question_key': None
        })

@app.route('/chatbot/reset', methods=['POST'])
def reset_chatbot():
    return jsonify({
        'response': 'Chatbot has been reset. How can I help you today?',
        'conversation_state': {},
        'should_ask_question': True
    })

# Global variable to hold current order history
order_history = []

@app.route('/api/order', methods=['POST'])
def place_order():
    global order_history
    data = request.json
    cart = data.get('cart', [])
    
    total_price = 0
    order_summary = []
    
    # Simple server-side validation/calculation
    for item in cart:
        item_id = item.get('id')
        quantity = item.get('quantity', 0)
        
        # Find product in db
        product = next((p for p in menu_items if p['id'] == item_id), None)
        
        if product and quantity > 0:
            item_total = product['price'] * quantity
            total_price += item_total
            order_summary.append({
                "name": product['name'],
                "quantity": quantity,
                "price": product['price'],
                "total": item_total
            })
    
    # Save order to the database
    save_order(user_profile['id'], order_summary, total_price)
    
    # Update the order history
    user_orders = get_user_orders(user_profile['id'] if user_profile else 1)
    order_history = user_orders
    
    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "order_summary": order_summary,
        "total_amount": total_price
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
