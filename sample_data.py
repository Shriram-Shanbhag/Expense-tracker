#!/usr/bin/env python3
"""
Sample Data Generator for Personal Finance Tracker
This script adds sample expense data to test the application.
"""

import sqlite3
from datetime import datetime, timedelta
import random

def add_sample_data():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Check if we have any users
    cursor.execute('SELECT id FROM users LIMIT 1')
    user = cursor.fetchone()
    
    if not user:
        print("No users found. Please register a user first.")
        return
    
    user_id = user[0]
    
    # Sample categories
    categories = [
        'Food & Dining', 'Transportation', 'Shopping', 'Entertainment',
        'Healthcare', 'Utilities', 'Housing', 'Education', 'Travel',
        'Insurance', 'Investments', 'Gifts', 'Other'
    ]
    
    # Sample descriptions for each category
    descriptions = {
        'Food & Dining': ['Lunch at restaurant', 'Grocery shopping', 'Coffee', 'Dinner out', 'Fast food'],
        'Transportation': ['Gas', 'Uber ride', 'Bus fare', 'Parking', 'Car maintenance'],
        'Shopping': ['Clothes', 'Electronics', 'Books', 'Home supplies', 'Gifts'],
        'Entertainment': ['Movie tickets', 'Concert', 'Netflix subscription', 'Game purchase', 'Restaurant'],
        'Healthcare': ['Doctor visit', 'Medicine', 'Dental checkup', 'Gym membership', 'Vitamins'],
        'Utilities': ['Electricity bill', 'Water bill', 'Internet', 'Phone bill', 'Gas bill'],
        'Housing': ['Rent', 'Mortgage', 'Home repairs', 'Furniture', 'Cleaning supplies'],
        'Education': ['Books', 'Online course', 'Workshop', 'Software license', 'Conference'],
        'Travel': ['Flight tickets', 'Hotel', 'Car rental', 'Souvenirs', 'Travel insurance'],
        'Insurance': ['Car insurance', 'Health insurance', 'Life insurance', 'Home insurance'],
        'Investments': ['Stock purchase', 'Mutual fund', 'Retirement contribution', 'Crypto'],
        'Gifts': ['Birthday gift', 'Wedding gift', 'Holiday gift', 'Anniversary gift'],
        'Other': ['Miscellaneous', 'Emergency expense', 'Donation', 'Service fee']
    }
    
    # Generate expenses for the last 3 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    expenses_added = 0
    
    current_date = start_date
    while current_date <= end_date:
        # Add 1-3 expenses per day
        num_expenses = random.randint(1, 3)
        
        for _ in range(num_expenses):
            category = random.choice(categories)
            description = random.choice(descriptions[category])
            
            # Generate realistic amounts based on category
            if category == 'Food & Dining':
                amount = round(random.uniform(5, 50), 2)
            elif category == 'Transportation':
                amount = round(random.uniform(10, 100), 2)
            elif category == 'Shopping':
                amount = round(random.uniform(20, 200), 2)
            elif category == 'Entertainment':
                amount = round(random.uniform(15, 150), 2)
            elif category == 'Healthcare':
                amount = round(random.uniform(20, 300), 2)
            elif category == 'Utilities':
                amount = round(random.uniform(30, 200), 2)
            elif category == 'Housing':
                amount = round(random.uniform(50, 1000), 2)
            elif category == 'Education':
                amount = round(random.uniform(25, 500), 2)
            elif category == 'Travel':
                amount = round(random.uniform(100, 1000), 2)
            elif category == 'Insurance':
                amount = round(random.uniform(50, 300), 2)
            elif category == 'Investments':
                amount = round(random.uniform(100, 1000), 2)
            elif category == 'Gifts':
                amount = round(random.uniform(20, 200), 2)
            else:
                amount = round(random.uniform(10, 100), 2)
            
            cursor.execute('''
                INSERT INTO expenses (user_id, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, amount, category, description, current_date.strftime('%Y-%m-%d')))
            
            expenses_added += 1
        
        current_date += timedelta(days=1)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Added {expenses_added} sample expenses to the database!")
    print("You can now login and see the sample data in your dashboard.")

if __name__ == '__main__':
    add_sample_data() 