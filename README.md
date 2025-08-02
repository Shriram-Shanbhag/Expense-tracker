# Personal Finance Tracker

A beautiful and comprehensive web application for tracking personal expenses with analytics and insights.

## Features

- 🔐 **User Authentication**: Secure login and registration system
- 📊 **Dashboard**: Overview of current month's spending with key metrics
- ➕ **Add Expenses**: Easy expense entry with category selection
- 📈 **Analytics**: Interactive charts and spending insights
- 📅 **History**: Complete expense history for the last 12 months
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 💾 **SQLite Database**: No complex setup required
- 📤 **Data Export**: Export your expense data to CSV

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

### First Time Setup

1. Click "Register" to create your account
2. Login with your credentials
3. Start adding your expenses!

## Usage Guide

### Dashboard
- View current month's total spending
- See category breakdown with percentages
- Check recent transactions
- Quick access to all features

### Adding Expenses
- Click "Add Expense" or use the quick add buttons
- Select from predefined categories:
  - Food & Dining
  - Transportation
  - Shopping
  - Entertainment
  - Healthcare
  - Utilities
  - Housing
  - Education
  - Travel
  - Insurance
  - Investments
  - Gifts
  - Other

### Analytics
- **Category Breakdown**: Pie chart showing spending by category
- **Daily Trend**: Line chart of daily spending patterns
- **Monthly Comparison**: Bar chart comparing last 6 months
- **Spending Insights**: AI-powered recommendations

### History
- View all expenses from the last 12 months
- Grouped by month for easy navigation
- Monthly summaries with statistics
- Yearly overview

## Database

The application uses SQLite, which means:
- No database server required
- Data is stored locally in `finance.db`
- Automatic database creation on first run
- Easy backup (just copy the .db file)

## File Structure

```
personal-finance-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── finance.db            # SQLite database (created automatically)
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # Main dashboard
    ├── add_expense.html  # Add expense form
    ├── history.html      # Expense history
    └── analytics.html    # Analytics and charts
```

## Security Features

- Password hashing using Werkzeug
- Session management with Flask-Login
- SQL injection protection
- CSRF protection

## Customization

### Adding New Categories
Edit the `add_expense.html` template and add new options to the category select dropdown.

### Changing Colors
Modify the CSS in `base.html` to change the color scheme.

### Database Schema
The database has two main tables:
- `users`: User accounts and authentication
- `expenses`: Expense records with user relationships

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Change the port in `app.py` line: `app.run(debug=True, host='0.0.0.0', port=5001)`

2. **Database errors**:
   - Delete `finance.db` and restart the application

3. **Import errors**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

### Getting Help

If you encounter any issues:
1. Check that Python 3.7+ is installed
2. Verify all dependencies are installed
3. Ensure no other application is using port 5000
4. Check the console for error messages

## Features in Detail

### Smart Analytics
- Automatic spending pattern recognition
- Budget recommendations based on spending habits
- Visual charts for easy understanding
- Export functionality for external analysis

### User Experience
- Modern, responsive design
- Intuitive navigation
- Quick add buttons for common expenses
- Real-time data updates

### Data Management
- Secure user authentication
- Individual user data isolation
- Easy data export
- Automatic backup through SQLite

## Future Enhancements

Potential features for future versions:
- Budget setting and tracking
- Recurring expense management
- Income tracking
- Multiple currency support
- Mobile app version
- Cloud backup integration

## License

This project is open source and available under the MIT License.

---

**Happy Budgeting! 💰** 