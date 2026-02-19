from django.db import models
import uuid
import json


class CodeSession(models.Model):
    """Model to store collaborative coding sessions"""
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    room_name = models.CharField(max_length=200, blank=True, default='')
    creator_username = models.CharField(max_length=200, blank=True, default='')
    code = models.TextField(blank=True, default='')
    output = models.TextField(blank=True, default='')
    language = models.CharField(max_length=50, default='python')
    participant_count = models.IntegerField(default=0)
    banned_ips = models.TextField(blank=True, default='[]')  # JSON array of banned IPs
    muted_users = models.TextField(blank=True, default='[]')  # JSON array of muted usernames
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.room_name or 'Session'} ({self.session_id[:8]}...)"
    
    def get_banned_ips(self):
        """Get list of banned IPs"""
        try:
            return json.loads(self.banned_ips)
        except:
            return []
    
    def add_banned_ip(self, ip):
        """Ban an IP address"""
        banned = self.get_banned_ips()
        if ip not in banned:
            banned.append(ip)
            self.banned_ips = json.dumps(banned)
            self.save()
    
    def get_muted_users(self):
        """Get list of muted users"""
        try:
            return json.loads(self.muted_users)
        except:
            return []
    
    def add_muted_user(self, username):
        """Mute a user"""
        muted = self.get_muted_users()
        if username not in muted:
            muted.append(username)
            self.muted_users = json.dumps(muted)
            self.save()
    
    def remove_muted_user(self, username):
        """Unmute a user"""
        muted = self.get_muted_users()
        if username in muted:
            muted.remove(username)
            self.muted_users = json.dumps(muted)
            self.save()
