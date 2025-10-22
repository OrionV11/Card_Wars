import requests
import json
import time
from bs4 import BeautifulSoup

def get_all_card_ids(session):
    """
    Get all card IDs by iterating through the cards.
    CardDweeb uses ?id= parameter for individual cards.
    We'll try IDs from 1 to a reasonable upper limit.
    """
    print("Discovering card IDs...")
    card_ids = []
    
    # Based on search results, we know cards exist up to at least id=553
    # Let's check up to 1000 to be safe
    for card_id in range(1, 1001):
        try:
            url = f"https://www.carddweeb.com/Card?id={card_id}"
            response = session.head(url, timeout=5)
            
            # If we get a 200, the card exists
            if response.status_code == 200:
                card_ids.append(card_id)
                if card_id % 50 == 0:
                    print(f"  Checked up to ID {card_id}... Found {len(card_ids)} cards so far")
        except:
            continue
    
    print(f"Found {len(card_ids)} total cards")
    return card_ids

def scrape_card_detail(card_id, session):
    """
    Scrape a single card's details from carddweeb.com
    """
    url = f"https://www.carddweeb.com/Card?id={card_id}"
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all text content and parse it
        page_text = soup.get_text()
        
        # Get card name (from title)
        name = ''
        title_tag = soup.find('title')
        if title_tag:
            name = title_tag.text.strip()
            # Remove "- Card Dweeb" suffix if present
            if ' - Card Dweeb' in name:
                name = name.replace(' - Card Dweeb', '').strip()
            if ' -Card Dweeb' in name:
                name = name.replace(' -Card Dweeb', '').strip()
        
        # Parse using text extraction with markers
        card_type = ''
        if 'Card Type:' in page_text:
            try:
                parts = page_text.split('Card Type:')[1].split('\n')
                # Get the first non-empty line after "Card Type:"
                for part in parts:
                    cleaned = part.strip()
                    if cleaned and cleaned not in ['Creature', 'Spell', 'Building', 'Hero', 'Landscape', 'Teamwork']:
                        continue
                    if cleaned in ['Creature', 'Spell', 'Building', 'Hero', 'Landscape', 'Teamwork']:
                        card_type = cleaned
                        break
            except:
                pass
        
        # Get landscape
        landscape = ''
        if 'Landscape:' in page_text:
            try:
                parts = page_text.split('Landscape:')[1].split('\n')
                for part in parts:
                    cleaned = part.strip()
                    if cleaned and cleaned not in ['Blue Plains', 'Cornfields', 'Useless Swamp', 'SandyLands', 
                                                     'NiceLands', 'IcyLands', 'Rainbow', 'LavaFlats', 'DarkLands']:
                        continue
                    if cleaned:
                        landscape = cleaned
                        break
            except:
                pass
        
        # Get ability
        ability = ''
        if 'Ability:' in page_text:
            try:
                ability_part = page_text.split('Ability:')[1]
                # Find text until the next known marker
                next_marker_idx = len(ability_part)
                for marker in ['Set:', 'Cost:', 'Attack:', 'Defense:', 'Revisions:']:
                    idx = ability_part.find(marker)
                    if idx != -1 and idx < next_marker_idx:
                        next_marker_idx = idx
                ability = ability_part[:next_marker_idx].strip()
                # Remove duplicate lines
                lines = [l.strip() for l in ability.split('\n') if l.strip()]
                if len(lines) > 1 and lines[0] == lines[1]:
                    ability = lines[0]
                else:
                    ability = ' '.join(lines)
            except:
                pass
        
        # Get cost
        cost = ''
        if 'Cost:' in page_text:
            try:
                cost_str = page_text.split('Cost:')[1].strip().split()[0]
                cost = int(cost_str)
            except:
                pass
        
        # Get attack
        attack = ''
        if 'Attack:' in page_text:
            try:
                attack_str = page_text.split('Attack:')[1].strip().split()[0]
                attack = int(attack_str)
            except:
                pass
        
        # Get defense
        defense = ''
        if 'Defense:' in page_text:
            try:
                defense_str = page_text.split('Defense:')[1].strip().split()[0]
                defense = int(defense_str)
            except:
                pass
        
        # Get image URL
        cover_url = ''
        img_tag = soup.find('img', src=lambda x: x and '/CardImages/' in x)
        if img_tag:
            cover_url = 'https://www.carddweeb.com' + img_tag['src']
        
        return {
            'id': card_id,
            'name': name or 'Unknown Name',
            'type': card_type or 'Unknown',
            'landscape': landscape or '',
            'ability': ability or '',
            'cost': cost if cost != '' else None,
            'attack': attack if attack != '' else None,
            'defense': defense if defense != '' else None,
            'cover_url': cover_url,
            'url': url
        }
        
    except Exception as e:
        print(f"  Error scraping card ID {card_id}: {e}")
        return None

