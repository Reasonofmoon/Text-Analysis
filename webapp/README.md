# English Text Analyzer - Web Application

A comprehensive web-based tool for analyzing English texts with focus on vocabulary, grammar, structure, content, and complexity analysis. Built for educational purposes and designed to be deployed on GitHub Pages.

## Features

- **Vocabulary Analysis**: CEFR level classification, academic vocabulary identification, collocations and idioms
- **Grammar Analysis**: Sentence types, tense usage, syntactic complexity
- **Structure Analysis**: Text organization, coherence, transition markers
- **Content Analysis**: Main ideas, supporting details, argument structure
- **Complexity Analysis**: Readability scores, CEFR estimation, lexical diversity

## Design

- **Minimal, Artistic UI**: Clean white background with black text and bold container borders
- **Educational Focus**: Designed specifically for teachers and language learners
- **Print-Friendly**: A4-optimized reports for educational materials
- **Responsive**: Works on desktop, tablet, and mobile devices

## Setup

### Prerequisites

- A Google Gemini API key (required for text analysis)
- Modern web browser with JavaScript enabled
- Internet connection for API calls

### Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key (starts with "AIza...")

### Local Development

1. Clone or download this repository
2. Open `index.html` in a web browser
3. Enter your Gemini API key in the configuration section
4. Start analyzing texts!

### GitHub Pages Deployment

1. Fork this repository
2. Go to repository Settings > Pages
3. Select "Deploy from a branch" 
4. Choose "main" branch and "/ (root)" folder
5. Your app will be available at `https://yourusername.github.io/repository-name`

## Usage

1. **Configure API Key**: Enter your Gemini API key and click "Save Key"
2. **Input Text**: Paste or type your English text in the text area
3. **Select Analysis**: Choose which types of analysis to perform
4. **Analyze**: Click "Analyze Text" to start the analysis
5. **View Results**: Review the comprehensive analysis results
6. **Export**: Export results as HTML, PDF, or print directly

## File Structure

```
webapp/
├── index.html              # Main application page
├── static/
│   ├── css/
│   │   ├── style.css       # Main styles (minimal, artistic design)
│   │   └── print.css       # Print-optimized styles for A4 reports
│   └── js/
│       ├── app.js          # Main application controller
│       ├── ui.js           # UI management and interactions
│       ├── analyzer.js     # Analysis engine and API communication
│       └── export.js       # Export functionality (HTML, PDF, print)
└── README.md               # This file
```

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Security

- API keys are stored locally in your browser only
- No data is sent to external servers except Google's Gemini API
- All analysis is performed client-side

## Educational Use

This tool is designed for:
- English teachers creating learning materials
- Language learners analyzing text complexity
- Curriculum developers assessing reading levels
- Researchers studying text characteristics

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Analyze text
- `Ctrl/Cmd + K`: Focus on API key input
- `Escape`: Clear text (when text area is focused)

## Troubleshooting

### API Key Issues
- Ensure your API key starts with "AIza"
- Check that your API key has Gemini API access enabled
- Verify you haven't exceeded your API quota

### Analysis Errors
- Ensure text has at least 10 words for meaningful analysis
- Check your internet connection
- Try refreshing the page if analysis fails

### Export Issues
- For PDF export, use your browser's print function
- HTML export downloads a complete report file
- Print function uses optimized A4 layout

## Contributing

This is part of the English Text Analyzer project. For contributions:
1. Follow the existing code style
2. Test on multiple browsers
3. Ensure accessibility compliance
4. Update documentation as needed

## License

Educational use license - see main project for details.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the browser console for error messages
3. Ensure you have a valid Gemini API key
4. Try with a different text sample

## Version History

- v1.0: Initial web application with core analysis features
- GitHub Pages compatible static deployment
- Minimal, artistic UI design
- Print-friendly A4 report generation