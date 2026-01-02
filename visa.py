import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from plyer import notification

# --- Notification Helper ---
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# --- Core Logic ---
def check_h1b_slots():
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)

    try:
        driver.get("https://visaslots.info/")
        print("Waiting for Cloudflare check...")
        time.sleep(8)  # wait for Cloudflare protection

        # Get all rows in the table
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        h1b_consular = []

        for row in rows:
            cells = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
            if len(cells) >= 5:
                location, visa_type, _, date, count = cells[:5]
                if (("H-1B" in visa_type and "CONSULAR" in location) or ("H-4" in visa_type and "VAC" in location)) and date != "N/A":
                    h1b_consular.append({
                        "location": location,
                        "date": date,
                        "count": count
                    })

        return h1b_consular

    finally:
        driver.quit()

# --- Continuous Monitoring ---
def main():
    print("Starting H1B slot monitor...")

    while True:
        slots = check_h1b_slots()
        print(f"Checked {time.strftime('%H:%M:%S')} → Found {len(slots)} available slots")

        for slot in slots:
            slot_id = f"{slot['location']}|{slot['date']}"
            if slot_id:
                message = f"{slot['location']} — {slot['date']} ({slot['count']} slots)"
                print("🟢 New slot:", message)
                send_notification("H-1B Slot Available!", message)

        # Query every 60 seconds (you can lower to e.g. 30)
        time.sleep(60)

if __name__ == "__main__":
    main()
