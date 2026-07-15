import network
import urequests
import ujson
import time

# --- Configuration variables ---
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_WiFi_Password"
# Replace with your local PC IP address found in Step 3
OLLAMA_API_URL = "http://10.0.0.27:11434/api/generate" 

def connect_to_wifi():
    print("Starting Wi-Fi connection process...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Wait until the connection is established
    while not wlan.isconnected():
        print("Connecting to network... Please wait.")
        time.sleep(1)
        
    print("Successfully connected to Wi-Fi!")
    print("ESP32 IP Address configuration:", wlan.ifconfig()[0])

def ask_local_llm(prompt_text):
    """Sends a text prompt to the local Ollama API and returns the response."""
    print("Preparing payload for the local LLM...")
    
    # Create the data structure expected by Ollama API
    payload = {
        "model": "gemma:2b",
        "prompt": prompt_text,
        "stream": False  # We want the full answer at once, not word-by-word
    }
    
    # Define headers to indicate JSON content
    headers = {"Content-Type": "application/json"}
    
    try:
        # Send the HTTP POST request to the PC
        print("Sending HTTP request to PC...")
        response = urequests.post(OLLAMA_API_URL, json=payload, headers=headers)
        
        # Parse the JSON response received from the server
        parsed_data = response.json()
        response.close()
        
        # Extract the text answer from the JSON structure
        llm_answer = parsed_data.get("response", "No response field found.")
        return llm_answer
        
    except Exception as error:
        # Simple error handling for debugging connection issues
        return "An error occurred during communication: " + str(error)

# --- Main Program Execution ---
connect_to_wifi()
while True:
    print("\n================================================")
    user_input = input("Enter your prompt for Gemma (or type 'quit' to stop): ")
    if user_input.strip().lower() == "quit":
        print("Exiting program. Goodbye!")
        break
        
    if not user_input.strip():
        print("Prompt cannot be empty. Try again.")
        continue
        
    # Send the prompt to the PC and get the answer
    result = ask_local_llm(user_input)
    print("\n--- Response from Local Gemma Model ---")
    print(result)
    print("----------------------------------------")
