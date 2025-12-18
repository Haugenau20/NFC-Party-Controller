# Living Room Party Lighting Setup Guide

Complete setup guide for the automated time-based party lighting system with NFC overrides.

---

## Overview

The living room lighting system provides:
- **Automated time-based transitions** for your New Year's party
- **4 distinct party phases** with carefully designed color schemes
- **NFC override cards** for manual control when needed
- **Special midnight countdown sequence** with dramatic lighting effects

---

## Party Phases

### 1. Early Evening (8:00 PM - 10:00 PM)
**Vibe:** Warm, welcoming, conversational

- **Signe Floor Lamp:** Warm amber/orange gradient at 70%
- **Ensis Hanging Lamp:** Warm white at 70%
- **Purpose:** Creates inviting atmosphere as guests arrive

### 2. Prime Time (10:00 PM - 11:30 PM)
**Vibe:** Energetic, saturated, party mode

- **Signe Floor Lamp:** Deep purple/magenta at 78%
- **Ensis Hanging Lamp:** White accent at 70%
- **Purpose:** Peak party energy, dancing, celebration

### 3. Countdown Prep (11:30 PM - 11:59 PM)
**Vibe:** Building anticipation for midnight

- **Signe Floor Lamp:** Goldenrod starting at 60%
- **Ensis Hanging Lamp:** Gold starting at 60%
- **Purpose:** Transition to midnight celebration

### 4. After Party (12:01 AM onwards)
**Vibe:** Celebratory but sustainable

- **Signe Floor Lamp:** Bright gold/champagne at 78%
- **Ensis Hanging Lamp:** Light yellow at 86%
- **Purpose:** Post-midnight celebration, can stay here or revert to Prime Time

---

## Special Feature: Midnight Countdown

At **11:59:00 PM**, an automatic 60-second countdown sequence begins:

1. **0:00-0:40** - Gradual brightness ramp from 20% → 80%
2. **0:40-0:58** - Faster pulsing between 80% → 90%
3. **0:58-1:00** - Build to 100% intensity
4. **1:00 (Midnight!)** - Pure white flash
5. **1:00+** - Settle into After Party colors

---

## Installation Steps

### 1. Find Your Hue Light Entity IDs

In Home Assistant:
1. Go to **Settings** → **Devices & Services** → **Philips Hue**
2. Find your living room lights:
   - Hue Signe floor lamp
   - Hue Ensis hanging lamp
3. Click each light and copy the **Entity ID** (e.g., `light.living_room_signe`)

### 2. Update Placeholders in Configuration Files

**File: `living_room_party_lighting.yaml`**

Replace these placeholders:
```yaml
# Light entities
light.PLACEHOLDER_LIVING_ROOM_SIGNE  → light.your_actual_signe_entity
light.PLACEHOLDER_LIVING_ROOM_ENSIS  → light.your_actual_ensis_entity

# NFC tag IDs (optional - only if you want override cards)
PLACEHOLDER_TAG_EARLY_EVENING  → your_nfc_tag_uid_1
PLACEHOLDER_TAG_PRIME_TIME     → your_nfc_tag_uid_2
PLACEHOLDER_TAG_AFTER_PARTY    → your_nfc_tag_uid_3
```

**File: `living_room_midnight_countdown.yaml`**

Replace these placeholders:
```yaml
# Light entities (same as above)
light.PLACEHOLDER_LIVING_ROOM_SIGNE  → light.your_actual_signe_entity
light.PLACEHOLDER_LIVING_ROOM_ENSIS  → light.your_actual_ensis_entity

# NFC tag ID (optional - for manual countdown trigger)
PLACEHOLDER_TAG_MIDNIGHT_COUNTDOWN  → your_nfc_tag_uid_4
```

### 3. Copy Files to Home Assistant

Copy both YAML files to your Home Assistant configuration directory:

```bash
# If using SSH/terminal access
cp living_room_party_lighting.yaml /config/
cp living_room_midnight_countdown.yaml /config/
```

Or use the Home Assistant File Editor add-on to upload the files.

### 4. Update `configuration.yaml`

Add these lines to include the new automation files:

```yaml
# Living Room Party Lighting
automation: !include_dir_merge_list .
script: !include_dir_merge_named .
```

Or manually include them:

```yaml
automation living_room_party: !include living_room_party_lighting.yaml
automation living_room_midnight: !include living_room_midnight_countdown.yaml

script: !include living_room_party_lighting.yaml
```

