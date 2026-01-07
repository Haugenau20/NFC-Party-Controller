# Living Room Party Lighting Setup Guide

Complete setup guide for the automated time-based party lighting system with NFC overrides.

---

## Overview

The living room lighting system provides:
- **Automated time-based transitions** for your New Year's party (5pm - midnight+)
- **6 distinct party phases** with carefully designed color schemes
- **NFC override cards** for manual control when needed
- **Special midnight countdown sequence** with dramatic lighting effects
- **5 synchronized lights** - Signe, Ensis Up/Down, Beyond Up/Down

---

## Party Timeline

| Time | Phase | Vibe |
|------|-------|------|
| 5:00 PM - 6:30 PM | **Arrival** | Warm and welcoming with colorful accents |
| 6:30 PM - 8:00 PM | **Dinner** | Cozy, warm, dinner-focused |
| 8:00 PM - 10:00 PM | **Post-Dinner** | Energy building, transition to party mode |
| 10:00 PM - 11:30 PM | **Prime Time** | Energetic, saturated, peak party mode |
| 11:30 PM - 11:59 PM | **Countdown Prep** | Building anticipation for midnight |
| 11:59 PM - 12:01 AM | **Midnight Countdown** | 60-second dramatic sequence |
| 12:01 AM onwards | **After Party** | Celebratory but sustainable |

---

## Party Phases (Detailed)

### 1. Arrival (5:00 PM - 6:30 PM)
**Vibe:** Warm and welcoming with colorful accents (not wild)

- **Signe Floor Lamp:** Light coral at 75% - welcoming accent
- **Ensis Up (Ceiling Wash):** Warm amber at 70% - ambient ceiling glow
- **Ensis Down (Task Light):** Soft warm white at 75% - functional light to see
- **Beyond Up (Table Accent):** Soft peach at 67% - adds warmth and depth
- **Beyond Down (Table Light):** Soft warm white at 70% - table illumination
- **Purpose:** Create inviting atmosphere as guests arrive

### 2. Dinner (6:30 PM - 8:00 PM)
**Vibe:** Cozy, warm, dinner-focused

- **Signe Floor Lamp:** Dimmed warm amber at 55% - cozy but not distracting
- **Ensis Up (Ceiling Wash):** Soft warm amber at 51% - subtle ambiance
- **Ensis Down (Task Light):** Bright warm white at 78% - need to see food!
- **Beyond Up (Table Accent):** Very soft warm amber at 47% - very subtle
- **Beyond Down (Table Light):** Warm white at 75% - functional table lighting
- **Purpose:** Functional lighting for dinner without being too bright

### 3. Post-Dinner (8:00 PM - 10:00 PM)
**Vibe:** Energy building, transition to party mode

- **Signe Floor Lamp:** Warm amber/orange at 70% - energy rising
- **Ensis Up (Ceiling Wash):** Warm amber/orange at 67% - matches Signe for cohesive vibe
- **Ensis Down (Task Light):** Warm white at 70% - functional lighting
- **Beyond Up (Table Accent):** Warm amber at 63% - matches Signe
- **Beyond Down (Table Light):** Warm white at 67% - table lighting
- **Purpose:** Transition from dinner relaxation to dancing energy

### 4. Prime Time (10:00 PM - 11:30 PM)
**Vibe:** Energetic, saturated, peak party mode

- **Signe Floor Lamp:** Deep purple/magenta at 78% - bold statement
- **Ensis Up (Ceiling Wash):** Deep purple/magenta at 78% - dramatic colorful ceiling
- **Ensis Down (Task Light):** Soft purple at 47% (dimmed) - less functional light, more vibe!
- **Beyond Up (Table Accent):** Deep purple at 75% - matches energy
- **Beyond Down (Table Light):** Soft purple at 51% - table accent
- **Purpose:** Peak party energy, dancing, celebration

### 5. Countdown Prep (11:30 PM - 11:59 PM)
**Vibe:** Building anticipation for midnight

- **Signe Floor Lamp:** Goldenrod at 59% - starting dimmer (will ramp up)
- **Ensis Up (Ceiling Wash):** Gold at 59% - building energy
- **Ensis Down (Task Light):** Gold at 55% - everyone coordinated
- **Beyond Up (Table Accent):** Goldenrod at 57% - matches Signe
- **Beyond Down (Table Light):** Gold at 55% - coordinated
- **Purpose:** Set stage for countdown sequence

### 6. After Party (12:01 AM onwards)
**Vibe:** Celebratory but sustainable

- **Signe Floor Lamp:** Bright gold/champagne at 78% - celebration!
- **Ensis Up (Ceiling Wash):** Bright gold at 86% - celebration mode
- **Ensis Down (Task Light):** Light yellow at 86% - everyone can see to celebrate
- **Beyond Up (Table Accent):** Bright gold at 82% - matches celebration
- **Beyond Down (Table Light):** Light yellow at 82% - bright and cheerful
- **Purpose:** Post-midnight celebration, sustainable for hours

---

## Light Design Philosophy

