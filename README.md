# 🍕 Food Ordering System

A comprehensive web-based food ordering system built with Python Flask, featuring an intelligent AI-powered recommendation chatbot and complete order management functionality.

## 🌟 Key Features

### 🤖 AI-Powered Recommendation Chatbot
- **Smart Food Recommendations**: Interactive chatbot that learns your preferences
- **Personalized Suggestions**: Recommends dishes based on:
  - Vegetarian/Non-vegetarian preferences
  - Spice level tolerance (Mild/Medium/Spicy)
  - Meal timing (Breakfast/Lunch/Dinner/Snack)
  - Budget range considerations
  - Taste preferences (Light/Healthy/Rich/Filling)
- **Context-Aware**: Considers current time of day for appropriate recommendations
- **Conversational Interface**: Natural dialogue flow with acknowledgment recognition

### 🛒 Complete Ordering System
- **Browse Menu**: Comprehensive menu with multiple categories (Pizza, Main Course, Rice, Chinese, Desserts, Beverages)
- **Category Filtering**: Filter by meal type (Breakfast, Lunch, Dinner, Snacks, Beverages)
- **Shopping Cart**: Add/remove items with quantity management
- **Order Placement**: Secure order processing with confirmation
- **Order History**: Track all previous orders with timestamps

### 👤 User Management
- **Profile Management**: Update personal information (Name, Email, Phone, Address)
- **Persistent Data**: User preferences and order history maintained
- **Guest Mode**: Immediate access without registration

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Interactive Elements**: Smooth animations and real-time updates
- **Intuitive Navigation**: Clean, user-friendly interface
- **Visual Feedback**: Loading states and success/error notifications

## 🛠️ Technologies Used

### Backend
- **Python 3.x** - Core programming language
- **Flask 2.3.3** - Web framework
- **Werkzeug 2.3.7** - WSGI utility library
- **Jinja2 3.1.2** - Templating engine

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling and layout
- **JavaScript (ES6+)** - Client-side interactivity
- **AJAX** - Asynchronous server communication

### Data Management
- **JSON** - Data serialization
- **In-Memory Storage** - Session-based data persistence

## 📁 Project Structure
```
Food Ordering System/
├── app.py                 # Main Flask application with all routes
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template with common layout
│   ├── index.html        # Home page with chatbot
│   ├── menu.html         # Menu browsing page
│   └── profile.html      # User profile management
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── script.js     # Client-side JavaScript
├── .venv/                # Virtual environment
├── .git/                 # Git repository
├── GIT_SETUP_GUIDE.txt   # Git setup instructions
└── setup_git.py          # Git automation script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Clone or Navigate to Repository**
   ```bash
   cd "c:\Users\swati\Documents\Food ordering\Food ordering"
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv .venv
   # Activate on Windows
   .venv\Scripts\activate
   # Activate on macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   Open your browser and visit: `http://localhost:5000`

### Alternative Quick Start
If you have Python installed, you can run directly:
```bash
python app.py
```

## 🎯 Usage Guide

### Making Your First Order
1. **Start Chatting**: Interact with the AI chatbot on the homepage
2. **Share Preferences**: Answer questions about your food preferences
3. **Get Recommendations**: Receive personalized dish suggestions
4. **Browse Menu**: Explore all available items in the menu section
5. **Add to Cart**: Select items and quantities
6. **Place Order**: Complete your purchase
7. **Track Orders**: View order history in your profile

### Chatbot Conversation Flow
The chatbot will ask you these questions in sequence:
1. Vegetarian or Non-vegetarian preference?
2. Preferred spice level?
3. Current meal timing?
4. Budget range?
5. Taste preference (light/healthy/rich)?

After answering, you'll receive personalized recommendations!

## 📊 Menu Categories

| Category | Description | Sample Items |
|----------|-------------|--------------|
| **Pizza** | Classic and farmhouse varieties | Margherita, Farmhouse |
| **Main Course** | Hearty meals | Paneer Butter Masala |
| **Rice** | Biryanis and rice dishes | Hyderabadi Biryani |
| **Chinese** | Asian cuisine | Hakka Noodles |
| **Desserts** | Sweet endings | Choco Lava Cake |
| **Beverages** | Drinks and refreshments | Masala Chai, Filter Coffee |

## 🔧 API Endpoints

### Frontend Routes
- `GET /` - Homepage with chatbot
- `GET /menu` - Browse menu items
- `GET /profile` - User profile page
- `GET /menu/filter/<category>` - Filter menu by category

### API Routes
- `POST /chatbot` - Chatbot conversation endpoint
- `POST /chatbot/reset` - Reset chatbot conversation
- `POST /api/order` - Place food order
- `POST /update_profile` - Update user profile
- `POST /login` - User login
- `GET /logout` - User logout

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make Your Changes**
4. **Commit Your Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Areas for Contribution
- 🍽️ **Menu Expansion**: Add more food items and categories
- 🎨 **UI/UX Improvements**: Enhance the visual design
- 🤖 **AI Enhancement**: Improve recommendation algorithms
- 📱 **Mobile Optimization**: Better responsive design
- 💾 **Data Persistence**: Add database integration
- 🌍 **Localization**: Multi-language support

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋 Support

If you encounter any issues or have questions:
1. Check the existing [issues](https://github.com/swativerma08/Food_Ordering-system/issues)
2. Create a new issue with detailed information
3. Contact the maintainer: swativerma08

## 🚀 Future Enhancements

- [ ] User authentication system
- [ ] Payment gateway integration
- [ ] Real-time order tracking
- [ ] Admin dashboard
- [ ] Customer reviews and ratings
- [ ] Loyalty program
- [ ] Multi-restaurant support
- [ ] Delivery management system

---

<p align="center">Made with ❤️ for food lovers everywhere!</p>