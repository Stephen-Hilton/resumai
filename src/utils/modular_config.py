#!/usr/bin/env python3
"""
Configuration system for modular vs legacy generation

Provides centralized configuration management for the modular resume generation system.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class ModularConfig:
    """
    Configuration manager for modular resume generation system.
    
    Handles configuration loading from environment variables, config files,
    and provides runtime configuration switching between modular and legacy modes.
    """
    
    DEFAULT_CONFIG = {
        # Generation method selection
        'use_modular_generation': True,
        'enable_parallel_processing': True,
        'fallback_to_legacy_on_failure': True,
        
        # Timing and performance
        'section_timeout_seconds': 30,
        'max_parallel_sections': 6,
        'ui_update_interval_seconds': 5.0,
        'max_retry_attempts': 2,
        
        # LLM configuration
        'llm_provider': None,  # Will be loaded from env
        'llm_model': None,     # Will be loaded from env
        'llm_api_key': None,   # Will be loaded from env
        
        # Template and resource paths (make them absolute)
        'template_dir': str(Path(__file__).parent.parent / 'resources' / 'templates'),
        'css_dir': str(Path(__file__).parent.parent / 'resources' / 'css'),
        'icons_dir': str(Path(__file__).parent.parent / 'resources' / 'icons'),
        'fonts_dir': str(Path(__file__).parent.parent / 'resources' / 'fonts'),
        
        # Output configuration
        'output_format': 'both',  # 'html', 'pdf', 'both'
        'enable_pdf_generation': True,
        'pdf_engine': 'weasyprint',
        
        # Progress tracking
        'enable_progress_tracking': True,
        'enable_websocket_updates': True,
        'progress_update_frequency': 2.0,  # seconds
        
        # Error handling
        'enable_error_recovery': True,
        'log_section_failures': True,
        'preserve_partial_results': True,
        
        # Development and testing
        'debug_mode': False,
        'enable_performance_monitoring': True,
        'save_intermediate_results': False
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Optional path to JSON configuration file
        """
        self.config_file = config_file
        self.config = self.DEFAULT_CONFIG.copy()
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from environment variables and config file."""
        # Load environment variables
        load_dotenv()
        
        # Load from environment variables
        self._load_from_environment()
        
        # Load from config file if provided
        if self.config_file and Path(self.config_file).exists():
            self._load_from_file()
        
        # Validate configuration
        self._validate_configuration()
        
        logger.info(f"Configuration loaded: modular={self.config['use_modular_generation']}, "
                   f"parallel={self.config['enable_parallel_processing']}")
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'USE_MODULAR_GENERATION': ('use_modular_generation', bool),
            'ENABLE_PARALLEL_PROCESSING': ('enable_parallel_processing', bool),
            'SECTION_TIMEOUT_SECONDS': ('section_timeout_seconds', int),
            'MAX_PARALLEL_SECTIONS': ('max_parallel_sections', int),
            'UI_UPDATE_INTERVAL': ('ui_update_interval_seconds', float),
            'MAX_RETRY_ATTEMPTS': ('max_retry_attempts', int),
            
            'LLM_MODEL_PROVIDER': ('llm_provider', str),
            'LLM_MODEL': ('llm_model', str),
            'LLM_API_KEY': ('llm_api_key', str),
            
            'ENABLE_PDF_GENERATION': ('enable_pdf_generation', bool),
            'PDF_ENGINE': ('pdf_engine', str),
            
            'DEBUG_MODE': ('debug_mode', bool),
            'ENABLE_PERFORMANCE_MONITORING': ('enable_performance_monitoring', bool)
        }
        
        for env_var, (config_key, value_type) in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                try:
                    if value_type == bool:
                        self.config[config_key] = env_value.lower() in ('true', '1', 'yes', 'on')
                    elif value_type == int:
                        self.config[config_key] = int(env_value)
                    elif value_type == float:
                        self.config[config_key] = float(env_value)
                    else:
                        self.config[config_key] = env_value
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid value for {env_var}: {env_value}, using default")
    
    def _load_from_file(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
                logger.info(f"Configuration loaded from {self.config_file}")
        except Exception as e:
            logger.error(f"Error loading config file {self.config_file}: {str(e)}")
    
    def _validate_configuration(self):
        """Validate configuration values and set reasonable defaults."""
        # Ensure timeout values are reasonable
        if self.config['section_timeout_seconds'] < 10:
            logger.warning("Section timeout too low, setting to 10 seconds")
            self.config['section_timeout_seconds'] = 10
        
        if self.config['section_timeout_seconds'] > 300:
            logger.warning("Section timeout too high, setting to 300 seconds")
            self.config['section_timeout_seconds'] = 300
        
        # Ensure parallel section count is reasonable
        if self.config['max_parallel_sections'] < 1:
            self.config['max_parallel_sections'] = 1
        elif self.config['max_parallel_sections'] > 10:
            self.config['max_parallel_sections'] = 10
        
        # Ensure update intervals are reasonable
        if self.config['ui_update_interval_seconds'] < 1.0:
            self.config['ui_update_interval_seconds'] = 1.0
        elif self.config['ui_update_interval_seconds'] > 10.0:
            self.config['ui_update_interval_seconds'] = 10.0
        
        # Validate paths exist
        for path_key in ['template_dir', 'css_dir', 'icons_dir', 'fonts_dir']:
            path_value = self.config[path_key]
            if not Path(path_value).exists():
                logger.warning(f"Path does not exist: {path_value}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value at runtime."""
        self.config[key] = value
        logger.info(f"Configuration updated: {key} = {value}")
    
    def enable_modular_generation(self, enable: bool = True) -> None:
        """Enable or disable modular generation."""
        self.config['use_modular_generation'] = enable
        logger.info(f"Modular generation {'enabled' if enable else 'disabled'}")
    
    def enable_parallel_processing(self, enable: bool = True) -> None:
        """Enable or disable parallel processing."""
        self.config['enable_parallel_processing'] = enable
        logger.info(f"Parallel processing {'enabled' if enable else 'disabled'}")
    
    def get_llm_config(self) -> Dict[str, str]:
        """Get LLM configuration for section generators."""
        return {
            'provider': self.config['llm_provider'],
            'model': self.config['llm_model'],
            'api_key': self.config['llm_api_key']
        }
    
    def get_resource_paths(self) -> Dict[str, str]:
        """Get resource directory paths."""
        return {
            'templates': self.config['template_dir'],
            'css': self.config['css_dir'],
            'icons': self.config['icons_dir'],
            'fonts': self.config['fonts_dir']
        }
    
    def is_modular_enabled(self) -> bool:
        """Check if modular generation is enabled."""
        return self.config['use_modular_generation']
    
    def is_parallel_enabled(self) -> bool:
        """Check if parallel processing is enabled."""
        return self.config['enable_parallel_processing']
    
    def save_to_file(self, file_path: str) -> None:
        """Save current configuration to file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving config to {file_path}: {str(e)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return self.config.copy()
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"ModularConfig(modular={self.config['use_modular_generation']}, " \
               f"parallel={self.config['enable_parallel_processing']}, " \
               f"timeout={self.config['section_timeout_seconds']}s)"


# Global configuration instance
_config_instance = None

def get_config(config_file: Optional[str] = None) -> ModularConfig:
    """
    Get global configuration instance.
    
    Args:
        config_file: Optional path to configuration file
        
    Returns:
        ModularConfig instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = ModularConfig(config_file)
    
    return _config_instance

def reload_config(config_file: Optional[str] = None) -> ModularConfig:
    """
    Reload configuration (useful for testing or runtime config changes).
    
    Args:
        config_file: Optional path to configuration file
        
    Returns:
        New ModularConfig instance
    """
    global _config_instance
    _config_instance = ModularConfig(config_file)
    return _config_instance