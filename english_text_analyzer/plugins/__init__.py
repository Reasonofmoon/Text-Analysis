"""Plugin architecture for English text analysis."""

from .manager import PluginManager
from .base import BasePlugin, PluginMetadata

__all__ = ['PluginManager', 'BasePlugin', 'PluginMetadata']