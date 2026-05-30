import os
import requests
from supabase import create_client, Client

# 1. Configuration
WEBSITES = [
    "https://www.google.com", 
    "https://arxiv.org",
    "https://chatgpt.com/"
    "http://www.youtube.com"
    "http://www.facebook.com"
    "http://www.instagram.com"
    "http://www.linkedin.com"
    "http://www.yahoo.co.jp"
    "http://www.msn.com"
    "http://www.pinterest.com"
    "http://www.netflix.com"
    
    # Add your personal library website URL here!
]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def log_downtime(url, status_code, error_msg):
    """Inserts a failure log into the Supabase database."""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        data = {
            "website_url": url,
            "status_code": status_code,
            "error_message": error_msg
        }
        supabase.table("downtime_logs").insert(data).execute()
        print(f"❌ Logged failure for {url}")
    except Exception as e:
        print(f"Failed to log to Supabase: {e}")

def check_websites():
    print("Starting website check...")
    for url in WEBSITES:
        try:
            # Send a request with a 10-second timeout
            response = requests.get(url, timeout=10)
            
            # If the status code is NOT in the 200-399 range, it's an issue
            if not response.ok:
                log_downtime(url, response.status_code, "Non-200 Status Code")
            else:
                print(f"✅ {url} is up! ({response.status_code})")
                
        except requests.exceptions.RequestException as e:
            # This catches network timeouts, DNS errors, etc.
            log_downtime(url, None, str(e))

if __name__ == "__main__":
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: Missing Supabase Environment Variables.")
    else:
        check_websites()