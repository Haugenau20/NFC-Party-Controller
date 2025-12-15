#!/usr/bin/env python3
"""
Convert old automation format to new blueprint-based format
Usage: python convert_automations.py
Input: input_automations.yaml (paste your old automations here)
Output: output_automations.yaml (blueprint-based automations)
"""

import yaml
import sys

# Input and output files
INPUT_FILE = "input_automations.yaml"
OUTPUT_FILE = "output_automations.yaml"

# Blueprint path
BLUEPRINT_PATH = "homeassistant/nfc_song_queue.yaml"

def extract_song_name(alias):
    """Extract song name from alias for the song_name field"""
    # The alias format might vary, so we'll just use the full alias
    # Users can manually adjust if needed
    return alias.replace("Tag ", "").replace(" is scanned", "")

def convert_automation(old_auto):
    """Convert old automation format to new blueprint format"""

    # Extract needed fields
    auto_id = old_auto.get('id', '')
    alias = old_auto.get('alias', '')
    tag_id = old_auto['triggers'][0]['tag_id']
    spotify_uri = old_auto['actions'][0]['data']['spotify_uris']

    # Create new blueprint-based automation
    new_auto = {
        'id': auto_id,
        'alias': alias,
        'description': '',
        'use_blueprint': {
            'path': BLUEPRINT_PATH,
            'input': {
                'song_name': extract_song_name(alias),
                'tag_id': tag_id,
                'spotify_uri': spotify_uri
            }
        }
    }

    return new_auto

def main():
    try:
        # Read input file
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            old_automations = yaml.safe_load(f)

        if not old_automations:
            print(f"Error: {INPUT_FILE} is empty or invalid")
            sys.exit(1)

        # Convert each automation
        new_automations = []
        for old_auto in old_automations:
            try:
                new_auto = convert_automation(old_auto)
                new_automations.append(new_auto)
                print(f"✓ Converted: {old_auto['alias']}")
            except Exception as e:
                print(f"✗ Error converting {old_auto.get('alias', 'unknown')}: {e}")

        # Write output file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(new_automations, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"\n✓ Conversion complete!")
        print(f"  Input:  {INPUT_FILE} ({len(old_automations)} automations)")
        print(f"  Output: {OUTPUT_FILE} ({len(new_automations)} automations)")
        print(f"\nNext steps:")
        print(f"1. Review {OUTPUT_FILE}")
        print(f"2. Copy the content to your Home Assistant automations.yaml")
        print(f"3. Reload automations in Home Assistant")

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found")
        print(f"Please create {INPUT_FILE} and paste your old automations there")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
