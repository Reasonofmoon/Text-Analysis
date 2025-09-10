"""Plugin manager for loading and managing plugins."""

import importlib
import importlib.util
import inspect
import logging
from pathlib import Path
from typing import Dict, List, Optional, Type, Any, Union
import json

from .base import BasePlugin, AnalyzerPlugin, ProcessorPlugin, ExporterPlugin, ValidationPlugin, PluginMetadata


class PluginManager:
    """Manager for loading, registering, and managing plugins."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.plugins: Dict[str, BasePlugin] = {}
        self.analyzer_plugins: Dict[str, AnalyzerPlugin] = {}
        self.processor_plugins: Dict[str, ProcessorPlugin] = {}
        self.exporter_plugins: Dict[str, ExporterPlugin] = {}
        self.validation_plugins: Dict[str, ValidationPlugin] = {}
        self.plugin_directories: List[str] = []
    
    def add_plugin_directory(self, directory: str) -> None:
        """Add a directory to search for plugins.
        
        Args:
            directory: Path to plugin directory
        """
        if directory not in self.plugin_directories:
            self.plugin_directories.append(directory)
            self.logger.info(f"Added plugin directory: {directory}")
    
    def load_plugin_from_file(self, file_path: str) -> Optional[BasePlugin]:
        """Load a plugin from a Python file.
        
        Args:
            file_path: Path to the plugin file
            
        Returns:
            Loaded plugin instance or None if failed
        """
        try:
            # Load module from file
            spec = importlib.util.spec_from_file_location("plugin_module", file_path)
            if spec is None or spec.loader is None:
                self.logger.error(f"Could not load spec from {file_path}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes in the module
            plugin_classes = []
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BasePlugin) and 
                    obj != BasePlugin and 
                    not obj.__name__.startswith('Base')):
                    plugin_classes.append(obj)
            
            if not plugin_classes:
                self.logger.warning(f"No plugin classes found in {file_path}")
                return None
            
            # Instantiate the first plugin class found
            plugin_class = plugin_classes[0]
            
            # Look for metadata in the module
            metadata = getattr(module, 'PLUGIN_METADATA', None)
            if metadata is None:
                # Create default metadata
                metadata = PluginMetadata(
                    name=plugin_class.__name__,
                    version="1.0.0",
                    description=plugin_class.__doc__ or "No description",
                    author="Unknown"
                )
            elif isinstance(metadata, dict):
                metadata = PluginMetadata(**metadata)
            
            # Create plugin instance
            plugin = plugin_class(metadata)
            
            # Validate requirements
            missing_requirements = plugin.validate_requirements()
            if missing_requirements:
                self.logger.error(
                    f"Plugin {metadata.name} missing requirements: {missing_requirements}"
                )
                return None
            
            self.logger.info(f"Loaded plugin: {metadata.name} v{metadata.version}")
            return plugin
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin from {file_path}: {e}")
            return None
    
    def load_plugin_from_module(self, module_name: str) -> Optional[BasePlugin]:
        """Load a plugin from an installed module.
        
        Args:
            module_name: Name of the module to load
            
        Returns:
            Loaded plugin instance or None if failed
        """
        try:
            module = importlib.import_module(module_name)
            
            # Look for plugin factory function
            if hasattr(module, 'create_plugin'):
                plugin = module.create_plugin()
                if isinstance(plugin, BasePlugin):
                    self.logger.info(f"Loaded plugin from module: {module_name}")
                    return plugin
            
            # Look for plugin classes
            plugin_classes = []
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BasePlugin) and 
                    obj != BasePlugin and 
                    not obj.__name__.startswith('Base')):
                    plugin_classes.append(obj)
            
            if plugin_classes:
                plugin_class = plugin_classes[0]
                metadata = getattr(module, 'PLUGIN_METADATA', None)
                if metadata is None:
                    metadata = PluginMetadata(
                        name=plugin_class.__name__,
                        version="1.0.0",
                        description=plugin_class.__doc__ or "No description",
                        author="Unknown"
                    )
                elif isinstance(metadata, dict):
                    metadata = PluginMetadata(**metadata)
                
                plugin = plugin_class(metadata)
                self.logger.info(f"Loaded plugin from module: {module_name}")
                return plugin
            
            self.logger.warning(f"No plugin classes found in module: {module_name}")
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin from module {module_name}: {e}")
            return None
    
    def register_plugin(self, plugin: BasePlugin, config: Optional[Dict[str, Any]] = None) -> bool:
        """Register a plugin with the manager.
        
        Args:
            plugin: Plugin instance to register
            config: Optional configuration for the plugin
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Initialize plugin
            plugin.initialize(config or {})
            plugin._initialized = True
            
            # Register in appropriate category
            self.plugins[plugin.metadata.name] = plugin
            
            if isinstance(plugin, AnalyzerPlugin):
                analyzer_name = plugin.get_analyzer_name()
                self.analyzer_plugins[analyzer_name] = plugin
                self.logger.info(f"Registered analyzer plugin: {analyzer_name}")
            
            elif isinstance(plugin, ProcessorPlugin):
                processor_name = plugin.get_processor_name()
                self.processor_plugins[processor_name] = plugin
                self.logger.info(f"Registered processor plugin: {processor_name}")
            
            elif isinstance(plugin, ExporterPlugin):
                format_name = plugin.get_format_name()
                self.exporter_plugins[format_name] = plugin
                self.logger.info(f"Registered exporter plugin: {format_name}")
            
            elif isinstance(plugin, ValidationPlugin):
                self.validation_plugins[plugin.metadata.name] = plugin
                self.logger.info(f"Registered validation plugin: {plugin.metadata.name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register plugin {plugin.metadata.name}: {e}")
            return False
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin.
        
        Args:
            plugin_name: Name of the plugin to unregister
            
        Returns:
            True if unregistration successful, False otherwise
        """
        if plugin_name not in self.plugins:
            self.logger.warning(f"Plugin not found: {plugin_name}")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            
            # Clean up plugin
            plugin.cleanup()
            
            # Remove from all registries
            del self.plugins[plugin_name]
            
            # Remove from specific registries
            if isinstance(plugin, AnalyzerPlugin):
                analyzer_name = plugin.get_analyzer_name()
                if analyzer_name in self.analyzer_plugins:
                    del self.analyzer_plugins[analyzer_name]
            
            elif isinstance(plugin, ProcessorPlugin):
                processor_name = plugin.get_processor_name()
                if processor_name in self.processor_plugins:
                    del self.processor_plugins[processor_name]
            
            elif isinstance(plugin, ExporterPlugin):
                format_name = plugin.get_format_name()
                if format_name in self.exporter_plugins:
                    del self.exporter_plugins[format_name]
            
            elif isinstance(plugin, ValidationPlugin):
                if plugin_name in self.validation_plugins:
                    del self.validation_plugins[plugin_name]
            
            self.logger.info(f"Unregistered plugin: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister plugin {plugin_name}: {e}")
            return False
    
    def discover_plugins(self) -> List[str]:
        """Discover plugins in registered directories.
        
        Returns:
            List of discovered plugin file paths
        """
        discovered = []
        
        for directory in self.plugin_directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                continue
            
            # Look for Python files
            for file_path in dir_path.glob("*.py"):
                if file_path.name.startswith("__"):
                    continue
                discovered.append(str(file_path))
            
            # Look for plugin packages
            for subdir in dir_path.iterdir():
                if subdir.is_dir() and (subdir / "__init__.py").exists():
                    discovered.append(str(subdir / "__init__.py"))
        
        return discovered
    
    def load_all_plugins(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """Load all discovered plugins.
        
        Args:
            config: Optional configuration dictionary for plugins
            
        Returns:
            Dictionary mapping plugin paths to load success status
        """
        results = {}
        discovered = self.discover_plugins()
        
        for plugin_path in discovered:
            plugin = self.load_plugin_from_file(plugin_path)
            if plugin:
                plugin_config = config.get(plugin.metadata.name, {}) if config else {}
                success = self.register_plugin(plugin, plugin_config)
                results[plugin_path] = success
            else:
                results[plugin_path] = False
        
        return results
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """Get a plugin by name.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin instance or None if not found
        """
        return self.plugins.get(plugin_name)
    
    def get_analyzer_plugin(self, analyzer_name: str) -> Optional[AnalyzerPlugin]:
        """Get an analyzer plugin by analyzer name.
        
        Args:
            analyzer_name: Name of the analyzer
            
        Returns:
            AnalyzerPlugin instance or None if not found
        """
        return self.analyzer_plugins.get(analyzer_name)
    
    def get_available_analyzers(self) -> List[str]:
        """Get list of available analyzer names from plugins.
        
        Returns:
            List of analyzer names
        """
        return list(self.analyzer_plugins.keys())
    
    def get_available_exporters(self) -> List[str]:
        """Get list of available export formats from plugins.
        
        Returns:
            List of export format names
        """
        return list(self.exporter_plugins.keys())
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """List all registered plugins with their metadata.
        
        Returns:
            Dictionary mapping plugin names to metadata
        """
        plugin_info = {}
        
        for name, plugin in self.plugins.items():
            plugin_info[name] = {
                "name": plugin.metadata.name,
                "version": plugin.metadata.version,
                "description": plugin.metadata.description,
                "author": plugin.metadata.author,
                "enabled": plugin.enabled,
                "initialized": plugin.initialized,
                "type": type(plugin).__name__
            }
        
        return plugin_info
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin.
        
        Args:
            plugin_name: Name of the plugin to enable
            
        Returns:
            True if successful, False otherwise
        """
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enable()
            self.logger.info(f"Enabled plugin: {plugin_name}")
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin.
        
        Args:
            plugin_name: Name of the plugin to disable
            
        Returns:
            True if successful, False otherwise
        """
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.disable()
            self.logger.info(f"Disabled plugin: {plugin_name}")
            return True
        return False
    
    def cleanup_all_plugins(self) -> None:
        """Clean up all registered plugins."""
        for plugin_name in list(self.plugins.keys()):
            self.unregister_plugin(plugin_name)
        
        self.logger.info("All plugins cleaned up")