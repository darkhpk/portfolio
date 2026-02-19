# Room Management Features

This document describes the room management features available to the room creator/owner.

## Overview

When a user creates a room, they become the **owner** (indicated by a 👑 crown icon next to their name). The owner has special privileges to manage participants in the room.

## Owner Transfer

If the owner leaves or disconnects from the room, **ownership is automatically transferred** to the next participant in the room. This ensures that the room always has an owner who can manage participants.

## Owner Privileges

### 1. **Kick User** (👢)
- Immediately removes a user from the room
- The kicked user is disconnected and shown a message
- The user can rejoin the room later

### 2. **Mute User** (🔇)
- Prevents a user from editing the shared code
- The muted user can still see code changes from others
- The muted user's textarea is disabled with a message: "You have been muted by the room owner"
- A muted user is shown with a "(muted)" indicator next to their name
- Can be undone with the unmute button (🔊)

### 3. **Ban User** (🚫)
- Permanently bans a user's IP address from the room
- The banned user is kicked immediately
- The user cannot reconnect to the room (connection is blocked at WebSocket level)
- Bans are stored in the database and persist across server restarts

### 4. **Close Room** (🚪)
- Closes the entire room
- All participants are redirected to the lobby
- The close button appears next to the participants button, only visible to the owner
- Confirmation dialog prevents accidental closure

## User Interface

### Participants List
The participants dropdown shows:
- All online users
- Owner indicator (👑)
- Muted status for muted users
- Management buttons (only visible to owner, and only for other users)

### Management Buttons
Each participant (except yourself if you're the owner) has three action buttons:
- **Mute/Unmute** (🔇/🔊): Toggle user's ability to edit code
- **Kick** (👢): Remove user from room
- **Ban** (🚫): Permanently ban user's IP

### Close Room Button
- Located in the header, next to the participants button
- Only visible to the room owner
- Red button labeled "🚪 Close Room"
- Requires confirmation before closing

## Technical Implementation

### Database Fields
- `banned_ips`: JSON array of banned IP addresses
- `muted_users`: JSON array of muted usernames
- Helper methods: `get_banned_ips()`, `add_banned_ip()`, `get_muted_users()`, `add_muted_user()`, `remove_muted_user()`

### WebSocket Messages
- `kick_user`: Kick a specific user
- `mute_user`: Mute a user's input
- `unmute_user`: Unmute a user's input
- `ban_user`: Ban a user's IP address
- `close_room`: Close the entire room

### IP Address Detection
The system detects user IP addresses from:
1. `X-Forwarded-For` header (for proxy/load balancer setups)
2. `X-Real-IP` header (for nginx reverse proxy)
3. Direct client IP from WebSocket scope

### Ban Check
When a user attempts to connect:
1. Their IP is extracted from headers
2. The room's banned IPs are checked
3. If banned, the connection is immediately rejected

### Mute Check
When a user sends a code update:
1. Their username is checked against the muted users list
2. If muted, the update is silently dropped
3. The muted user's textarea is disabled client-side

## Logging

All management actions are logged to `logs/websocket.log`:
- User kicks
- User mutes/unmutes
- IP bans
- Room closures
- Ownership transfers
- Banned connection attempts
- Unauthorized management attempts

## Security Considerations

1. **Authorization**: All management actions verify that the requester is the current owner
2. **IP Banning**: Uses IP detection from multiple header sources for reliability
3. **Validation**: All management commands validate target user existence
4. **Logging**: Complete audit trail of all management actions
5. **Client-side Protection**: Disabled textarea prevents accidental edits by muted users

## User Experience

### For Owners
- Management buttons appear in the participants list
- Close room button visible in header
- Clear visual feedback for all actions
- Confirmation dialogs prevent accidents

### For Regular Users
- No management buttons visible
- Clear notifications when kicked, banned, or muted
- Automatic redirect to lobby when kicked/banned/room closed
- Disabled input with explanation when muted

### For Transferred Owners
- Seamlessly gain management privileges when previous owner leaves
- Close room button appears automatically
- Management buttons appear in participants list
- Logged as the new owner in system logs
