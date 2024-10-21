import ujson

# קריאת קובץ JSON
def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
        return ujson.loads(data)
    except OSError as e:
        print("שגיאה בקריאת הקובץ:", e)
        return None

# פענוח והדפסת תוכן ה-JSON
def parse_and_print_json(json_data):
    if json_data is not None:
        print("שם:", json_data.get("שם"))
        print("גיל:", json_data.get("גיל"))
        print("עיר:", json_data.get("עיר"))
        print("נשוי:", "כן" if json_data.get("נשוי") else "לא")
        
        print("תחביבים:")
        for hobby in json_data.get("תחביבים", []):
            print("- " + hobby)
        
        work = json_data.get("עבודה", {})
        print("עבודה:")
        print("- תפקיד:", work.get("תפקיד"))
        print("- חברה:", work.get("חברה"))

# שימוש בפונקציות
filename = "data.json"
json_data = read_json_file(filename)
parse_and_print_json(json_data)