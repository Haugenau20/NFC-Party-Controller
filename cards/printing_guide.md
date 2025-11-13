# NFC Card Printing Guide

This guide explains how to design, print, and assemble the physical NFC cards for the party controller.

## Materials Needed

### Hardware
- **150x NTAG215 NFC tags** (30mm circular stickers on roll)
- **Card stock or business cards** (85x55mm, 300gsm recommended)
- **Laser or inkjet printer** (color recommended for better design)
- **Laminator** (optional, for durability)

### Software
- **Design software**: Adobe Illustrator, Inkscape, or Canva
- **NFC Tools app** (iOS/Android) for initial tag registration

## Card Design Specifications

### Dimensions
- **Standard size**: 85mm x 55mm (credit card size)
- **NFC tag placement**: Center or near-center (30mm circular sticker)
- **Print bleed**: 3mm if using professional printing

### Design Elements

**Front of Card**:
- Playlist/action name (large, readable font)
- Mood/category indicator (color-coded)
- Icon or album art representation
- Optional: NFC symbol to indicate scan area

**Back of Card**:
- Tag number (for reference to `tag_mapping.csv`)
- Brief description of action
- Optional: QR code linking to Spotify playlist

### Color Coding Suggestions

| Mood/Category | Color Scheme | Suggested Hex |
|---------------|--------------|---------------|
| Energetic | Red/Orange | #FF5733 |
| Chill | Blue/Teal | #36D7B7 |
| Romantic | Pink/Purple | #E056FD |
| Focus | Green/Yellow | #6C757D |
| System Control | Gray/Black | #2C3E50 |

## Card Template Layout

```
┌─────────────────────────────────────────┐
│                                         │
│          ENERGETIC PARTY MIX            │
│                                         │
│              [Icon/Art]                 │
│                                         │
│           [ NFC Tag Area ]              │
│                                         │
│         Scan to start the party!        │
│                                         │
└─────────────────────────────────────────┘
```

## Printing Process

### 1. Design Your Cards

1. Open design software
2. Create 85x55mm artboard/page
3. Design card front and back
4. Export as high-resolution PDF (300 DPI minimum)

**Template tips**:
- Use card template generator tools online
- Design 8-10 cards per A4 sheet for efficient printing
- Leave space for NFC tag placement (30mm circle)
- Use high-contrast text for readability

### 2. Print Cards

**Laser Printer** (Recommended):
- Use 300gsm card stock
- Print with highest quality settings
- Allow ink to fully dry before handling

**Inkjet Printer**:
- Use inkjet-compatible card stock
- Consider waterproof spray coating after printing
- Print test page first to check colors

**Professional Printing** (Best Quality):
- Services like Moo, VistaPrint, or local print shops
- Upload PDF with crop marks
- Choose matte or glossy finish based on preference

### 3. Apply NFC Tags

1. **Test tags first**: Use NFC Tools app to verify all tags work
2. **Clean surface**: Ensure card surface is clean and dry
3. **Center placement**: Align tag in center or designated area
4. **Firm pressure**: Press tag firmly for 10-15 seconds
5. **Avoid bubbles**: Smooth from center outward

**Important**: Apply tags AFTER printing to avoid heat damage (laser printers can affect NFC tags).

### 4. Optional: Laminate

For extra durability:
- Use cold lamination pouches (heat can damage NFC tags)
- Or use clear protective spray coating
- Test NFC readability after lamination

## Registering Tags

### 1. Scan and Register Each Tag

Using NFC Tools app or Home Assistant:

1. Scan tag with phone/reader
2. Note the **Tag UID** (unique identifier)
3. Record in `tag_mapping.csv` under corresponding tag number
4. Register in Home Assistant: **Settings** → **Tags**

### 2. Create Automation

For each tag in Home Assistant:

1. Go to **Settings** → **Automations**
2. Create new automation
3. **Trigger**: Tag scanned (select your tag)
4. **Action**: Service call to play playlist, toggle mode, etc.

Alternatively, batch-configure using the package templates in `home-assistant/packages/nfc_tags.yaml`.

## Organization Tips

### Tag Numbering System

Use the CSV to organize tags logically:

- **1-20**: Most frequently used playlists
- **21-40**: Room-specific tags
- **41-70**: Extended playlist library
- **71-90**: Seasonal/special occasion
- **91-100**: System controls and special functions

### Physical Organization

- **Card holder/box**: Keep cards in a dedicated box near the NFC reader
- **Sleeve protectors**: Use trading card sleeves for extra protection
- **Dividers**: Separate by category (Energetic, Chill, System, etc.)
- **Display stand**: Create a decorative display for frequently used cards

## Design Inspiration

### Minimalist Style
- White background
- Bold sans-serif text
- Small centered icon
- Color accent bar at top

### Album Art Style
- Spotify playlist cover as background
- Semi-transparent overlay
- White text for readability
- Playlist name and song count

### Icon-Based Style
- Large icon representing mood
- Color gradient background
- Minimal text
- Tag number in corner

## Testing Cards

Before finalizing all 100 cards:

1. **Print 5-10 test cards** with different designs
2. **Apply NFC tags** and test scanning
3. **Check readability** from normal scanning distance
4. **Test durability** (handle frequently, light moisture)
5. **Get feedback** from household/party guests
6. **Iterate design** based on testing

## Maintenance

- **Clean cards** occasionally with slightly damp cloth
- **Replace damaged cards** as needed (keep spare tags)
- **Update CSV** when reassigning tags
- **Backup tag database** from Home Assistant regularly

## Troubleshooting

### Tag won't scan
- Ensure NFC tag is not damaged
- Check tag placement (not too close to card edge)
- Verify tag is NTAG215 compatible
- Test with different NFC reader/phone

### Print quality issues
- Increase printer DPI settings
- Use higher quality card stock
- Check ink/toner levels
- Calibrate printer colors

### Tags stopped working after lamination
- Heat lamination can damage NFC tags
- Use cold lamination method only
- Test cards before and after laminating
- Consider protective spray instead

## Cost Estimate

| Item | Quantity | Estimated Cost |
|------|----------|----------------|
| NTAG215 tags (roll) | 150 tags | $15-25 |
| Card stock (300gsm) | 100 sheets | $20-30 |
| Printing (home) | 100 cards | $5-10 (ink) |
| Lamination pouches | 100 pouches | $15-20 |
| **Total** | | **$55-85** |

**Professional printing**: $100-200 for premium quality

## Resources

- [NTAG215 Specifications](https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf)
- [NFC Tools App](https://www.wakdev.com/en/apps/nfc-tools.html)
- [Free Design Templates](https://www.canva.com/templates/)
- [Business Card Size Guide](https://www.printivity.com/business-card-size/)

## Next Steps

1. ✅ Complete tag mapping CSV
2. ⏳ Design card templates
3. ⏳ Print test batch (10 cards)
4. ⏳ Apply NFC tags and test scanning
5. ⏳ Register tags in Home Assistant
6. ⏳ Create automations for each tag
7. ⏳ Print full set of 100 cards
8. ⏳ Organize and deploy

---

**Happy printing!** Your physical party controller will be a unique conversation piece and functional smart home interface.
