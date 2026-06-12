"""
SSH Client Utility
Handles SSH connections and command execution
"""

import paramiko
from utils.logger import setup_logger

logger = setup_logger('ssh')


class SSHClient:
    """SSH client for remote command execution"""
    
    def __init__(self, server_config):
        """
        Initialize SSH client
        
        Args:
            server_config: Server configuration dictionary
        """
        self.config = server_config
        self.client = None
    
    def connect(self):
        """Establish SSH connection"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect using key or password
            if 'key_path' in self.config:
                key = paramiko.RSAKey.from_private_key_file(self.config['key_path'])
                self.client.connect(
                    hostname=self.config['host'],
                    port=self.config.get('port', 22),
                    username=self.config['user'],
                    pkey=key
                )
            else:
                self.client.connect(
                    hostname=self.config['host'],
                    port=self.config.get('port', 22),
                    username=self.config['user'],
                    password=self.config.get('password')
                )
            
            logger.debug(f"Connected to {self.config['host']}")
            
        except Exception as e:
            logger.error(f"SSH connection failed: {str(e)}")
            raise
    
    def execute(self, command, timeout=30):
        """
        Execute command on remote server
        
        Args:
            command: Command to execute
            timeout: Execution timeout
            
        Returns:
            str: Command output
        """
        if not self.client:
            self.connect()
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if error:
                logger.warning(f"Command error: {error}")
            
            return output
            
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            raise
    
    def close(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            logger.debug("SSH connection closed")
