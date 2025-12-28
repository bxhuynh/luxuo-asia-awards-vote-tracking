import subprocess
import time
import datetime
import os

# Configuration
SCRIPT_NAME = "scraper.py"  # Your scraping script
DATA_FILE = "data.json"     # The file being updated
INTERVAL = 600              # 10 minutes in seconds

def run_automation():
    print(f"--- Starting Task: {datetime.datetime.now()} ---")

    try:
        # 1. Run the scraper
        print(f"Running {SCRIPT_NAME}...")
        subprocess.run(["python3", SCRIPT_NAME], check=True)

        # 2. Configure Git (Only needs to be done once, but safe to repeat)
        subprocess.run(["git", "config", "user.name", "Scraper Bot"], check=True)
        subprocess.run(["git", "config", "user.email", "bot@github.com"], check=True)

        # 3. Add, Commit, and Push
        print("Committing changes to GitHub...")
        subprocess.run(["git", "add", DATA_FILE], check=True)
        
        # We use a simplified date string for the commit message
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Update votes: {current_time}"
        
        # The '|| exit 0' logic: commit only if there are changes
        result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
        
        if "nothing to commit" in result.stdout:
            print("No changes detected in data.json. Skipping push.")
        else:
            subprocess.run(["git", "push"], check=True)
            print("Successfully pushed to GitHub!")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        run_automation()
        print(f"Next run in {INTERVAL/60} minutes...")
        time.sleep(INTERVAL)