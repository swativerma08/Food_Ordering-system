from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from datetime import datetime
import json
import random
from collections import defaultdict
import math

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key in production

# Mock Database - Single User Profile
user_profile = {
    'username': 'Guest User',
    'full_name': '',
    'email': 'guest@example.com',
    'phone': '',
    'address': '',
    'created_at': str(datetime.now().date())
}

# Mock Database - Order History
order_history = []

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
    }
]


class ChatbotRecommender:
    def __init__(self, menu_items):
        self.menu_items = menu_items
        
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
                        import re
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
        
        # Calculate normalized score
        if max_score > 0:
            return (score / max_score) * 100
        else:
            return 0
    
    def recommend_items(self, user_preferences, num_recommendations=3):
        """Recommend menu items based on user preferences"""
        # Calculate scores for all items
        scored_items = []
        for item in self.menu_items:
            score = self.calculate_similarity_score(user_preferences, item)
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
        questions = [
            {"key": "food_preference", "question": "Do you prefer vegetarian or non-vegetarian food?"},
            {"key": "spice_level", "question": "How spicy do you like your food? (Mild / Medium / Spicy)"},
            {"key": "meal_type", "question": "What are you looking for right now — breakfast, lunch, dinner, or a snack?"},
            {"key": "budget_range", "question": "What is your preferred budget range (in ₹)?"},
            {"key": "taste_preference", "question": "Do you prefer something light, healthy, or rich and filling?"}
        ]
        
        for q in questions:
            if q["key"] not in conversation_state or conversation_state[q["key"]] is None:
                return q["question"], q["key"]
        
        # If all preferences are collected, provide recommendations
        return None, None

# Initialize the recommender
recommender = ChatbotRecommender(menu_items_enhanced)

@app.route('/')
def home():
    return render_template('index.html', user=user_profile, orders=order_history)

@app.route('/profile')
def profile():
    return render_template('profile.html', user=user_profile, orders=order_history)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Update the single user profile
    user_profile['username'] = request.form.get('username', user_profile['username'])
    user_profile['full_name'] = request.form.get('full_name', user_profile['full_name'])
    user_profile['email'] = request.form.get('email', user_profile['email'])
    user_profile['phone'] = request.form.get('phone', '')
    user_profile['address'] = request.form.get('address', '')
    
    print(f"Profile updated: {user_profile}")  # Debug
    
    return jsonify({'success': True, 'message': 'Profile updated successfully'})

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
    return render_template('menu.html', menu=menu_items)


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
    user_message = data.get('message', '').strip().lower()
    conversation_state = data.get('conversation_state', {})
    
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

@app.route('/chatbot/reset', methods=['POST'])
def reset_chatbot():
    return jsonify({
        'response': 'Chatbot has been reset. How can I help you today?',
        'conversation_state': {},
        'should_ask_question': True
    })

@app.route('/api/order', methods=['POST'])
def place_order():
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
    
    # Save order to the order history
    order_data = {
        'order_summary': order_summary,
        'total_amount': total_price,
        'timestamp': str(datetime.now())
    }
    order_history.append(order_data)
    
    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "order_summary": order_summary,
        "total_amount": total_price
    })


