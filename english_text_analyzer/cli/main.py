"""Main CLI application for English text analysis."""

import argparse
import sys
import json
from pathlib import Path
from typing import List, Optional

from ..core.analyzer import EnglishTextAnalyzer
from ..config.manager import ConfigManager
from ..batch.processor import BatchProcessor, BatchItem
from ..reports.html_generator import HTMLReportGenerator
from ..reports.json_exporter import JSONExporter
from ..reports.pdf_generator import PDFReportGenerator


def create_cli() -> argparse.ArgumentParser:
    """Create the command-line interface parser."""
    parser = argparse.ArgumentParser(
        description="English Text Analyzer - Comprehensive linguistic analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single text file
  eta analyze input.txt --output report.html

  # Analyze text from stdin
  echo "Your text here" | eta analyze --format json

  # Batch analyze multiple files
  eta batch *.txt --output-dir results/

  # Generate different report formats
  eta analyze input.txt --format pdf --output report.pdf

  # Use specific analyzers only
  eta analyze input.txt --analyzers vocabulary,grammar

  # Configure API key
  eta config set api_key YOUR_API_KEY
        """
    )
    
    # Global options
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-error output'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze a single text'
    )
    analyze_parser.add_argument(
        'input',
        nargs='?',
        help='Input text file (use - for stdin)'
    )
    analyze_parser.add_argument(
        '--text', '-t',
        help='Text to analyze directly'
    )
    analyze_parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )
    analyze_parser.add_argument(
        '--format', '-f',
        choices=['html', 'json', 'pdf', 'summary'],
        default='html',
        help='Output format'
    )
    analyze_parser.add_argument(
        '--title',
        help='Title for the analysis report'
    )
    analyze_parser.add_argument(
        '--analyzers',
        help='Comma-separated list of analyzers to use'
    )
    analyze_parser.add_argument(
        '--template',
        choices=['teacher', 'student', 'researcher', 'summary'],
        help='Report template to use'
    )
    
    # Batch command
    batch_parser = subparsers.add_parser(
        'batch',
        help='Analyze multiple texts'
    )
    batch_parser.add_argument(
        'inputs',
        nargs='+',
        help='Input text files or patterns'
    )
    batch_parser.add_argument(
        '--output-dir', '-d',
        default='./results',
        help='Output directory for results'
    )
    batch_parser.add_argument(
        '--format', '-f',
        choices=['html', 'json', 'pdf'],
        default='html',
        help='Output format for individual reports'
    )
    batch_parser.add_argument(
        '--summary',
        action='store_true',
        help='Generate batch summary report'
    )
    batch_parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers'
    )
    
    # Config command
    config_parser = subparsers.add_parser(
        'config',
        help='Manage configuration'
    )
    config_subparsers = config_parser.add_subparsers(dest='config_action')
    
    # Config show
    config_subparsers.add_parser(
        'show',
        help='Show current configuration'
    )
    
    # Config set
    set_parser = config_subparsers.add_parser(
        'set',
        help='Set configuration value'
    )
    set_parser.add_argument('key', help='Configuration key')
    set_parser.add_argument('value', help='Configuration value')
    
    # Config reset
    config_subparsers.add_parser(
        'reset',
        help='Reset configuration to defaults'
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        'info',
        help='Show system information'
    )
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Initialize configuration
        config_manager = ConfigManager(args.config)
        
        if args.command == 'analyze':
            return handle_analyze_command(args, config_manager)
        elif args.command == 'batch':
            return handle_batch_command(args, config_manager)
        elif args.command == 'config':
            return handle_config_command(args, config_manager)
        elif args.command == 'info':
            return handle_info_command(args, config_manager)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1
    
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_analyze_command(args, config_manager: ConfigManager) -> int:
    """Handle the analyze command."""
    # Get input text
    if args.text:
        text = args.text
        title = args.title or "Direct Input"
    elif args.input == '-' or not args.input:
        text = sys.stdin.read()
        title = args.title or "Standard Input"
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Input file not found: {args.input}", file=sys.stderr)
            return 1
        
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        title = args.title or input_path.stem
    
    if not text.strip():
        print("No text to analyze", file=sys.stderr)
        return 1
    
    # Initialize analyzer
    config = config_manager.load_config()
    
    # Override analyzers if specified
    if args.analyzers:
        analyzer_list = [name.strip() for name in args.analyzers.split(',')]
        config.enabled_analyzers = analyzer_list
    
    analyzer = EnglishTextAnalyzer(config=config)
    
    # Perform analysis
    if not args.quiet:
        print("Analyzing text...", file=sys.stderr)
    
    results = analyzer.analyze_text(text)
    results.title = title
    
    # Generate output
    if args.format == 'json':
        exporter = JSONExporter()
        output = exporter.export_results(results)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            if not args.quiet:
                print(f"Results saved to {args.output}", file=sys.stderr)
        else:
            print(output)
    
    elif args.format == 'pdf':
        generator = PDFReportGenerator()
        pdf_bytes = generator.generate_report(results, title, args.output)
        
        if not args.output:
            print("PDF format requires --output option", file=sys.stderr)
            return 1
        
        if not args.quiet:
            print(f"PDF report saved to {args.output}", file=sys.stderr)
    
    elif args.format == 'summary':
        exporter = JSONExporter()
        output = exporter.export_summary_only(results)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            if not args.quiet:
                print(f"Summary saved to {args.output}", file=sys.stderr)
        else:
            print(output)
    
    else:  # HTML format
        generator = HTMLReportGenerator()
        html_output = generator.generate_report(results, title)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html_output)
            if not args.quiet:
                print(f"HTML report saved to {args.output}", file=sys.stderr)
        else:
            print(html_output)
    
    return 0


def handle_batch_command(args, config_manager: ConfigManager) -> int:
    """Handle the batch command."""
    # Collect input files
    input_files = []
    for pattern in args.inputs:
        if '*' in pattern or '?' in pattern:
            # Handle glob patterns
            from glob import glob
            matches = glob(pattern)
            input_files.extend(matches)
        else:
            input_files.append(pattern)
    
    if not input_files:
        print("No input files found", file=sys.stderr)
        return 1
    
    # Verify files exist
    valid_files = []
    for file_path in input_files:
        if Path(file_path).exists():
            valid_files.append(file_path)
        else:
            print(f"Warning: File not found: {file_path}", file=sys.stderr)
    
    if not valid_files:
        print("No valid input files", file=sys.stderr)
        return 1
    
    # Initialize analyzer and batch processor
    config = config_manager.load_config()
    analyzer = EnglishTextAnalyzer(config=config)
    batch_processor = BatchProcessor(analyzer, max_workers=args.workers)
    
    # Set up progress monitoring
    if not args.quiet:
        progress_monitor = batch_processor.create_progress_monitor()
        batch_processor.set_progress_callback(progress_monitor)
    
    # Process batch
    if not args.quiet:
        print(f"Processing {len(valid_files)} files...", file=sys.stderr)
    
    batch_results = batch_processor.process_files(valid_files)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate individual reports
    for i, result in enumerate(batch_results.successful_results):
        filename = f"analysis_{i+1}.{args.format}"
        output_path = output_dir / filename
        
        if args.format == 'html':
            generator = HTMLReportGenerator()
            html_output = generator.generate_report(result)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
        
        elif args.format == 'json':
            exporter = JSONExporter()
            json_output = exporter.export_results(result)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
        
        elif args.format == 'pdf':
            generator = PDFReportGenerator()
            pdf_bytes = generator.generate_report(result, output_path=str(output_path))
    
    # Generate summary if requested
    if args.summary:
        from ..batch.comparator import BatchComparator
        comparator = BatchComparator()
        summary = comparator.compare_batch_results(batch_results)
        
        # Save summary report
        summary_path = output_dir / "batch_summary.txt"
        summary_report = comparator.generate_comparison_report(summary)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_report)
        
        # Save summary data
        summary_data_path = output_dir / "batch_summary.json"
        summary_data = comparator.export_comparison_data(summary)
        with open(summary_data_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    if not args.quiet:
        print(f"Batch processing complete. Results saved to {output_dir}", file=sys.stderr)
        print(f"Successful: {len(batch_results.successful_results)}, Failed: {len(batch_results.failed_items)}", file=sys.stderr)
    
    return 0


def handle_config_command(args, config_manager: ConfigManager) -> int:
    """Handle the config command."""
    if args.config_action == 'show':
        config = config_manager.get_config()
        summary = config_manager.get_config_summary()
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    elif args.config_action == 'set':
        # Parse value
        try:
            value = json.loads(args.value)
        except json.JSONDecodeError:
            value = args.value
        
        # Update configuration
        updates = {args.key: value}
        config_manager.update_config(updates)
        print(f"Configuration updated: {args.key} = {value}")
    
    elif args.config_action == 'reset':
        config_manager.reset_to_defaults()
        print("Configuration reset to defaults")
    
    else:
        print("Config action required: show, set, or reset", file=sys.stderr)
        return 1
    
    return 0


def handle_info_command(args, config_manager: ConfigManager) -> int:
    """Handle the info command."""
    import platform
    from .. import __version__
    
    info = {
        "english_text_analyzer": {
            "version": __version__,
            "description": "Comprehensive English text analysis tool"
        },
        "system": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture()[0]
        },
        "configuration": config_manager.get_config_summary()
    }
    
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())