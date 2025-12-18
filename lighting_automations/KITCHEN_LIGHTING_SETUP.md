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

### 2. Find Your Tag Friendly Names

Since you already have all 80+ tags registered in Home Assistant's tag registry, this is easy!

**In Home Assistant:**
1. Go to **Settings** → **Tags**
2. Find your 18 playlist tags in the list
3. Note down their friendly names (e.g., `rock_playlist`, `jazz_playlist`, etc.)

**Tip:** If your tag friendly names follow a pattern, this will be quick! For example, if they're named like:
- `80s_playlist`, `90s_playlist`, `00s_playlist`
- `rock_playlist`, `jazz_playlist`, `house_playlist`

Then you just need to match them to the placeholders in the automation file.

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

# Tag friendly names - Replace with your actual tag names from Settings → Tags
# These appear in TWO places: trigger section (line ~300) and conditions (line ~330+)

# ENERGETIC CATEGORY (14 playlists)
80s_playlist        → your_actual_80s_tag_name
90s_playlist        → your_actual_90s_tag_name
00s_playlist        → your_actual_00s_tag_name
10s_playlist        → your_actual_10s_tag_name
20s_playlist        → your_actual_20s_tag_name
disco_playlist      → your_actual_disco_tag_name
rock_playlist       → your_actual_rock_tag_name
house_playlist      → your_actual_house_tag_name
hiphop_playlist     → your_actual_hiphop_tag_name
party_playlist      → your_actual_party_tag_name
rap_playlist        → your_actual_rap_tag_name
singalong_playlist  → your_actual_singalong_tag_name
mgp_playlist        → your_actual_mgp_tag_name
dansk_top_playlist  → your_actual_dansk_top_tag_name

# CHILL CATEGORY (4 playlists)
chill_playlist      → your_actual_chill_tag_name
jazz_playlist       → your_actual_jazz_tag_name
elevator_playlist   → your_actual_elevator_tag_name
lounge_playlist     → your_actual_lounge_tag_name
```

**Note:** Each tag name appears in TWO places in the file:
1. In the `trigger:` section (~line 301-316)
2. In the `conditions:` for each playlist (~line 331+)

Use find/replace to update both at once!

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
