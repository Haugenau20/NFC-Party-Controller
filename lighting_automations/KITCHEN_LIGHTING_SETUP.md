# Kitchen Playlist-Based Lighting Setup Guide

Complete setup guide for the category-based kitchen lighting system that responds to playlist NFC scans.

---

## Overview

The kitchen lighting system provides:
- **Playlist-responsive lighting** - Colors change based on which music is playing
- **Category-based color palettes** - Energetic vs Chill playlists get different vibes
- **Color rotation** - Colors cycle through palettes to keep things fresh
- **Smart light handling** - Aurelle (white only) and Lightstrip (full color) controlled separately
- **Optional extra lightstrip** - Code included but commented out for future installation

---

## How It Works

### Categories & Playlists

**Energetic** (14 playlists):
- Decades: 80s, 90s, 00s, 10s, 20s
- Dance: Disco, House
- Urban: HipHop, Rap
- High Energy: Rock, Party, Singalong, MGP, Dansk Top

**Chill** (4 playlists):
- Relaxed: Chill, Jazz, Elevator, Lounge

### Color Palettes

**Energetic Palette** (rotates each scan):
1. Electric Blue - Bright and energetic
2. Hot Magenta - Bold and vibrant
3. Vibrant Orange - Warm energy
4. Lime Green - Fresh and lively
5. Purple - Deep saturation

**Chill Palette** (rotates each scan):
1. Cool Teal - Calm and relaxing
2. Soft Purple - Gentle ambiance
3. Warm White - Cozy feel
4. Deep Blue - Tranquil depth

### Light Behavior

**Hue Aurelle (Ceiling Panel):**
- White ambiance only (no color capability)
- Energetic: Cool white at 86% brightness
- Chill: Warm white at 59% brightness

**Hue Lightstrip:**
- Full RGB color
- Energetic: 78% brightness with saturated colors
- Chill: 63% brightness with calm colors

**Extra 2m Lightstrip (Optional):**
- Matches main lightstrip behavior
- Code is commented out until installed

---

## Installation Steps

### 1. Find Your Hue Light Entity IDs

In Home Assistant:
1. Go to **Settings** → **Devices & Services** → **Philips Hue**
2. Find your kitchen lights:
   - Hue Aurelle 60x60cm ceiling panel
   - Hue lightstrip with colors
   - Extra 2m lightstrip (if installed)
3. Click each light and copy the **Entity ID**

### 2. Get Your NFC Tag IDs

You need the tag UIDs for all 18 playlist cards. For each one:
1. Scan the NFC card with Device 2 (Kitchen)
2. Go to **Settings** → **System** → **Logs**
3. Look for `tag_scanned` events
4. Copy the `tag_id` value (e.g., `04-23-D3-2A-B1-49-80`)

Or use the Home Assistant NFC tag manager if you've already registered them.

### 3. Update Placeholders

**File: `kitchen_input_helpers.yaml`**
- No placeholders! This file is ready to use as-is.

**File: `kitchen_playlist_lighting.yaml`**

Replace these placeholders:

```yaml
# Light entities
light.PLACEHOLDER_KITCHEN_AURELLE          → light.your_actual_aurelle_entity
light.PLACEHOLDER_KITCHEN_LIGHTSTRIP       → light.your_actual_lightstrip_entity
light.PLACEHOLDER_KITCHEN_LIGHTSTRIP_EXTRA → light.your_actual_extra_lightstrip_entity (OPTIONAL)

# NFC Tag IDs - Energetic Category (14 playlists)
PLACEHOLDER_TAG_80S        → your_80s_tag_uid
PLACEHOLDER_TAG_90S        → your_90s_tag_uid
PLACEHOLDER_TAG_00S        → your_00s_tag_uid
PLACEHOLDER_TAG_10S        → your_10s_tag_uid
PLACEHOLDER_TAG_20S        → your_20s_tag_uid
PLACEHOLDER_TAG_DISCO      → your_disco_tag_uid
PLACEHOLDER_TAG_ROCK       → your_rock_tag_uid
PLACEHOLDER_TAG_HOUSE      → your_house_tag_uid
PLACEHOLDER_TAG_HIPHOP     → your_hiphop_tag_uid
PLACEHOLDER_TAG_PARTY      → your_party_tag_uid
PLACEHOLDER_TAG_RAP        → your_rap_tag_uid
PLACEHOLDER_TAG_SINGALONG  → your_singalong_tag_uid
PLACEHOLDER_TAG_MGP        → your_mgp_tag_uid
PLACEHOLDER_TAG_DANSK_TOP  → your_dansk_top_tag_uid

# NFC Tag IDs - Chill Category (4 playlists)
PLACEHOLDER_TAG_CHILL      → your_chill_tag_uid
PLACEHOLDER_TAG_JAZZ       → your_jazz_tag_uid
PLACEHOLDER_TAG_ELEVATOR   → your_elevator_tag_uid
PLACEHOLDER_TAG_LOUNGE     → your_lounge_tag_uid
```

### 4. Copy Files to Home Assistant

Copy all three YAML files to your Home Assistant configuration directory:

```bash
cp kitchen_input_helpers.yaml /config/
cp kitchen_playlist_lighting.yaml /config/
```

### 5. Update `configuration.yaml`

Add these includes:

```yaml
# Kitchen Lighting
input_select: !include kitchen_input_helpers.yaml
automation kitchen_lighting: !include kitchen_playlist_lighting.yaml
script: !include kitchen_playlist_lighting.yaml
```

Or if you already have automation/script/input_select includes, merge accordingly.

### 6. Restart Home Assistant

**Settings** → **System** → **Restart**

### 7. Verify Setup