**Functional vs. Ambient:**
- **Ensis Down & Beyond Down:** Functional overhead/table lighting (stable, helps people see)
- **Ensis Up & Beyond Up:** Ambient ceiling/table wash (colorful, matches vibe)
- **Signe:** Main color statement piece (sets the overall mood)

**During Different Phases:**
- **Dinner:** Functional lights (Down) are brighter for eating
- **Prime Time:** Functional lights (Down) are dimmed for party vibe
- **Countdown:** All lights synchronized for dramatic effect

---

## Special Feature: Midnight Countdown

At **11:59:00 PM**, an automatic 60-second countdown sequence begins with all 5 lights synchronized:

1. **0:00-0:10** - All lights start at 20% gold (dim)
2. **0:10-0:20** - Gradual ramp to 40% gold
3. **0:20-0:30** - Gradual ramp to 60% gold
4. **0:30-0:40** - Gradual ramp to 80% gold
5. **0:40-0:50** - Faster pulsing: 90% → 80% → 90% → 80%
6. **0:50-0:58** - Build to 100% gold intensity
7. **0:58-1:00** - Maximum brightness, building tension
8. **1:00 (Midnight!)** - Pure white flash at 100% (instant)
9. **1:00+** - Settle into After Party celebratory colors

---

## Installation Steps

### 1. Find Your Hue Light Entity IDs

In Home Assistant:
1. Go to **Settings** → **Devices & Services** → **Philips Hue**
2. Find your living room lights:
   - **Hue Signe** floor lamp
   - **Hue Ensis** hanging lamp - has TWO separate entities:
     - One for the "Up" light (ceiling wash)
     - One for the "Down" light (task lighting)
   - **Hue Beyond** table lamp - has TWO separate entities:
     - One for the "Up" light (ambient)
     - One for the "Down" light (table task lighting)
3. Click each light and copy the **Entity ID**
   - Example: `light.living_room_signe`
   - Example: `light.living_room_ensis_up`
   - Example: `light.living_room_beyond_down`

### 2. Update Placeholders in Configuration Files

**File: `living_room_party_lighting.yaml`**

Replace these placeholders:
```yaml
# Light entities (5 total)
light.PLACEHOLDER_LIVING_ROOM_SIGNE        → light.your_actual_signe_entity
light.PLACEHOLDER_LIVING_ROOM_ENSIS_UP     → light.your_actual_ensis_up_entity
light.PLACEHOLDER_LIVING_ROOM_ENSIS_DOWN   → light.your_actual_ensis_down_entity
light.PLACEHOLDER_LIVING_ROOM_BEYOND_UP    → light.your_actual_beyond_up_entity
light.PLACEHOLDER_LIVING_ROOM_BEYOND_DOWN  → light.your_actual_beyond_down_entity

# NFC tag IDs (optional - only if you want override cards)
PLACEHOLDER_TAG_ARRIVAL      → your_nfc_tag_uid_1
PLACEHOLDER_TAG_DINNER       → your_nfc_tag_uid_2
PLACEHOLDER_TAG_POST_DINNER  → your_nfc_tag_uid_3
PLACEHOLDER_TAG_PRIME_TIME   → your_nfc_tag_uid_4
PLACEHOLDER_TAG_AFTER_PARTY  → your_nfc_tag_uid_5
```

**File: `living_room_midnight_countdown.yaml`**

Replace these placeholders:
```yaml
# Light entities (same 5 as above)
light.PLACEHOLDER_LIVING_ROOM_SIGNE        → light.your_actual_signe_entity
light.PLACEHOLDER_LIVING_ROOM_ENSIS_UP     → light.your_actual_ensis_up_entity
light.PLACEHOLDER_LIVING_ROOM_ENSIS_DOWN   → light.your_actual_ensis_down_entity
light.PLACEHOLDER_LIVING_ROOM_BEYOND_UP    → light.your_actual_beyond_up_entity
light.PLACEHOLDER_LIVING_ROOM_BEYOND_DOWN  → light.your_actual_beyond_down_entity

# NFC tag ID (optional - for manual countdown trigger)
PLACEHOLDER_TAG_MIDNIGHT_COUNTDOWN  → your_nfc_tag_uid_6
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
   - "Living Room - Auto Arrival (5pm)"
   - "Living Room - Auto Dinner (6:30pm)"
   - "Living Room - Auto Post-Dinner (8pm)"
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
   - `living_room_arrival`
   - `living_room_dinner`
   - `living_room_post_dinner`
   - `living_room_prime_time`
   - `living_room_countdown_prep`
   - `living_room_after_party`
3. Watch all 5 lights change together!

### Test Midnight Countdown

1. **Option A:** Run the script manually
   - Go to Scripts → `living_room_midnight_countdown`
   - Click "Run Script"
   - Watch the 60-second sequence

2. **Option B:** Use NFC card (if configured)
   - Scan the midnight countdown override card

3. **Option C:** Temporarily change the time trigger
   - Edit automation to trigger in 1 minute
   - Test, then change back to `23:59:00`

### Test Time-Based Triggers

Temporarily change one automation's time trigger to test:
1. Edit "Living Room - Auto Arrival"
2. Change `at: "17:00:00"` to a time 1 minute from now
3. Wait and verify it triggers
4. Change back to `17:00:00`

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
- **Card 1:** "Arrival" (warm welcoming vibe)
- **Card 2:** "Dinner" (functional dining light)
- **Card 3:** "Post-Dinner" (energy building)
- **Card 4:** "Prime Time" (peak party mode)
- **Card 5:** "After Party" (celebration mode)
- **Card 6:** "Midnight Countdown" (manual trigger)

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

Current phase colors:
- Arrival: Light coral `[255, 160, 122]`, warm amber `[255, 180, 100]`
- Dinner: Warm amber `[255, 150, 80]`, warm white `[255, 220, 180]`
- Post-Dinner: Warm amber/orange `[255, 147, 41]`, warm white `[255, 197, 143]`
- Prime Time: Deep purple/magenta `[138, 43, 226]`, soft purple `[180, 100, 230]`
- Countdown Prep: Goldenrod `[218, 165, 32]`, gold `[255, 215, 0]`
- After Party: Gold `[255, 215, 0]`, light yellow `[255, 255, 224]`

### Adjusting Brightness

Brightness values: 0-255 (0 = off, 255 = 100%)
- 51 = 20%
- 102 = 40%
- 120 = 47%
- 140 = 55%
- 153 = 60%
- 170 = 67%
- 180 = 70%
- 190 = 75%
- 200 = 78%
- 204 = 80%
- 220 = 86%
- 230 = 90%
- 255 = 100%

### Adjusting Times

Edit the time triggers in the automation sections:
```yaml
trigger:
  - platform: time
    at: "17:00:00"  # 24-hour format: HH:MM:SS (5:00 PM)
