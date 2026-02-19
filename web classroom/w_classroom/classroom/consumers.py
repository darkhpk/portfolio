from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

# Get logger
logger = logging.getLogger('classroom.websocket')

# Store participants per room with additional info
# Structure: {session_id: {'owner': 'username', 'users': {'username': {'ip': 'ip_address', 'channel': 'channel_name'}}}}
room_participants = {}

class CodeConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time code collaboration"""
    
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'code_{self.session_id}'
        self.username = self.scope.get('session', {}).get('username', 'Anonymous')
        
        # Get client IP address
        headers = dict(self.scope.get('headers', []))
        self.ip_address = headers.get(b'x-forwarded-for', b'').decode() or \
                         headers.get(b'x-real-ip', b'').decode() or \
                         self.scope.get('client', [''])[0]
        
        logger.info(f"WebSocket connection initiated - User: {self.username}, Session: {self.session_id}, IP: {self.ip_address}")
        
        # Check if IP is banned
        from channels.db import database_sync_to_async
        from classroom.models import CodeSession
        
        @database_sync_to_async
        def check_banned():
            try:
                session = CodeSession.objects.get(session_id=self.session_id)
                return self.ip_address in session.get_banned_ips()
            except CodeSession.DoesNotExist:
                return False
        
        if await check_banned():
            logger.warning(f"Banned IP {self.ip_address} attempted to connect to session {self.session_id}")
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Initialize room if it doesn't exist
        if self.session_id not in room_participants:
            room_participants[self.session_id] = {'owner': self.username, 'users': {}}
        
        # Add participant to room
        if self.username not in room_participants[self.session_id]['users']:
            room_participants[self.session_id]['users'][self.username] = {
                'ip': self.ip_address,
                'channel': self.channel_name
            }
        
        # Update database participant count
        await self.update_participant_count()
        
        logger.info(f"User {self.username} joined session {self.session_id}. Total participants: {len(room_participants[self.session_id]['users'])}")
        
        # Broadcast updated participant list
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participants_update',
                'participants': list(room_participants[self.session_id]['users'].keys()),
                'owner': room_participants[self.session_id]['owner']
            }
        )
    
    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnecting - User: {self.username}, Session: {self.session_id}, Code: {close_code}")
        
        # Check if user was the owner
        was_owner = False
        if self.session_id in room_participants:
            was_owner = room_participants[self.session_id]['owner'] == self.username
            
            # Remove participant from room
            if self.username in room_participants[self.session_id]['users']:
                del room_participants[self.session_id]['users'][self.username]
            
            if not room_participants[self.session_id]['users']:
                # Room is empty, clean up
                del room_participants[self.session_id]
                logger.info(f"Session {self.session_id} now empty, removed from active rooms")
            else:
                # Transfer ownership if owner left
                if was_owner:
                    # Give ownership to the next person
                    new_owner = next(iter(room_participants[self.session_id]['users'].keys()))
                    room_participants[self.session_id]['owner'] = new_owner
                    logger.info(f"Ownership of session {self.session_id} transferred to {new_owner}")
                
                # Broadcast updated participant list
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'participants_update',
                        'participants': list(room_participants[self.session_id]['users'].keys()),
                        'owner': room_participants[self.session_id]['owner']
                    }
                )
                logger.info(f"User {self.username} left session {self.session_id}. Remaining participants: {len(room_participants[self.session_id]['users'])}")
        
        # Update database participant count
        await self.update_participant_count()
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'unknown')
            logger.debug(f"Received message from {self.username} in session {self.session_id}: type={message_type}")
            
            # Handle management commands
            if message_type == 'kick_user':
                await self.handle_kick_user(data)
            elif message_type == 'mute_user':
                await self.handle_mute_user(data)
            elif message_type == 'unmute_user':
                await self.handle_unmute_user(data)
            elif message_type == 'ban_user':
                await self.handle_ban_user(data)
            elif message_type == 'close_room':
                await self.handle_close_room()
            else:
                # Check if user is muted before allowing code updates
                if message_type == 'code_update':
                    from channels.db import database_sync_to_async
                    from classroom.models import CodeSession
                    
                    @database_sync_to_async
                    def is_muted():
                        try:
                            session = CodeSession.objects.get(session_id=self.session_id)
                            return self.username in session.get_muted_users()
                        except CodeSession.DoesNotExist:
                            return False
                    
                    if await is_muted():
                        logger.warning(f"Muted user {self.username} attempted to update code in session {self.session_id}")
                        return
                
                # Broadcast to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'code_message',
                        'data': data
                    }
                )
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received from {self.username}: {e}")
        except Exception as e:
            logger.error(f"Error processing message from {self.username}: {e}", exc_info=True)
    
    async def code_message(self, event):
        """Receive message from room group"""
        data = event['data']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))
    
    async def participants_update(self, event):
        """Send updated participant list"""
        await self.send(text_data=json.dumps({
            'type': 'participants_update',
            'participants': event['participants'],
            'owner': event['owner']
        }))
    
    async def update_participant_count(self):
        """Update participant count in database"""
        from channels.db import database_sync_to_async
        from classroom.models import CodeSession
        
        @database_sync_to_async
        def update_count():
            try:
                session = CodeSession.objects.get(session_id=self.session_id)
                count = len(room_participants.get(self.session_id, {}).get('users', {}))
                session.participant_count = count
                session.save(update_fields=['participant_count'])
                logger.debug(f"Updated participant count for session {self.session_id}: {count}")
            except CodeSession.DoesNotExist:
                logger.warning(f"Attempted to update participant count for non-existent session: {self.session_id}")
            except Exception as e:
                logger.error(f"Error updating participant count for session {self.session_id}: {e}", exc_info=True)
        
        await update_count()
    
    async def handle_kick_user(self, data):
        """Kick a user from the room (owner only)"""
        if room_participants[self.session_id]['owner'] != self.username:
            logger.warning(f"Non-owner {self.username} attempted to kick user")
            return
        
        target_user = data.get('target_user')
        if target_user and target_user in room_participants[self.session_id]['users']:
            # Get the target user's channel name
            target_channel = room_participants[self.session_id]['users'][target_user]['channel']
            
            # Send kick notification to target user
            await self.channel_layer.send(
                target_channel,
                {
                    'type': 'user_kicked'
                }
            )
            
            logger.info(f"User {target_user} kicked from session {self.session_id} by owner {self.username}")
    
    async def handle_mute_user(self, data):
        """Mute a user's input (owner only)"""
        if room_participants[self.session_id]['owner'] != self.username:
            logger.warning(f"Non-owner {self.username} attempted to mute user")
            return
        
        target_user = data.get('target_user')
        if target_user:
            from channels.db import database_sync_to_async
            from classroom.models import CodeSession
            
            @database_sync_to_async
            def mute_user():
                try:
                    session = CodeSession.objects.get(session_id=self.session_id)
                    session.add_muted_user(target_user)
                    session.save()
                except CodeSession.DoesNotExist:
                    pass
            
            await mute_user()
            
            # Notify all users about the mute
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_muted',
                    'username': target_user
                }
            )
            
            # Broadcast updated participant list to refresh UI
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'participants_update',
                    'participants': list(room_participants[self.session_id]['users'].keys()),
                    'owner': room_participants[self.session_id]['owner']
                }
            )
            
            logger.info(f"User {target_user} muted in session {self.session_id} by owner {self.username}")
    
    async def handle_unmute_user(self, data):
        """Unmute a user's input (owner only)"""
        if room_participants[self.session_id]['owner'] != self.username:
            logger.warning(f"Non-owner {self.username} attempted to unmute user")
            return
        
        target_user = data.get('target_user')
        if target_user:
            from channels.db import database_sync_to_async
            from classroom.models import CodeSession
            
            @database_sync_to_async
            def unmute_user():
                try:
                    session = CodeSession.objects.get(session_id=self.session_id)
                    session.remove_muted_user(target_user)
                    session.save()
                except CodeSession.DoesNotExist:
                    pass
            
            await unmute_user()
            
            # Notify all users about the unmute
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_unmuted',
                    'username': target_user
                }
            )
            
            # Broadcast updated participant list to refresh UI
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'participants_update',
                    'participants': list(room_participants[self.session_id]['users'].keys()),
                    'owner': room_participants[self.session_id]['owner']
                }
            )
            
            logger.info(f"User {target_user} unmuted in session {self.session_id} by owner {self.username}")
    
    async def handle_ban_user(self, data):
        """Ban a user's IP address (owner only)"""
        if room_participants[self.session_id]['owner'] != self.username:
            logger.warning(f"Non-owner {self.username} attempted to ban user")
            return
        
        target_user = data.get('target_user')
        if target_user and target_user in room_participants[self.session_id]['users']:
            target_ip = room_participants[self.session_id]['users'][target_user]['ip']
            target_channel = room_participants[self.session_id]['users'][target_user]['channel']
            
            from channels.db import database_sync_to_async
            from classroom.models import CodeSession
            
            @database_sync_to_async
            def ban_ip():
                try:
                    session = CodeSession.objects.get(session_id=self.session_id)
                    session.add_banned_ip(target_ip)
                    session.save()
                except CodeSession.DoesNotExist:
                    pass
            
            await ban_ip()
            
            # Send kick notification to target user
            await self.channel_layer.send(
                target_channel,
                {
                    'type': 'user_banned'
                }
            )
            
            logger.info(f"User {target_user} (IP: {target_ip}) banned from session {self.session_id} by owner {self.username}")
    
    async def handle_close_room(self):
        """Close the room and redirect all users to lobby (owner only)"""
        if room_participants[self.session_id]['owner'] != self.username:
            logger.warning(f"Non-owner {self.username} attempted to close room")
            return
        
        # Delete room from database
        from channels.db import database_sync_to_async
        from classroom.models import CodeSession
        
        @database_sync_to_async
        def delete_room():
            try:
                session = CodeSession.objects.get(session_id=self.session_id)
                session.delete()
                logger.info(f"Room {self.session_id} deleted from database")
            except CodeSession.DoesNotExist:
                pass
        
        await delete_room()
        
        # Notify all users to redirect to lobby
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_closed'
            }
        )
        
        logger.info(f"Room {self.session_id} closed by owner {self.username}")
    
    async def user_kicked(self, event):
        """Handle being kicked from the room"""
        await self.send(text_data=json.dumps({
            'type': 'kicked'
        }))
        await self.close()
    
    async def user_banned(self, event):
        """Handle being banned from the room"""
        await self.send(text_data=json.dumps({
            'type': 'banned'
        }))
        await self.close()
    
    async def user_muted(self, event):
        """Broadcast that a user was muted"""
        await self.send(text_data=json.dumps({
            'type': 'user_muted',
            'username': event['username']
        }))
    
    async def user_unmuted(self, event):
        """Broadcast that a user was unmuted"""
        await self.send(text_data=json.dumps({
            'type': 'user_unmuted',
            'username': event['username']
        }))
    
    async def room_closed(self, event):
        """Handle room being closed"""
        await self.send(text_data=json.dumps({
            'type': 'room_closed'
        }))
