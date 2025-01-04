#!/usr/bin/env python3

import requests
import json
from bs4 import BeautifulSoup

def get_code_value(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract the code value based on the specific HTML structure
        code_value = soup.find('span', class_='font-size-20 text-white').text.strip()
        return int(code_value)
    except Exception as e:
        print(f"Error fetching the code value: {e}")
        return None

def send_to_discord(webhook_url, message):
    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print(f"Message sent to Discord: {message}")
    except Exception as e:
        print(f"Error sending message to Discord: {e}")

def main():
    urls = {
        "CDSA": "https://academy.hackthebox.com/achievement/badge/82cd4c4a-aa21-11ee-bfb6-bea50ffe6cb4",
        "CPTS": "https://academy.hackthebox.com/achievement/badge/7afa3db6-b304-11ef-864f-bea50ffe6cb4",
        "CBBH": "https://academy.hackthebox.com/achievement/badge/05d65b60-9daf-11ef-864f-bea50ffe6cb4",
        "CWEE": "https://academy.hackthebox.com/achievement/badge/9b5c7136-e85b-11ee-b18d-bea50ffe6cb4"
    }
    discord_webhook_url = "<Discord_Webhook_Url>"  # create a discord server webhook and place the url here
    last_values_file = "last_values.json"

    # Check if the last values exist
    try:
        with open(last_values_file, 'r') as file:
            last_values = json.load(file)
    except FileNotFoundError:
        print("No previous values found. Fetching initial values...")
        last_values = {key: None for key in urls}

    messages = []
    for key, url in urls.items():
        current_value = get_code_value(url)

        if current_value is not None:
            if last_values[key] is None:
                messages.append(f"{key}: Initial value fetched: {current_value}.")
            elif current_value != last_values[key]:
                difference = current_value - last_values[key]
                messages.append(f"{key}: New values ! {current_value} (+{difference}).")
            else:
                messages.append(f"{key}: Same value... No batch: {current_value}.")

            # Update last value
            last_values[key] = current_value
        else:
            messages.append(f"{key}: Error fetching the code value.")

    # Save updated values
    with open(last_values_file, 'w') as file:
        json.dump(last_values, file)

    # Send combined message to Discord
    send_to_discord(discord_webhook_url, "\n".join(messages))

if __name__ == "__main__":
    main()