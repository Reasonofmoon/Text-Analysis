"""Tests for command-line interface."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import sys
from io import StringIO
import json

from ..cli.main import (
    create_cli, main, handle_analyze_command, handle_batch_command,
    handle_config_command, handle_info_command
)


class TestCLI:
    """Test command-line interface functionality."""
    
    def test_create_cli(self):
        """Test CLI parser creation."""
        parser = create_cli()
        
        assert parser.prog is not None
        assert "English Text Analyzer" in parser.description
        
        # Test that subcommands are created
        subparsers_actions = [
            action for action in parser._actions 
            if hasattr(action, 'choices') and action.choices is not None
        ]
        assert len(subparsers_actions) > 0
        
        if subparsers_actions:
            subcommands = subparsers_actions[0].choices
            assert 'analyze' in subcommands
            assert 'batch' in subcommands
            assert 'config' in subcommands
            assert 'info' in subcommands
    
    def test_cli_help(self):
        """Test CLI help output."""
        parser = create_cli()
        
        # Should not raise exception
        help_text = parser.format_help()
        assert "English Text Analyzer" in help_text
        assert "analyze" in help_text
        assert "batch" in help_text
    
    @patch('sys.argv', ['eta'])
    @patch('english_text_analyzer.cli.main.create_cli')
    def test_main_no_command(self, mock_create_cli):
        """Test main function with no command."""
        mock_parser = Mock()
        mock_parser.parse_args.return_value = Mock(command=None)
        mock_create_cli.return_value = mock_parser
        
        result = main()
        
        assert result == 1
        mock_parser.print_help.assert_called_once()
    
    @patch('sys.argv', ['eta', 'analyze', '--text', 'test text'])
    @patch('english_text_analyzer.cli.main.handle_analyze_command')
    @patch('english_text_analyzer.cli.main.ConfigManager')
    def test_main_analyze_command(self, mock_config_manager, mock_handle_analyze):
        """Test main function with analyze command."""
        mock_handle_analyze.return_value = 0
        
        result = main()
        
        assert result == 0
        mock_handle_analyze.assert_called_once()
    
    @patch('english_text_analyzer.cli.main.ConfigManager')
    @patch('english_text_analyzer.cli.main.EnglishTextAnalyzer')
    def test_handle_analyze_command_direct_text(self, mock_analyzer_class, mock_config_manager):
        """Test analyze command with direct text input."""
        # Mock configuration
        mock_config = Mock()
        mock_config.enabled_analyzers = ['vocabulary', 'complexity']
        mock_config_manager_instance = Mock()
        mock_config_manager_instance.load_config.return_value = mock_config
        mock_config_manager.return_value = mock_config_manager_instance
        
        # Mock analyzer
        mock_analyzer = Mock()
        mock_result = Mock()
        mock_result.title = None
        mock_analyzer.analyze_text.return_value = mock_result
        mock_analyzer_class.return_value = mock_analyzer
        
        # Mock arguments
        args = Mock()
        args.text = "Test text to analyze"
        args.title = "Test Title"
        args.input = None
        args.analyzers = None
        args.format = "json"
        args.output = None
        args.quiet = True
        
        # Mock JSONExporter
        with patch('english_text_analyzer.cli.main.JSONExporter') as mock_exporter_class:
            mock_exporter = Mock()
            mock_exporter.export_results.return_value = '{"test": "result"}'
            mock_exporter_class.return_value = mock_exporter
            
            result = handle_analyze_command(args, mock_config_manager_instance)
        
        assert result == 0
        mock_analyzer.analyze_text.assert_called_once_with("Test text to analyze")
        assert mock_result.title == "Test Title"
    
    @patch('english_text_analyzer.cli.main.ConfigManager')
    @patch('english_text_analyzer.cli.main.EnglishTextAnalyzer')
    @patch('builtins.open', create=True)
    def test_handle_analyze_command_file_input(self, mock_open, mock_analyzer_class, mock_config_manager):
        """Test analyze command with file input."""
        # Mock file content
        mock_open.return_value.__enter__.return_value.read.return_value = "File content"
        
        # Mock configuration
        mock_config = Mock()
        mock_config_manager_instance = Mock()
        mock_config_manager_instance.load_config.return_value = mock_config
        mock_config_manager.return_value = mock_config_manager_instance
        
        # Mock analyzer
        mock_analyzer = Mock()
        mock_result = Mock()
        mock_result.title = None
        mock_analyzer.analyze_text.return_value = mock_result
        mock_analyzer_class.return_value = mock_analyzer
        
        # Mock arguments
        args = Mock()
        args.text = None
        args.input = "test.txt"
        args.title = None
        args.analyzers = None
        args.format = "html"
        args.output = "output.html"
        args.quiet = True
        
        # Mock file existence
        with patch('pathlib.Path.exists', return_value=True):
            with patch('english_text_analyzer.cli.main.HTMLReportGenerator') as mock_generator_class:
                mock_generator = Mock()
                mock_generator.generate_report.return_value = "<html>report</html>"
                mock_generator_class.return_value = mock_generator
                
                result = handle_analyze_command(args, mock_config_manager_instance)
        
        assert result == 0
        mock_analyzer.analyze_text.assert_called_once_with("File content")
    
    @patch('english_text_analyzer.cli.main.ConfigManager')
    @patch('english_text_analyzer.cli.main.EnglishTextAnalyzer')
    @patch('english_text_analyzer.cli.main.BatchProcessor')
    @patch('glob.glob')
    def test_handle_batch_command(self, mock_glob, mock_batch_processor_class, mock_analyzer_class, mock_config_manager):
        """Test batch command handling."""
        # Mock glob results
        mock_glob.return_value = ["file1.txt", "file2.txt"]
        
        # Mock configuration
        mock_config = Mock()
        mock_config_manager_instance = Mock()
        mock_config_manager_instance.load_config.return_value = mock_config
        mock_config_manager.return_value = mock_config_manager_instance
        
        # Mock analyzer
        mock_analyzer = Mock()
        mock_analyzer_class.return_value = mock_analyzer
        
        # Mock batch processor
        mock_processor = Mock()
        mock_batch_results = Mock()
        mock_batch_results.successful_results = [Mock(), Mock()]
        mock_batch_results.failed_items = []
        mock_processor.process_files.return_value = mock_batch_results
        mock_processor.create_progress_monitor.return_value = Mock()
        mock_batch_processor_class.return_value = mock_processor
        
        # Mock arguments
        args = Mock()
        args.inputs = ["*.txt"]
        args.output_dir = "results"
        args.format = "html"
        args.summary = False
        args.workers = 4
        args.quiet = True
        
        # Mock file existence and directory creation
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.mkdir'):
                with patch('english_text_analyzer.cli.main.HTMLReportGenerator') as mock_generator_class:
                    mock_generator = Mock()
                    mock_generator.generate_report.return_value = "<html>report</html>"
                    mock_generator_class.return_value = mock_generator
                    
                    with patch('builtins.open', create=True):
                        result = handle_batch_command(args, mock_config_manager_instance)
        
        assert result == 0
        mock_processor.process_files.assert_called_once()
    
    def test_handle_config_command_show(self):
        """Test config show command."""
        mock_config_manager = Mock()
        mock_summary = {"test": "config"}
        mock_config_manager.get_config_summary.return_value = mock_summary
        
        args = Mock()
        args.config_action = "show"
        
        with patch('builtins.print') as mock_print:
            result = handle_config_command(args, mock_config_manager)
        
        assert result == 0
        mock_print.assert_called_once()
        # Verify JSON was printed
        printed_args = mock_print.call_args[0]
        assert json.loads(printed_args[0]) == mock_summary
    
    def test_handle_config_command_set(self):
        """Test config set command."""
        mock_config_manager = Mock()
        
        args = Mock()
        args.config_action = "set"
        args.key = "api_key"
        args.value = "test_key"
        
        with patch('builtins.print') as mock_print:
            result = handle_config_command(args, mock_config_manager)
        
        assert result == 0
        mock_config_manager.update_config.assert_called_once_with({"api_key": "test_key"})
        mock_print.assert_called_once()
    
    def test_handle_config_command_set_json_value(self):
        """Test config set command with JSON value."""
        mock_config_manager = Mock()
        
        args = Mock()
        args.config_action = "set"
        args.key = "enabled_analyzers"
        args.value = '["vocabulary", "grammar"]'
        
        with patch('builtins.print') as mock_print:
            result = handle_config_command(args, mock_config_manager)
        
        assert result == 0
        expected_updates = {"enabled_analyzers": ["vocabulary", "grammar"]}
        mock_config_manager.update_config.assert_called_once_with(expected_updates)
    
    def test_handle_config_command_reset(self):
        """Test config reset command."""
        mock_config_manager = Mock()
        
        args = Mock()
        args.config_action = "reset"
        
        with patch('builtins.print') as mock_print:
            result = handle_config_command(args, mock_config_manager)
        
        assert result == 0
        mock_config_manager.reset_to_defaults.assert_called_once()
        mock_print.assert_called_once()
    
    def test_handle_config_command_invalid_action(self):
        """Test config command with invalid action."""
        mock_config_manager = Mock()
        
        args = Mock()
        args.config_action = "invalid"
        
        result = handle_config_command(args, mock_config_manager)
        
        assert result == 1
    
    @patch('english_text_analyzer.cli.main.platform')
    def test_handle_info_command(self, mock_platform):
        """Test info command handling."""
        mock_platform.platform.return_value = "Test Platform"
        mock_platform.python_version.return_value = "3.9.0"
        mock_platform.architecture.return_value = ["64bit", ""]
        
        mock_config_manager = Mock()
        mock_summary = {"test": "config"}
        mock_config_manager.get_config_summary.return_value = mock_summary
        
        args = Mock()
        
        with patch('builtins.print') as mock_print:
            result = handle_info_command(args, mock_config_manager)
        
        assert result == 0
        mock_print.assert_called_once()
        
        # Verify info structure
        printed_args = mock_print.call_args[0]
        info = json.loads(printed_args[0])
        assert "english_text_analyzer" in info
        assert "system" in info
        assert "configuration" in info
    
    @patch('sys.stdin')
    @patch('english_text_analyzer.cli.main.ConfigManager')
    @patch('english_text_analyzer.cli.main.EnglishTextAnalyzer')
    def test_handle_analyze_command_stdin(self, mock_analyzer_class, mock_config_manager, mock_stdin):
        """Test analyze command with stdin input."""
        # Mock stdin
        mock_stdin.read.return_value = "Text from stdin"
        
        # Mock configuration
        mock_config = Mock()
        mock_config_manager_instance = Mock()
        mock_config_manager_instance.load_config.return_value = mock_config
        mock_config_manager.return_value = mock_config_manager_instance
        
        # Mock analyzer
        mock_analyzer = Mock()
        mock_result = Mock()
        mock_result.title = None
        mock_analyzer.analyze_text.return_value = mock_result
        mock_analyzer_class.return_value = mock_analyzer
        
        # Mock arguments
        args = Mock()
        args.text = None
        args.input = "-"  # stdin
        args.title = None
        args.analyzers = None
        args.format = "json"
        args.output = None
        args.quiet = True
        
        with patch('english_text_analyzer.cli.main.JSONExporter') as mock_exporter_class:
            mock_exporter = Mock()
            mock_exporter.export_results.return_value = '{"test": "result"}'
            mock_exporter_class.return_value = mock_exporter
            
            result = handle_analyze_command(args, mock_config_manager_instance)
        
        assert result == 0
        mock_analyzer.analyze_text.assert_called_once_with("Text from stdin")
    
    def test_handle_analyze_command_no_text(self):
        """Test analyze command with no text input."""
        mock_config_manager = Mock()
        
        args = Mock()
        args.text = None
        args.input = None
        
        # Mock stdin to return empty text
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.read.return_value = ""
            
            result = handle_analyze_command(args, mock_config_manager)
        
        assert result == 1
    
    def test_handle_analyze_command_file_not_found(self):
        """Test analyze command with non-existent file."""
        mock_config_manager = Mock()
        
        args = Mock()
        args.text = None
        args.input = "nonexistent.txt"
        
        with patch('pathlib.Path.exists', return_value=False):
            result = handle_analyze_command(args, mock_config_manager)
        
        assert result == 1


if __name__ == "__main__":
    pytest.main([__file__])