import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """Handle all database operations"""
    
    def __init__(self, db_name="app.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to database"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
    
    def create_conversations_table(self):
        """Create table for storing conversations"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT
                )
            """)
            self.connection.commit()
            logger.info("Conversations table created/verified")
        except sqlite3.Error as e:
            logger.error(f"Error creating table: {str(e)}")
            raise
    
    def create_expenses_table(self):
        """Create table for storing expenses"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    category TEXT,
                    user_id TEXT
                )
            """)
            self.connection.commit()
            logger.info("Expenses table created/verified")
        except sqlite3.Error as e:
            logger.error(f"Error creating table: {str(e)}")
            raise
    
    def create_users_table(self):
        """Create table for storing users"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
            logger.info("Users table created/verified")
        except sqlite3.Error as e:
            logger.error(f"Error creating table: {str(e)}")
            raise
    
    def insert_conversation(self, user_message, ai_response, user_id=None):
        """Save conversation to database"""
        try:
            self.cursor.execute("""
                INSERT INTO conversations (user_message, ai_response, user_id)
                VALUES (?, ?, ?)
            """, (user_message, ai_response, user_id))
            self.connection.commit()
            logger.info("Conversation saved to database")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error inserting conversation: {str(e)}")
            raise
    
    def insert_expense(self, name, amount, category=None, user_id=None):
        """Save expense to database"""
        try:
            self.cursor.execute("""
                INSERT INTO expenses (name, amount, category, user_id)
                VALUES (?, ?, ?, ?)
            """, (name, amount, category, user_id))
            self.connection.commit()
            logger.info(f"Expense '{name}' saved: {amount}")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error inserting expense: {str(e)}")
            raise
    
    def get_all_conversations(self, user_id=None):
        """Retrieve all conversations"""
        try:
            if user_id:
                self.cursor.execute(
                    "SELECT * FROM conversations WHERE user_id = ? ORDER BY timestamp DESC",
                    (user_id,)
                )
            else:
                self.cursor.execute("SELECT * FROM conversations ORDER BY timestamp DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error retrieving conversations: {str(e)}")
            raise
    
    def get_all_expenses(self, user_id=None):
        """Retrieve all expenses"""
        try:
            if user_id:
                self.cursor.execute(
                    "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC",
                    (user_id,)
                )
            else:
                self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error retrieving expenses: {str(e)}")
            raise
    
    def get_total_expenses(self, user_id=None):
        """Get sum of all expenses"""
        try:
            if user_id:
                self.cursor.execute(
                    "SELECT SUM(amount) FROM expenses WHERE user_id = ?",
                    (user_id,)
                )
            else:
                self.cursor.execute("SELECT SUM(amount) FROM expenses")
            result = self.cursor.fetchone()
            return result[0] if result[0] else 0
        except sqlite3.Error as e:
            logger.error(f"Error calculating total: {str(e)}")
            raise
    
    def delete_conversation(self, conversation_id):
        """Delete a conversation"""
        try:
            self.cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            self.connection.commit()
            logger.info(f"Conversation {conversation_id} deleted")
        except sqlite3.Error as e:
            logger.error(f"Error deleting conversation: {str(e)}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

# Test the database
if __name__ == "__main__":
    try:
        db = Database("test_app.db")
        
        # Create tables
        db.create_conversations_table()
        db.create_expenses_table()
        db.create_users_table()
        
        # Insert test data
        db.insert_conversation("Hello", "Hi there!", user_id="user1")
        db.insert_conversation("How are you?", "I am doing well!", user_id="user1")
        db.insert_expense("Food", 500, "meals", user_id="user1")
        db.insert_expense("Transport", 1200, "travel", user_id="user1")
        
        # Retrieve data
        conversations = db.get_all_conversations("user1")
        expenses = db.get_all_expenses("user1")
        total = db.get_total_expenses("user1")
        
        print("\n--- Conversations ---")
        for conv in conversations:
            print(f"User: {conv[1]}")
            print(f"AI: {conv[2]}")
            print(f"Time: {conv[3]}\n")
        
        print("--- Expenses ---")
        for exp in expenses:
            print(f"Item: {exp[1]}, Amount: {exp[2]}, Category: {exp[3]}")
        
        print(f"\nTotal Expenses: {total}")
        
        db.close()
        print("\nDatabase test completed successfully!")
    
    except Exception as e:
        print(f"Error: {str(e)}")