import sqlite3
import hashlib
from datetime import datetime

class AuthSystem:
    """Professional user authentication system"""
    
    def __init__(self, db_name="nsuk_auth.db"):
        """Initialize authentication database"""
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.create_default_admin()
    
    def create_tables(self):
        """Create authentication tables"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'student',
                department TEXT,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                ip_address TEXT
            )
        """)
        self.connection.commit()
    
    def create_default_admin(self):
        """Create default admin account if none exists"""
        self.cursor.execute(
            "SELECT id FROM users WHERE role = 'admin'"
        )
        if not self.cursor.fetchone():
            self.register_user(
                user_id="ADMIN001",
                full_name="NSUK Administrator",
                email="admin@nsuk.edu.ng",
                password="admin123",
                role="admin"
            )
    
    def hash_password(self, password):
        """Hash password securely using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, user_id, full_name, email, password, role="student", department=None):
        """Register a new user"""
        try:
            if len(password) < 6:
                return False, "Password must be at least 6 characters"
            if len(user_id) < 3:
                return False, "User ID must be at least 3 characters"
            
            password_hash = self.hash_password(password)
            self.cursor.execute("""
                INSERT INTO users (user_id, full_name, email, password_hash, role, department)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, full_name, email, password_hash, role, department))
            self.connection.commit()
            return True, "Registration successful!"
        
        except sqlite3.IntegrityError as e:
            if "user_id" in str(e):
                return False, "User ID already exists"
            elif "email" in str(e):
                return False, "Email already registered"
            return False, "Registration failed"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def login(self, user_id, password):
        """Login a user"""
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute("""
                SELECT id, user_id, full_name, role, department, is_active
                FROM users
                WHERE user_id = ? AND password_hash = ?
            """, (user_id, password_hash))
            
            user = self.cursor.fetchone()
            
            if not user:
                self.cursor.execute("""
                    INSERT INTO login_history (user_id, status)
                    VALUES (?, ?)
                """, (user_id, "failed"))
                self.connection.commit()
                return False, "Invalid ID or password"
            
            if user[5] == 0:
                return False, "Account is deactivated. Contact admin."
            
            self.cursor.execute("""
                UPDATE users SET last_login = ? WHERE user_id = ?
            """, (datetime.now(), user_id))
            
            self.cursor.execute("""
                INSERT INTO login_history (user_id, status)
                VALUES (?, ?)
            """, (user_id, "success"))
            
            self.connection.commit()
            
            return True, {
                "id": user[0],
                "user_id": user[1],
                "full_name": user[2],
                "role": user[3],
                "department": user[4]
            }
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_all_users(self):
        """Get all registered users"""
        self.cursor.execute("""
            SELECT user_id, full_name, email, role, department, 
                   is_active, created_at, last_login
            FROM users ORDER BY created_at DESC
        """)
        return self.cursor.fetchall()
    
    def deactivate_user(self, user_id):
        """Deactivate a user account"""
        self.cursor.execute(
            "UPDATE users SET is_active = 0 WHERE user_id = ?",
            (user_id,)
        )
        self.connection.commit()
        return True, f"User {user_id} deactivated"
    
    def reset_password(self, user_id, new_password):
        """Reset user password"""
        if len(new_password) < 6:
            return False, "Password must be at least 6 characters"
        password_hash = self.hash_password(new_password)
        self.cursor.execute("""
            UPDATE users SET password_hash = ? WHERE user_id = ?
        """, (password_hash, user_id))
        self.connection.commit()
        return True, "Password reset successfully"
    
    def get_user_count(self):
        """Get total users by role"""
        self.cursor.execute("""
            SELECT role, COUNT(*) FROM users GROUP BY role
        """)
        return self.cursor.fetchall()
    
    def get_login_history(self, limit=20):
        """Get recent login history"""
        self.cursor.execute("""
            SELECT user_id, login_time, status
            FROM login_history
            ORDER BY login_time DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()