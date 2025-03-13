import requests
from bs4 import BeautifulSoup
from plyer import notification
import urllib.request
import time
 
# Function to send notifications
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification will disappear after 10 seconds
    )
 
# Function to parse HTML and check for changes
def parse_html(url, last_content):
    try:
        # Send HTTP request and get the webpage content
        session = requests.Session()
        response = session.get(url, headers={'User-Agent': 'Mozilla/6.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        all_dates = [row.find('td', {"class":"earliest"}).get_text().strip() for row in soup.find('table').tbody.find_all('tr') if 'VAC' in row.find('a').get_text() and 'N/A' not in row.find('td', {"class":"earliest"}).get_text().strip()]
        print(all_dates)
        if all_dates:
            send_notification("Appointments Available", f"{all_dates}")
  
    except Exception as e:
        print(f"Error: {e}")
        return last_content
 
# Main loop to run the script continuously
def main():

    url = "https://visaslots.info/"
    while True:
        print("checking dates")
        parse_html(url, "")
        time.sleep(30)
 
if __name__ == "__main__":
    main()