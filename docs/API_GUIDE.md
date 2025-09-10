# Gemini API Key Setup Guide

This guide will help you obtain and configure a Gemini API key for the English Text Analyzer.

## What is the Gemini API?

The Gemini API is Google's generative AI service that powers the text analysis capabilities of this application. The API provides advanced natural language processing capabilities for analyzing English texts.

## Getting Your API Key

### Step 1: Visit Google AI Studio

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account

### Step 2: Create an API Key

1. Click on "Create API Key"
2. Select an existing Google Cloud project or create a new one
3. Your API key will be generated automatically
4. Copy the API key (it starts with "AIza...")

### Step 3: Configure the API Key in the Application

1. Return to the English Text Analyzer
2. Paste your API key in the "Gemini API Key" field
3. Click "Save Key"
4. The key will be stored securely in your browser's local storage

## Important Security Notes

- **Your API key is stored locally**: The key is only stored in your browser's local storage and is never sent to any external servers except Google's Gemini API
- **Keep your key private**: Don't share your API key with others
- **Monitor usage**: Check your API usage in Google Cloud Console to avoid unexpected charges

## API Usage and Pricing

### Free Tier
- Google provides a generous free tier for the Gemini API
- Check current limits at [Google AI Pricing](https://ai.google.dev/pricing)

### Rate Limits
- The free tier includes rate limits
- If you encounter rate limit errors, wait a few minutes before trying again

## Troubleshooting

### "Invalid API key format" Error
- Ensure your API key starts with "AIza"
- Make sure you copied the complete key without extra spaces

### "API request failed" Error
- Check your internet connection
- Verify your API key is correct
- Ensure you haven't exceeded rate limits
- Check if your Google Cloud project has the Gemini API enabled

### "Analysis failed" Error
- Try with a shorter text
- Check if your API key has sufficient quota
- Ensure the text is in English for best results

## Privacy and Data Handling

### What data is sent to Google?
- Only the text you choose to analyze is sent to Google's Gemini API
- No personal information or API keys are stored on external servers

### Data retention
- Google's data retention policies apply to API requests
- Your analysis results are only stored locally in your browser

## Support and Resources

- [Google AI Documentation](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/api/rest)
- [Google Cloud Console](https://console.cloud.google.com/)

## Alternative Setup Methods

### Using Environment Variables (for developers)
If you're running this locally or hosting it yourself, you can set the API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Batch Processing
For analyzing multiple texts, consider:
- Using the batch analysis features in the application
- Monitoring your API usage to stay within limits
- Implementing delays between requests if needed

## Best Practices

1. **Test with short texts first** to ensure your setup works
2. **Monitor your API usage** in Google Cloud Console
3. **Keep your API key secure** and don't commit it to version control
4. **Use appropriate text lengths** - very long texts may hit token limits
5. **Handle errors gracefully** - implement retry logic for temporary failures

## Getting Help

If you encounter issues:

1. Check this guide first
2. Verify your API key setup
3. Test with a simple, short text
4. Check the browser console for error messages
5. Refer to Google's official documentation

Remember: This application runs entirely in your browser and only communicates with Google's Gemini API. Your data and API key remain under your control.