After restart, check:
1. **Developer Tools** → **States** → Search for:
   - `input_select.kitchen_energetic_color_rotation`
   - `input_select.kitchen_chill_color_rotation`
2. **Settings** → **Automations** → Look for:
   - "Kitchen - Playlist-Based Lighting Control"
3. **Settings** → **Scripts** → Look for:
   - `kitchen_energetic_electric_blue`, etc.
   - `kitchen_chill_cool_teal`, etc.

---

## Testing Before the Party

### Test Individual Colors

1. Go to **Developer Tools** → **Services**
2. Call script services manually:
   - `script.kitchen_energetic_electric_blue`
   - `script.kitchen_chill_cool_teal`
   - etc.
3. Watch your kitchen lights change!

### Test Playlist Scans

1. Scan an "Energetic" playlist card (e.g., Rock, 80s, Party)
   - Lights should change to current energetic color
   - Color rotation should advance to next color
2. Scan another "Energetic" playlist card
   - Should get the NEXT color in the energetic palette
3. Scan a "Chill" playlist card (e.g., Jazz, Lounge)
   - Lights should change to current chill color
   - Chill rotation advances independently

### Test Color Rotation

Scan the same category playlist 5+ times:
- **Energetic**: Blue → Magenta → Orange → Green → Purple → Blue (cycles)
- **Chill**: Teal → Purple → White → Blue → Teal (cycles)

---

## Adding the Extra 2m Lightstrip Later

When you install the extra lightstrip:

1. Find its entity ID in Home Assistant (Hue integration)
2. Open `kitchen_playlist_lighting.yaml`
3. Replace `light.PLACEHOLDER_KITCHEN_LIGHTSTRIP_EXTRA` with actual entity ID
4. **Uncomment all lines that start with `##`**
   - Search for `##` in the file
   - Remove the `##` prefix from each line
5. Save and restart Home Assistant

The extra lightstrip will now sync with the main lightstrip!

---

## Customization Tips

### Adjusting Colors

Find the RGB color values in the script sections and modify:

```yaml
rgb_color: [255, 0, 144]  # [Red, Green, Blue] - each 0-255
```

Popular party colors:
- `[255, 0, 0]` - Red
- `[0, 255, 0]` - Green
- `[0, 0, 255]` - Blue
- `[255, 255, 0]` - Yellow
- `[0, 255, 255]` - Cyan
- `[255, 0, 255]` - Magenta

### Adjusting Brightness

```yaml
brightness: 200  # 0-255 scale (78% = 200)
```

Common levels:
- 255 = 100%
- 200 = 78%
- 150 = 59%
- 100 = 39%

### Adjusting Aurelle White Temperature

```yaml
color_temp: 250  # Lower = cooler white, Higher = warmer white
```

Range: 153 (coolest) to 500 (warmest)
- 250 = Cool white (energetic)
- 400 = Warm white (chill)

### Adding New Playlists

1. Decide if it's "Energetic" or "Chill"
2. Get the NFC tag UID
3. Add a new condition block in `kitchen_playlist_lighting.yaml`:

```yaml
# Your New Playlist
- conditions:
    - condition: template
      value_template: "{{ trigger.event.data.tag_id == 'YOUR_TAG_UID' }}"
  sequence:
    - service: "script.kitchen_energetic_{{ states('input_select.kitchen_energetic_color_rotation') | lower | replace(' ', '_') }}"
    - service: input_select.select_next
      target:
        entity_id: input_select.kitchen_energetic_color_rotation
      data:
        cycle: true
```

(Change `energetic` to `chill` if it's a chill playlist)

### Moving a Playlist Between Categories

Just copy its condition block from one category section to the other, and change the script service and input_select entity accordingly.

---

## Troubleshooting

### Lights don't change when scanning playlist card
- Verify tag UID is correct (check logs)
- Ensure Device 2 ID matches in automation condition
- Check that playlist card works for music (if music plays, tag is recognized)

### Wrong colors appear
- Check which input_select is being used (energetic vs chill)
- Verify RGB values in script match what you expect
- Aurelle can only show white - color changes won't be visible on it

### Color rotation doesn't advance
- Check input_select helpers exist in **Developer Tools** → **States**
- Verify `select_next` service call is present in sequence
- Check Home Assistant logs for errors

### Extra lightstrip doesn't work after uncommenting
- Ensure entity ID is correct
- Verify all `##` prefixes were removed
- Check that lightstrip is detected in Hue integration

---

## Color Palette Reference

Quick reference for all colors:

**Energetic:**
- Electric Blue: `[0, 191, 255]`
- Hot Magenta: `[255, 0, 144]`
- Vibrant Orange: `[255, 140, 0]`
- Lime Green: `[50, 205, 50]`
- Purple: `[138, 43, 226]`

**Chill:**
- Cool Teal: `[0, 150, 150]`
- Soft Purple: `[147, 112, 219]`
- Warm White: `[255, 228, 181]`
- Deep Blue: `[25, 25, 112]`

---

## What Happens During the Party

### Typical Flow:

1. **Guest arrives, scans "Party" card** → Kitchen lights turn hot magenta
2. **Someone wants chill vibes, scans "Jazz" card** → Lights change to cool teal
3. **Back to dancing, scans "House" card** → Lights cycle to next energetic color (vibrant orange)
4. **Scan "Rock" card** → Lights advance again (lime green)
5. **Scan "Chill" card** → Back to chill palette (soft purple)

Every scan within a category advances the color rotation, keeping the kitchen visually dynamic without being repetitive!

---

**Created for New Year's Party 2025** 🎉
Device 2 (Kitchen) - Experimental & Playful Breakout Room