def organize_cards_by_type(cards_list):
    """
    Organize cards into a dictionary where each type contains a list of cards
    Format: {"Creature": [{...}], "Spell": [{...}], "Hero": [{...}]}
    """
    organized = {}
    
    for card in cards_list:
        card_type = card.get('type', 'Unknown')
        
        # Create a cleaner card data dict (remove 'id', 'type', and 'url' for output)
        card_data = {
            'name': card.get('name'),
            'landscape': card.get('landscape'),
            'ability': card.get('ability'),
            'cost': card.get('cost'),
            'attack': card.get('attack'),
            'defense': card.get('defense'),
            'cover_url': card.get('cover_url')
        }
        
        # Initialize the type list if it doesn't exist
        if card_type not in organized:
            organized[card_type] = []
        
        organized[card_type].append(card_data)
    
    return organized

def main():
    print("="*60)
    print("CardDweeb.com Card Scraper")
    print("="*60)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    # Step 1: Get all card IDs
    card_ids = get_all_card_ids(session)
    
    if not card_ids:
        print("No cards found. Exiting.")
        return
    
    # Step 2: Scrape each card
    print(f"\nScraping {len(card_ids)} cards...")
    all_cards = []
    success_count = 0
    fail_count = 0
    
    for i, card_id in enumerate(card_ids, 1):
        print(f"[{i}/{len(card_ids)}] Scraping card ID {card_id}...", end='')
        
        data = scrape_card_detail(card_id, session)
        
        if data:
            print(f" ✓ {data['name']} ({data['type']})")
            all_cards.append(data)
            success_count += 1
        else:
            print(f" ✗ Failed")
            fail_count += 1
        
        # Be respectful - add delay between requests
        if i % 10 == 0:
            time.sleep(2)  # Longer pause every 10 requests
        else:
            time.sleep(0.5)  # Short pause between requests
    
    # Step 3: Organize by type
    print("\n" + "="*60)
    print("Organizing cards by type...")
    organized_cards = organize_cards_by_type(all_cards)
    
    # Print summary
    print("\nSummary by Type:")
    for card_type, cards in sorted(organized_cards.items()):
        print(f"  {card_type}: {len(cards)} cards")
    
    # Step 4: Save to files
    
    # Save organized by type
    output_file_typed = 'carddweeb_cards_by_type.json'
    with open(output_file_typed, 'w', encoding='utf-8') as f:
        json.dump(organized_cards, f, indent=4, ensure_ascii=False)
    print(f"\n✓ Saved organized data to: {output_file_typed}")
    
    # Save all cards (flat list with all details)
    output_file_all = 'carddweeb_all_cards.json'
    with open(output_file_all, 'w', encoding='utf-8') as f:
        json.dump(all_cards, f, indent=4, ensure_ascii=False)
    print(f"✓ Saved complete data to: {output_file_all}")
    
    print("\n" + "="*60)
    print(f"Scraping Complete!")
    print(f"  Successfully scraped: {success_count} cards")
    print(f"  Failed: {fail_count} cards")
    print("="*60)

if __name__ == "__main__":
    main()