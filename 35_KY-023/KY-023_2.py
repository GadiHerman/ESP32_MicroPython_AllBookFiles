
from machine import Pin, ADC, I2C
from i2c_lcd import I2C_LCD
from time import sleep_ms

# Setup I2C and LCD
i2c = I2C(scl=Pin(22), sda=Pin(21))
lcd = I2C_LCD(i2c, 0x27)

# Setup Joystick Y axis for scrolling
joy_y = ADC(Pin(35))
joy_y.atten(ADC.ATTN_11DB)

# Setup Joystick Button for selecting
joy_btn = Pin(32, Pin.IN, Pin.PULL_UP)

# Define the menu items
menu_items = ["1. Start Game", "2. Settings", "3. High Score", "4. Exit"]
current_item = 0

# Function to draw the menu on the LCD
def draw_menu():
    lcd.clear()
    
    # Print current item on the first line with a cursor
    lcd.puts("> " + menu_items[current_item], 0, 0)
    
    # Print the next item on the second line if it exists
    if current_item + 1 < len(menu_items):
        lcd.puts("  " + menu_items[current_item + 1], 0, 1)

# Draw the initial menu
draw_menu()

while True:
    y_val = joy_y.read()
    btn_val = joy_btn.value()
    
    # Move Down (Y value is high)
    if y_val > 3000:
        if current_item < len(menu_items) - 1:
            current_item += 1
            draw_menu()
            # Simple delay to prevent scrolling too fast
            sleep_ms(300) 
            
    # Move Up (Y value is low)
    if y_val < 1000:
        if current_item > 0:
            current_item -= 1
            draw_menu()
            # Simple delay to prevent scrolling too fast
            sleep_ms(300)
            
    # Select item (Button is pressed -> value is 0)
    if btn_val == 0:
        lcd.clear()
        lcd.puts("You Selected:")
        lcd.puts(menu_items[current_item], 0, 1)
        
        # Show selection for 2 seconds
        sleep_ms(2000) 
        
        # Redraw menu to go back
        draw_menu() 
        
    # Small delay for system stability
    sleep_ms(100)