```

Party timeline suggestions:
- Start earlier: Change 17:00:00 to 16:00:00 (4 PM)
- Dinner later: Change 18:30:00 to 19:00:00 (7 PM)
- Prime Time longer: Keep at 22:00:00 but extend Countdown Prep to 23:45:00

### Adjusting Transitions

Transition = smooth fade duration in seconds:
```yaml
transition: 3   # 3-second fade (standard)
transition: 0   # Instant change
transition: 5   # 5-second fade (smooth dinner transition)
transition: 10  # 10-second fade (countdown prep)
```

---

## Troubleshooting

### Lights don't change at scheduled time
- Verify Home Assistant time zone is correct (**Settings** → **System** → **General**)
- Check automation is enabled (toggle switch on)
- Check Home Assistant logs for errors
- Verify light entity IDs are correct

### Only some lights change
- Check that all 5 entity IDs are correct
- Verify lights are powered on and reachable
- Check Hue bridge connection
- Test each light individually in Hue app

### Midnight countdown doesn't start
- Verify automation trigger time is `23:59:00`
- Check that `living_room_after_party` script exists (countdown calls it at the end)
- Test script manually first

### Colors look wrong
- Some Hue bulbs have different color capabilities
- Adjust RGB values to match your bulb's color gamut
- Use Hue app to find preferred colors, then replicate in Home Assistant
- White ambiance bulbs (if any) can't show colors - only brightness

### NFC override doesn't work
- Verify tag UID is correct (check logs: **Settings** → **System** → **Logs**)
- Ensure button entity exists: `button.nfc_party_controller_1_play_success`
- Test script directly to isolate issue (Scripts → Run Script)
- Verify Device 1 is scanning the tag (not Device 2)

### Countdown timing is off
- The countdown sequence is exactly 60 seconds from start to midnight flash
- If started at 11:59:00, the white flash occurs at 12:00:00
- Test manually to verify timing before party night

---

## What Happens During the Party

### Typical Flow:

**5:00 PM** - Arrival phase begins automatically (warm, welcoming)

**6:30 PM** - Dinner phase begins automatically (functional lighting for eating)

**8:00 PM** - Post-Dinner phase begins (energy starts building, warmer colors)

**10:00 PM** - Prime Time hits (purple/magenta, peak party energy!)

**11:30 PM** - Countdown Prep begins (everything turns gold, anticipation building)

**11:59:00 PM** - Midnight Countdown starts (60-second synchronized sequence)

**12:00:00 AM** - PURE WHITE FLASH - Happy New Year! 🎉

**12:00:01 AM** - After Party phase (bright gold celebration colors)

### Manual Override Scenarios:

- **Guests arrive early?** Scan "Arrival" card to start early
- **Dinner runs late?** Scan "Dinner" card to extend dining phase
- **Want to pump energy early?** Scan "Prime Time" card anytime
- **Test countdown?** Scan "Midnight Countdown" card during setup

---

## Next Steps

Once living room is working:
- [ ] Test all 6 phases before the party
- [ ] Test midnight countdown sequence
- [ ] Label your NFC override cards (if using)
- [ ] Verify all 5 lights respond correctly
- [ ] Consider testing the full timeline 1 day before party
- [ ] Kitchen lighting is separate - see `KITCHEN_LIGHTING_SETUP.md`

---

**Created for New Year's Party 2025** 🎉
Device 1 (Living Room) - Automated Time-Based Lighting with 5 Synchronized Lights
