import os
import gc

def get_fs_info():
    """מחזיר מידע על מערכת הקבצים"""
    try:
        # חישוב נפח כולל וזמין
        stats = os.statvfs('/')
        total_space = stats[0] * stats[2]  # block_size * total_blocks
        free_space = stats[0] * stats[3]   # block_size * free_blocks
        return {
            'total_space': total_space,
            'free_space': free_space
        }
    except Exception as e:
        return f"שגיאה בקבלת מידע על מערכת הקבצים: {str(e)}"

def list_files():
    """מציג את כל הקבצים במערכת"""
    try:
        return os.listdir()
    except Exception as e:
        return f"שגיאה בהצגת קבצים: {str(e)}"

def create_file(filename, content):
    """יוצר קובץ חדש עם תוכן מסוים"""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"הקובץ {filename} נוצר בהצלחה"
    except Exception as e:
        return f"שגיאה ביצירת הקובץ: {str(e)}"

def read_file(filename):
    """קורא תוכן מקובץ"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:
        return f"שגיאה בקריאת הקובץ: {str(e)}"

def delete_file(filename):
    """מוחק קובץ"""
    try:
        os.remove(filename)
        return f"הקובץ {filename} נמחק בהצלחה"
    except Exception as e:
        return f"שגיאה במחיקת הקובץ: {str(e)}"

def print_menu():
    """מציג תפריט אפשרויות"""
    print("\n=== תפריט מערכת קבצים ===")
    print("1. הצג מידע על מערכת הקבצים")
    print("2. הצג רשימת קבצים")
    print("3. צור קובץ חדש")
    print("4. קרא מקובץ")
    print("5. מחק קובץ")
    print("6. יציאה")
    print("========================")

def main_menu():
    """לולאת התפריט הראשי"""
    while True:
        print_menu()
        choice = input("בחר אפשרות (1-6): ")
        
        if choice == '1':
            info = get_fs_info()
            print("\nמידע על מערכת הקבצים:")
            print(f"נפח כולל: {info['total_space']} bytes")
            print(f"נפח פנוי: {info['free_space']} bytes")
        
        elif choice == '2':
            print("\nרשימת קבצים:")
            files = list_files()
            for f in files:
                print(f"- {f}")
        
        elif choice == '3':
            filename = input("שם הקובץ: ")
            content = input("תוכן הקובץ: ")
            print(create_file(filename, content))
        
        elif choice == '4':
            filename = input("שם הקובץ לקריאה: ")
            print("\nתוכן הקובץ:")
            print(read_file(filename))
        
        elif choice == '5':
            filename = input("שם הקובץ למחיקה: ")
            print(delete_file(filename))
        
        elif choice == '6':
            print("להתראות!")
            break
        
        else:
            print("אפשרות לא חוקית, נסה שוב")
        
        print("\nלחץ Enter להמשך...")
        input()
        gc.collect()  # ניקוי זיכרון לא בשימוש

if __name__ == '__main__':
    main_menu()
