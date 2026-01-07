# SpotifyPlus Automations (Active Development)

**Status:** In development
**Branch:** `feature/spotifyplus-migration`

## Purpose

This folder contains the **new SpotifyPlus-based** versions of automations, blueprints, and scripts.

## Migration Checklist

Files to migrate from `../spotcast/`:

- [ ] `nfc_music_control_playlist_rotation.yaml`
- [ ] `nfc_song_queue_blueprint.yaml`
- [ ] `nfc_playlist_switch_blueprint.yaml`
- [ ] `pause_play_all_speakers_automation.yaml`
- [ ] `playlist_1_automation.yaml`
- [ ] `playlist_2_automation.yaml`

## Key Changes

SpotifyPlus uses:
- Different service names (e.g., `spotifyplus.play_media`)
- Entity-based account selection (each account = separate `media_player` entity)
- Potentially different parameter names for shuffle/repeat
- More comprehensive API coverage (95+ services)

## Testing Process

1. Migrate one file at a time
2. Copy-paste into Home Assistant
3. Test with both Device 1 and Device 2
4. Verify both Spotify accounts work correctly
5. Commit working version with clear message

## Reference

- SpotifyPlus Documentation: https://github.com/thlucas1/homeassistantcomponent_spotifyplus/wiki
- Original Spotcast versions: `../spotcast/`
