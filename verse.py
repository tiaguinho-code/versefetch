import requests
import textwrap
import os
import random
from datetime import datetime
import yaml 

def get_daily_verse():
    popular_verses_keys = ['1 Corinthians 13:4', '1 John 4:8', '1 Peter 5:7', '1 Thessalonians 5:17', '2 Corinthians 5:17', '2 Timothy 1:7', 'Acts 1:8', 'Acts 2:38', 'Colossians 3:16', 'Ephesians 2:8', 'Ephesians 4:32', 'Galatians 5:22', 'Genesis 1:1', 'Genesis 1:26', 'Hebrews 11:1', 'Isaiah 41:10', 'Isaiah 53:5', 'James 1:2', 'James 1:5', 'Jeremiah 29:11', 'John 10:10', 'John 3:16', 'Joshua 1:9', 'Luke 11:9', 'Luke 6:31', 'Matthew 11:28', 'Matthew 28:19', 'Matthew 5:14', 'Matthew 6:33', 'Philippians 4:13', 'Philippians 4:6', 'Proverbs 18:10', 'Proverbs 22:6', 'Proverbs 3:5', 'Psalms 119:105', 'Psalms 150:6', 'Psalms 23:1', 'Romans 12:2', 'Romans 6:23', 'Romans 8:28']

    # Obtain current date
    today = datetime.now()
    # Create a seed from the day, month, and year
    seed = today.day + today.month + today.year
    # Seed the random number generator
    random.seed(seed)
    
    # Select a random verse from the list using the seeded random generator
    random_verse = random.choice(popular_verses_keys)
    return random_verse

def fetch_daily_verse(verse):
    url = f"https://bible-api.com/{verse}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        verse_data = response.json()
        text = verse_data['text']
        reference = verse_data['reference']
        return text, reference
    except requests.RequestException as e:
        print(f"Error fetching the daily Bible verse: {e}")
        return None, None

def local_fetch_verse(verse):
    try:
        reference = verse
        with open("/home/tiago/Documents/polybox/verse.yaml", 'r') as file:
            dictio = yaml.safe_load(file)
            text = dictio.get(reference)
        return text, reference
    except requests.RequestException as e:
        print(f"Error fetching the daily Bible verse: {e}")
        return None, None


def get_terminal_width():
    try:
        size = os.get_terminal_size()
        return size.columns
    except OSError:
        return 80

def print_rounded_frame(text_lines):
    max_length = max(len(line) for line in text_lines)
    width = max_length + 4  # padding for aesthetics

    # Top border
    print("\u256D" + "\u2500" + "\033[1;36m Daily Bible Verse \033[0m" + "\u2500" * (width - 22) + "\u256E")

    # Text within the border
    for line in text_lines:
        padding = " " * (width - len(line) - 4)
        print(f"\u2502 \033[1;33m{line}\033[0m{padding} \u2502")

    # Bottom border
    print("\u2570" + "\u2500" * (width - 2) + "\u256F")


def main():
    text, reference = local_fetch_verse(get_daily_verse())
    if text:
        columns = get_terminal_width() - 4  # Adjust width for border
        wrapped_text = textwrap.fill(text.strip(), width=columns)
        wrapped_text += "\n- " + reference
        text_lines = wrapped_text.split("\n")
        print_rounded_frame(text_lines)
        print("\n")

if __name__ == "__main__":
    main()
