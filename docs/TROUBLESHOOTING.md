# Troubleshooting Guide

Common issues and solutions for the NFC Party Controller.

## Hardware Issues

### ESP32 Not Connecting to WiFi

**Symptoms**: Device not appearing in Home Assistant

**Solutions**:
- Check WiFi credentials in secrets.yaml
- Verify 2.4GHz network (ESP32 does not support 5GHz)
- Check router allows new device connections
- Look for fallback AP and configure via captive portal
- Check ESPHome logs: esphome logs esphome/nfc_controller.yaml

### NFC Tags Not Detected

**Symptoms**: No tag scan events in logs

**Solutions**:
- Verify PN532 wiring (SDA=GPIO21, SCL=GPIO22)
- Check PN532 is in I2C mode (DIP switches)
- Test with known-good NTAG215 tags
- Check I2C initialization in ESPHome logs
- Try different tag (may be damaged)
- Ensure tag is within 3-5cm of reader

### Buttons Not Responding

**Symptoms**: No events when button pressed

**Solutions**:
- Check button wiring to correct GPIO
- Verify GND connection
- Test button continuity with multimeter
- Check ESPHome logs for button state changes
- Ensure pullup configured in YAML

### Potentiometer Readings Erratic

**Symptoms**: Volume jumps randomly

**Solutions**:
- Check pot wiring (VCC, GND, wiper to GPIO34)
- Clean potentiometer contacts
- Adjust filter settings in ESPHome
- Increase delta filter threshold
- Replace potentiometer if worn

### Buzzer Not Working

**Symptoms**: No sound on tag scan

**Solutions**:
- Check MOSFET wiring (gate to GPIO23)
- Verify 5V power to buzzer
- Test MOSFET with multimeter
- Check flyback diode orientation
- Try different buzzer (may be faulty)

## Software Issues

### ESPHome Compilation Errors

**Symptoms**: Errors during esphome run

**Solutions**:
- Update ESPHome: pip install -U esphome
- Check YAML syntax (indentation must be exact)
- Validate secrets.yaml exists and has correct format
- Review error messages for specific issues

### OTA Upload Fails

**Symptoms**: Cannot upload over WiFi

**Solutions**:
- Verify device is on same network
- Check OTA password matches secrets.yaml
- Try USB upload instead
- Restart ESP32
- Check firewall not blocking mDNS/OTA ports

### Home Assistant Not Discovering ESP32

**Symptoms**: Device missing from integrations

**Solutions**:
- Check ESP32 is online (ping IP address)
- Restart Home Assistant
- Manually add ESPHome integration with IP
- Verify API encryption key matches
- Check HA logs for connection errors

## Automation Issues

### Tags Not Triggering Automations

**Symptoms**: Tag scans but nothing happens

**Solutions**:
- Verify tag registered in HA: Settings → Tags
- Check automation is enabled
- Review automation conditions (party mode, time, etc.)
- Test automation manually in Developer Tools
- Check tag ID matches in automation trigger
- View Events in Developer Tools (listen for tag_scanned)

### Spotify Playlists Not Playing

**Symptoms**: No music on tag scan

**Solutions**:
- Verify Spotify integration working
- Check playlist URI format (spotify:playlist:ID)
- Ensure speaker entity ID correct
- Test manual playlist playback first
- Check Spotify account has Premium (required for API)
- Verify speaker supports Spotify

### Volume Control Not Working

**Symptoms**: Pot rotation does not change volume

**Solutions**:
- Check sensor updating: sensor.nfc_party_controller_volume_pot
- Verify rate limiting condition in automation
- Ensure media player entity IDs correct
- Check party mode is active (if required by automation)
- Test manual volume service call

### Multi-Room Audio Grouping Fails

**Symptoms**: Speakers not synchronizing

**Solutions**:
- Check all speakers online and responsive
- Verify entity IDs in grouping script
- Use native Beolink for B&O (not Chromecast)
- Check speaker firmware up to date
- Test grouping manually via HA UI

## Network Issues

### Intermittent Disconnections

**Solutions**:
- Check WiFi signal strength
- Move router closer or add WiFi extender
- Set static IP for ESP32
- Reduce WiFi channel interference
- Update ESP32 WiFi parameters in ESPHome

### Slow Response Times

**Solutions**:
- Check network latency
- Reduce automation complexity
- Optimize Home Assistant performance
- Use wired Ethernet for HA server
- Check HA system resources

## Card/Tag Issues

### Tags Losing Programming

**Symptoms**: Previously working tags stop working

**Solutions**:
- Re-scan tag and check UID unchanged
- Re-register tag in Home Assistant
- Avoid exposure to strong magnets
- Replace damaged tags
- Keep tags away from heat sources

### Laminated Cards Not Scanning

**Symptoms**: Cards work before lamination, not after

**Solutions**:
- Use cold lamination only (heat damages tags)
- Ensure tag not too deep in card stack
- Try thinner lamination
- Test before laminating full batch

## Performance Issues

### Home Assistant Slow

**Solutions**:
- Check system resources (CPU, RAM, disk)
- Reduce recorder history retention
- Disable unused integrations
- Optimize automations (reduce frequency)
- Consider HA Yellow or dedicated hardware

### ESP32 Rebooting

**Solutions**:
- Check power supply (stable 5V, 1A minimum)
- Reduce WiFi transmit power in ESPHome
- Check for short circuits
- Update ESP32 firmware
- Check for overheating

## Debugging Tools

### ESPHome Logs
esphome logs esphome/nfc_controller.yaml

### Home Assistant Logs
Settings → System → Logs

### Developer Tools
- States: View all entity states
- Events: Listen for specific events (tag_scanned)
- Services: Test service calls manually

### Network Tools
- ping: Check device connectivity
- nmap: Scan for devices on network
- mDNS browser: Find ESPHome devices

## Getting Help

If issues persist:
1. Check ESPHome logs for errors
2. Review Home Assistant logs
3. Search GitHub issues
4. Post on Home Assistant forum
5. ESPHome Discord channel

## Common Error Messages

**"API client connection error"**
- ESP32 cannot reach Home Assistant
- Check network connectivity and API key

**"Tag not found"**
- Tag not registered in Home Assistant
- Register in Settings → Tags

**"Media player unavailable"**
- Speaker offline or entity ID wrong
- Check speaker power and network

**"Spotify authentication failed"**
- Re-authorize Spotify integration
- Check client ID and secret

---

**Tip**: Most issues are resolved by checking logs and verifying configuration matches documentation.
