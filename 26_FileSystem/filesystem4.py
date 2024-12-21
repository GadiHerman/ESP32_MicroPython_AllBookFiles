import os

def get_fs_info():
    try:
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
    try:
        return os.listdir()
    except Exception as e:
        return f"שגיאה בהצגת קבצים: {str(e)}"

info = get_fs_info()
print("\nמידע על מערכת הקבצים:")
print(f"נפח כולל: {info['total_space']} bytes")
print(f"נפח פנוי: {info['free_space']} bytes")

print("\nרשימת קבצים:")
files = list_files()
for f in files:
    print(f"- {f}")
