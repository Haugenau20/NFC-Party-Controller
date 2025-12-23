# Spotcast Automations (Archived)

**Status:** Working configuration as of 2025-12-23
**Git Tag:** `v1.0-spotcast-stable-2025-12-23`

## Purpose

This folder contains the **last known working** Spotcast-based automations, blueprints, and scripts. These files are archived as a safety fallback during the SpotifyPlus migration.

## Files

- `nfc_music_control_playlist_rotation.yaml` - Playlist rotation automation
- `nfc_song_queue_blueprint.yaml` - Song queue blueprint with 3-song limit
- `nfc_playlist_switch_blueprint.yaml` - Playlist switcher blueprint
- `pause_play_all_speakers_automation.yaml` - Admin pause/play all speakers
- `playlist_1_automation.yaml` - New Year Playlist 1
- `playlist_2_automation.yaml` - New Year Playlist 2

## Usage

**Do not modify these files.** They serve as reference and rollback material.

To restore Spotcast functionality:
1. Copy files from this directory back to root
2. Paste into Home Assistant manually
3. Or use git: `git checkout v1.0-spotcast-stable-2025-12-23`

## Migration Notes

These files use:
- `spotcast.play_media` service
- `spotcast.add_to_queue` service
- Account-specific parameters (`account: "01KACG..."`)
- Inline shuffle/repeat configuration

See `../spotifyplus/` for the new SpotifyPlus versions.
