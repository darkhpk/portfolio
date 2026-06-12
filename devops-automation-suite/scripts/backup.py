"""
Backup Management Script
Automated backup and restoration
"""

import argparse
import os
import shutil
import tarfile
from datetime import datetime, timedelta
from pathlib import Path
from utils.logger import setup_logger
from utils.config_loader import load_config

logger = setup_logger('backup')


class BackupManager:
    """Manages backup operations"""
    
    def __init__(self, config):
        """
        Initialize backup manager
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.backup_dest = config.get('backup', {}).get('destination', '/backups')
        self.retention_days = config.get('backup', {}).get('retention_days', 30)
    
    def create_backup(self, backup_type='full', compress=True):
        """
        Create backup
        
        Args:
            backup_type: Type of backup (full, incremental)
            compress: Whether to compress backup
            
        Returns:
            str: Path to backup file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{backup_type}_{timestamp}"
        
        logger.info("=" * 60)
        logger.info(f"Creating {backup_type} backup")
        logger.info("=" * 60)
        
        # Create backup directory
        os.makedirs(self.backup_dest, exist_ok=True)
        
        backup_path = os.path.join(self.backup_dest, backup_name)
        
        if compress:
            backup_path += '.tar.gz'
            self._create_compressed_backup(backup_path)
        else:
            os.makedirs(backup_path, exist_ok=True)
            self._create_directory_backup(backup_path)
        
        logger.info(f"✓ Backup created: {backup_path}")
        
        # Cleanup old backups
        self._cleanup_old_backups()
        
        return backup_path
    
    def _create_compressed_backup(self, backup_path):
        """Create compressed tar.gz backup"""
        source_paths = self.config.get('backup', {}).get('sources', [])
        
        with tarfile.open(backup_path, "w:gz") as tar:
            for source in source_paths:
                if os.path.exists(source):
                    logger.info(f"  Adding {source}...")
                    tar.add(source, arcname=os.path.basename(source))
                else:
                    logger.warning(f"  Source not found: {source}")
    
    def _create_directory_backup(self, backup_path):
        """Create directory backup"""
        source_paths = self.config.get('backup', {}).get('sources', [])
        
        for source in source_paths:
            if os.path.exists(source):
                logger.info(f"  Copying {source}...")
                dest = os.path.join(backup_path, os.path.basename(source))
                if os.path.isdir(source):
                    shutil.copytree(source, dest)
                else:
                    shutil.copy2(source, dest)
            else:
                logger.warning(f"  Source not found: {source}")
    
    def _cleanup_old_backups(self):
        """Remove backups older than retention period"""
        logger.info("\nCleaning up old backups...")
        
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        removed_count = 0
        
        for item in Path(self.backup_dest).iterdir():
            if item.is_file() or item.is_dir():
                # Get file modification time
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                
                if mtime < cutoff_date:
                    logger.info(f"  Removing old backup: {item.name}")
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)
                    removed_count += 1
        
        if removed_count > 0:
            logger.info(f"✓ Removed {removed_count} old backup(s)")
        else:
            logger.info("  No old backups to remove")
    
    def list_backups(self):
        """List all available backups"""
        logger.info("=" * 60)
        logger.info("Available Backups")
        logger.info("=" * 60)
        
        if not os.path.exists(self.backup_dest):
            logger.info("No backups found")
            return []
        
        backups = []
        for item in sorted(Path(self.backup_dest).iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            size = self._get_size(item)
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            
            backups.append({
                'name': item.name,
                'path': str(item),
                'size': size,
                'date': mtime
            })
            
            logger.info(f"{item.name}")
            logger.info(f"  Size: {self._format_size(size)}")
            logger.info(f"  Date: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("")
        
        return backups
    
    def _get_size(self, path):
        """Get size of file or directory"""
        if path.is_file():
            return path.stat().st_size
        
        total = 0
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
        return total
    
    def _format_size(self, bytes_value):
        """Format bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Backup Management Script')
    parser.add_argument('--action', choices=['create', 'list'], default='create',
                       help='Action to perform')
    parser.add_argument('--type', choices=['full', 'incremental'], default='full',
                       help='Backup type')
    parser.add_argument('--compress', action='store_true', default=True,
                       help='Compress backup')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        config = {}
    
    # Initialize backup manager
    manager = BackupManager(config)
    
    # Perform action
    if args.action == 'create':
        manager.create_backup(backup_type=args.type, compress=args.compress)
    elif args.action == 'list':
        manager.list_backups()


if __name__ == '__main__':
    main()
