# Release Notes

## v0.2.1 (Pending)
##### Fixes
- Fixed parsing Pokemon log messages with multiple details (`ME-647`).
- Fixed parsing null log messages (`ME-648`).

##### Features
- Added RetryPolicy and RetryPolicyBuilder (`ME-659`).
- Added stopping after attempt (`ME-659`).
- Added stopping after duration (`ME-659`).
- Added stopping after never (`ME-659`).
- Added stopping on multiple conditions (`ME-659`).
- Added waiting for fixed duration (`ME-659`).
- Added continuing on exceptions (`ME-659`).
- Added continuing on results (`ME-659`).
- Added pre-hooks (`ME-659`).
- Added post-hooks (`ME-659`).

## v0.2.0 (Pending)
##### Changes
- Renamed morpha package to "clare".

## v0.1.0 (2017-04-20)
##### Features
- Added logging.
- Added BattleMetricsService with damage dealt metric (`ME-630`).
- Added Battle, Player, and Pokemon (`ME-630`).
- Added BattleLog (`ME-630`).
- Added IRecord and concrete Record (`ME-630`).
