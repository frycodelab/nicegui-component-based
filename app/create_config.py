import json
import os

def create_config():
    """Create a default config.json file if it doesn't exist"""
    
    config_path = "config.json"
    
    if os.path.exists(config_path):
        print("config.json already exists!")
        return
    
    default_config = {
        "appName": "NiceGUI Base App",
        "appVersion": "v1.0.0",
        "appPort": 8080,
        "google_oauth": {
            "client_id": "YOUR_GOOGLE_CLIENT_ID_HERE",
            "client_secret": "YOUR_GOOGLE_CLIENT_SECRET_HERE",
            "redirect_uri": "http://localhost:8080/auth"
        }
    }
    
    with open(config_path, 'w') as file:
        json.dump(default_config, file, indent=4)
    
    print("Created config.json file!")
    print("Please update the Google OAuth credentials in config.json before running the application.")
    print("See OAUTH_SETUP.md for detailed instructions.")

if __name__ == "__main__":
    create_config()
