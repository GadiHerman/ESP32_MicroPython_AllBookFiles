import json
import os

class UserManager:
    def __init__(self, filename="users.txt"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """יוצר קובץ משתמשים אם לא קיים"""
        if not self.filename in os.listdir():
            with open(self.filename, 'w') as f:
                json.dump({}, f)
    
    def _read_users(self):
        """קורא את רשימת המשתמשים מהקובץ"""
        with open(self.filename, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users):
        """שומר את רשימת המשתמשים לקובץ"""
        with open(self.filename, 'w') as f:
            json.dump(users, f)
    
    def verify_login(self, username, password):
        """מאמת פרטי התחברות"""
        users = self._read_users()
        return username in users and users[username] == password
    
    def add_user(self, username, password):
        """מוסיף משתמש חדש"""
        users = self._read_users()
        if username in users:
            return False, "שם המשתמש כבר קיים"
        users[username] = password
        self._save_users(users)
        return True, "המשתמש נוסף בהצלחה"
    
    def delete_user(self, username):
        """מוחק משתמש"""
        users = self._read_users()
        if username not in users:
            return False, "המשתמש לא קיים"
        del users[username]
        self._save_users(users)
        return True, "המשתמש נמחק בהצלחה"
    
    def update_password(self, username, new_password):
        """מעדכן סיסמה למשתמש"""
        users = self._read_users()
        if username not in users:
            return False, "המשתמש לא קיים"
        users[username] = new_password
        self._save_users(users)
        return True, "הסיסמה עודכנה בהצלחה"
    
    def list_users(self):
        """מחזיר רשימת משתמשים"""
        return list(self._read_users().keys())

def admin_menu(user_manager):
    """תפריט ניהול משתמשים"""
    while True:
        print("\n=== תפריט ניהול משתמשים ===")
        print("1. הוסף משתמש חדש")
        print("2. מחק משתמש")
        print("3. עדכן סיסמה")
        print("4. הצג רשימת משתמשים")
        print("5. התנתק")
        
        choice = input("\nבחר אפשרות (1-5): ")
        
        if choice == "1":
            username = input("הכנס שם משתמש חדש: ")
            password = input("הכנס סיסמה: ")
            success, message = user_manager.add_user(username, password)
            print(message)
        
        elif choice == "2":
            username = input("הכנס שם משתמש למחיקה: ")
            success, message = user_manager.delete_user(username)
            print(message)
        
        elif choice == "3":
            username = input("הכנס שם משתמש: ")
            new_password = input("הכנס סיסמה חדשה: ")
            success, message = user_manager.update_password(username, new_password)
            print(message)
        
        elif choice == "4":
            users = user_manager.list_users()
            print("\nרשימת משתמשים:")
            for user in users:
                print(f"- {user}")
        
        elif choice == "5":
            print("להתראות!")
            break
        
        else:
            print("אפשרות לא חוקית")
        
        input("\nלחץ Enter להמשך...")

def main():
    user_manager = UserManager()
    
    # אם אין משתמשים, צור משתמש ברירת מחדל
    if not user_manager.list_users():
        user_manager.add_user("admin", "admin")
        print("נוצר משתמש ברירת מחדל: admin/admin")
    
    while True:
        print("\n=== מערכת התחברות ===")
        username = input("שם משתמש: ")
        password = input("סיסמה: ")
        
        if user_manager.verify_login(username, password):
            print("\nהתחברת בהצלחה!")
            admin_menu(user_manager)
            break
        else:
            print("\nשם משתמש או סיסמה שגויים")
            retry = input("לנסות שוב? (Y/N): ")
            if retry.lower() != 'y':
                break

if __name__ == "__main__":
    main()
