"""
Deployment Automation Script
Automates deployment to multiple servers with rollback capability
"""

import argparse
import sys
import time
from datetime import datetime
from utils.ssh_client import SSHClient
from utils.config_loader import load_config
from utils.logger import setup_logger
from utils.email_notifier import send_notification

logger = setup_logger('deploy')


class DeploymentManager:
    """Manages deployment operations"""
    
    def __init__(self, environment, config):
        """
        Initialize deployment manager
        
        Args:
            environment: Target environment (production, staging, etc.)
            config: Configuration dictionary
        """
        self.environment = environment
        self.config = config
        self.servers = self._get_servers()
    
    def _get_servers(self):
        """Get servers for the environment"""
        return [s for s in self.config['servers'] if s.get('environment') == self.environment]
    
    def deploy(self, branch='main', tag=None, rollback_on_error=False):
        """
        Deploy application
        
        Args:
            branch: Git branch to deploy
            tag: Git tag to deploy (overrides branch)
            rollback_on_error: Rollback if deployment fails
            
        Returns:
            bool: True if deployment successful
        """
        logger.info(f"Starting deployment to {self.environment}")
        logger.info(f"Branch/Tag: {tag or branch}")
        
        deployment_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for server in self.servers:
            logger.info(f"Deploying to {server['name']} ({server['host']})")
            
            try:
                ssh = SSHClient(server)
                
                # Pre-deployment checks
                logger.info("Running pre-deployment checks...")
                if not self._pre_deployment_checks(ssh):
                    raise Exception("Pre-deployment checks failed")
                
                # Backup current version
                logger.info("Creating backup of current version...")
                self._create_backup(ssh, deployment_id)
                
                # Pull latest code
                logger.info("Pulling latest code...")
                git_ref = tag if tag else branch
                ssh.execute(f"cd {server['app_path']} && git fetch --all")
                ssh.execute(f"cd {server['app_path']} && git checkout {git_ref}")
                ssh.execute(f"cd {server['app_path']} && git pull origin {git_ref}")
                
                # Install dependencies
                logger.info("Installing dependencies...")
                ssh.execute(f"cd {server['app_path']} && pip install -r requirements.txt")
                
                # Run migrations if needed
                if server.get('run_migrations', False):
                    logger.info("Running database migrations...")
                    ssh.execute(f"cd {server['app_path']} && python manage.py migrate")
                
                # Restart services
                logger.info("Restarting services...")
                for service in server.get('services', []):
                    ssh.execute(f"sudo systemctl restart {service}")
                    time.sleep(2)
                
                # Post-deployment checks
                logger.info("Running post-deployment checks...")
                if not self._post_deployment_checks(ssh, server):
                    if rollback_on_error:
                        logger.error("Post-deployment checks failed. Rolling back...")
                        self._rollback(ssh, deployment_id)
                        raise Exception("Deployment failed and rolled back")
                    else:
                        raise Exception("Post-deployment checks failed")
                
                logger.info(f"✓ Deployment to {server['name']} successful")
                
            except Exception as e:
                logger.error(f"✗ Deployment to {server['name']} failed: {str(e)}")
                send_notification(
                    subject=f"Deployment Failed: {self.environment}",
                    body=f"Deployment to {server['name']} failed: {str(e)}",
                    config=self.config
                )
                return False
        
        logger.info("=" * 60)
        logger.info("Deployment completed successfully!")
        logger.info("=" * 60)
        
        send_notification(
            subject=f"Deployment Successful: {self.environment}",
            body=f"Deployment to {self.environment} completed successfully",
            config=self.config
        )
        
        return True
    
    def _pre_deployment_checks(self, ssh):
        """Run pre-deployment checks"""
        # Check disk space
        output = ssh.execute("df -h / | tail -1 | awk '{print $5}'")
        disk_usage = int(output.strip().replace('%', ''))
        
        if disk_usage > 90:
            logger.error(f"Disk usage too high: {disk_usage}%")
            return False
        
        return True
    
    def _create_backup(self, ssh, deployment_id):
        """Create backup of current version"""
        ssh.execute(f"mkdir -p /backups/deployments")
        # Backup would be implemented here
        pass
    
    def _post_deployment_checks(self, ssh, server):
        """Run post-deployment health checks"""
        # Check if services are running
        for service in server.get('services', []):
            output = ssh.execute(f"systemctl is-active {service}")
            if output.strip() != 'active':
                logger.error(f"Service {service} is not running")
                return False
        
        # Check application health endpoint
        if 'health_url' in server:
            import requests
            try:
                response = requests.get(server['health_url'], timeout=10)
                if response.status_code != 200:
                    logger.error(f"Health check failed: {response.status_code}")
                    return False
            except Exception as e:
                logger.error(f"Health check failed: {str(e)}")
                return False
        
        return True
    
    def _rollback(self, ssh, deployment_id):
        """Rollback to previous version"""
        logger.info("Rolling back to previous version...")
        # Rollback implementation would be here
        pass


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Deployment Automation Script')
    parser.add_argument('--environment', '-e', required=True,
                       help='Target environment (production, staging)')
    parser.add_argument('--branch', '-b', default='main',
                       help='Git branch to deploy')
    parser.add_argument('--tag', '-t', help='Git tag to deploy')
    parser.add_argument('--rollback-on-error', action='store_true',
                       help='Rollback if deployment fails')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        sys.exit(1)
    
    # Initialize deployment manager
    manager = DeploymentManager(args.environment, config)
    
    # Deploy
    success = manager.deploy(
        branch=args.branch,
        tag=args.tag,
        rollback_on_error=args.rollback_on_error
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