### 5. Restart Home Assistant

**Settings** → **System** → **Restart**

### 6. Verify Automations

After restart:
1. Go to **Settings** → **Automations & Scenes**
2. Verify these automations appear:
   - "Living Room - Auto Early Evening (8pm)"
   - "Living Room - Auto Prime Time (10pm)"
   - "Living Room - Auto Countdown Prep (11:30pm)"
   - "Living Room - Auto After Party (12:01am)"
   - "Living Room - Auto Midnight Countdown (11:59pm)"
   - NFC override automations (if configured)

---

## Testing Before the Party

### Test Individual Phases

1. Go to **Settings** → **Automations & Scenes** → **Scripts**
2. Find and run these scripts manually:
   - `living_room_early_evening`
   - `living_room_prime_time`
   - `living_room_countdown_prep`
   - `living_room_after_party`

### Test Midnight Countdown

1. **Option A:** Run the script manually
   - Go to Scripts → `living_room_midnight_countdown`
   - Click "Run Script"

2. **Option B:** Use NFC card (if configured)
   - Scan the midnight countdown override card

3. **Option C:** Temporarily change the time trigger
   - Edit automation to trigger in 1 minute
   - Test, then change back to `23:59:00`

### Test Time-Based Triggers

Temporarily change one automation's time trigger to test:
1. Edit "Living Room - Auto Early Evening"
2. Change `at: "20:00:00"` to a time 1 minute from now
3. Wait and verify it triggers
4. Change back to `20:00:00`

---

## NFC Override Cards (Optional)

If you want manual control via NFC cards:

### Getting NFC Tag UIDs

1. Scan an NFC tag with Device 1
2. Go to **Settings** → **System** → **Logs**
3. Look for `tag_scanned` events
4. Copy the `tag_id` value (e.g., `04-23-D3-2A-B1-49-80`)

### Assign Card Purposes

Create physical labels for your cards:
- **Card 1:** "Early Evening" (warm arrival vibe)
- **Card 2:** "Prime Time" (peak party mode)
- **Card 3:** "After Party" (celebration mode)
- **Card 4:** "Midnight Countdown" (manual trigger)

### Update Configuration

Replace the placeholder tag IDs with your actual UIDs in both YAML files.

---

## Customization Tips

### Adjusting Colors

RGB color format: `[Red, Green, Blue]` where each value is 0-255

Common party colors:
```yaml
[255, 0, 0]      # Red
[255, 165, 0]    # Orange
[255, 215, 0]    # Gold
[255, 192, 203]  # Pink
[138, 43, 226]   # Purple
[0, 191, 255]    # Deep sky blue
[50, 205, 50]    # Lime green
[255, 255, 255]  # White
```

### Adjusting Brightness

Brightness values: 0-255 (0 = off, 255 = 100%)
- 51 = 20%
- 102 = 40%
- 153 = 60%
- 204 = 80%
- 230 = 90%
- 255 = 100%

### Adjusting Times

Edit the time triggers in the automation sections:
```yaml
trigger:
  - platform: time
    at: "20:00:00"  # 24-hour format: HH:MM:SS
```

### Adjusting Transitions

Transition = smooth fade duration in seconds:
```yaml
transition: 3  # 3-second fade
transition: 0  # Instant change
transition: 10 # 10-second fade
```

---

## Troubleshooting

### Lights don't change at scheduled time
- Verify Home Assistant time zone is correct
- Check automation is enabled (toggle switch on)
- Check Home Assistant logs for errors

### Midnight countdown doesn't start
- Verify automation trigger time is `23:59:00`
- Check that `living_room_after_party` script exists (countdown calls it at the end)

### Colors look wrong
- Some Hue bulbs have different color capabilities
- Adjust RGB values to match your bulb's range
- Use Hue app to find preferred colors, then match in HA

### NFC override doesn't work
- Verify tag UID is correct (check logs)
- Ensure button entity exists: `button.nfc_party_controller_1_play_success`
- Test script directly to isolate issue

---

## Next Steps

Once living room is working:
- [ ] Test all phases before the party
- [ ] Label your NFC override cards
- [ ] Move on to kitchen lighting integration (playlist-based colors)
- [ ] Consider adding the extra 2m lightstrip to kitchen

---

**Created for New Year's Party 2025** 🎉
Device 1 (Living Room) - Automated & Override Control
