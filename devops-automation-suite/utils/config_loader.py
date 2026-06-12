"""
Configuration Loader
Loads and validates configuration files
"""

import yaml
from pathlib import Path


def load_config(config_path='config.yaml'):
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def validate_config(config):
    """
    Validate configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        bool: True if valid
    """
    required_keys = ['servers']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    return True
