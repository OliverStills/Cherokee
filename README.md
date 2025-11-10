# Cherokee - AI News Digest Automation

An automated system that searches the internet for recent updates about generative AI (particularly from Google), summarizes the findings, and emails you a digest every morning at 7 AM.

## Features

- 🔍 **Automated Web Search**: Searches for the latest generative AI news with focus on Google developments
- 📰 **Google AI Blog Integration**: Fetches recent posts directly from Google's AI blog
- 📧 **Email Delivery**: Sends a beautifully formatted HTML digest to your email
- ⏰ **Scheduled Execution**: Runs automatically every morning at 7 AM via cron
- 🎨 **Clean HTML Formatting**: Professional-looking email digest with organized sections

## Prerequisites

- Python 3.7 or higher
- Linux/Mac environment with cron (or Windows Task Scheduler)
- An email account for sending digests (Gmail recommended)

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Email Settings

Copy the example environment file and configure your email settings:

```bash
cp .env.example .env
```

Edit `.env` and fill in your email credentials:

```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password-here
RECIPIENT_EMAIL=recipient@example.com
```

**Important for Gmail users:**
- You need to use an [App Password](https://support.google.com/accounts/answer/185833), not your regular Gmail password
- Enable 2-Factor Authentication on your Google account
- Generate an App Password specifically for this application

### 3. Test the Script

Run the script manually to ensure everything works:

```bash
python3 ai_news_digest.py
```

You should see output showing the search progress and email delivery status.

### 4. Set Up Daily Schedule

Run the setup script to schedule daily execution at 7 AM:

```bash
chmod +x setup_schedule.sh
./setup_schedule.sh
```

This will:
- Create a wrapper script that loads your environment variables
- Add a cron job to run the digest at 7:00 AM daily
- Set up logging to `digest.log`

## Manual Usage

### Run Immediately

```bash
python3 ai_news_digest.py
```

### View Scheduled Jobs

```bash
crontab -l
```

### View Logs

```bash
tail -f digest.log
```

### Remove Scheduled Job

```bash
crontab -e
# Delete the line containing ai_news_digest.py
```

## Configuration

### Email Providers

The default configuration is set up for Gmail, but you can use other providers:

**Outlook/Hotmail:**
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

### Customizing Search Queries

Edit `ai_news_digest.py` and modify the `search_queries` list in the `__init__` method:

```python
self.search_queries = [
    "Google generative AI latest updates",
    "Google Gemini AI news",
    # Add your own queries here
]
```

### Changing Schedule Time

To run at a different time, edit the cron schedule. The format is:

```
minute hour day month weekday command
```

Examples:
- `0 7 * * *` - 7:00 AM daily (default)
- `0 9 * * *` - 9:00 AM daily
- `0 7 * * 1` - 7:00 AM every Monday
- `0 7 1 * *` - 7:00 AM on the 1st of each month

Edit your crontab:
```bash
crontab -e
```

## Troubleshooting

### Email Not Sending

1. **Gmail App Password Issues:**
   - Ensure 2FA is enabled on your Google account
   - Create a new App Password at https://myaccount.google.com/apppasswords
   - Use the 16-character App Password (no spaces)

2. **SMTP Connection Errors:**
   - Check your firewall settings
   - Verify SMTP server and port are correct
   - Try using port 465 with SSL instead of 587 with TLS

3. **Check Logs:**
   ```bash
   cat digest.log
   ```

### No Results Found

- Check your internet connection
- Some websites may block automated requests
- Try running with verbose output to see what's happening

### Cron Job Not Running

1. **Verify cron is running:**
   ```bash
   sudo service cron status
   ```

2. **Check cron logs:**
   ```bash
   grep CRON /var/log/syslog
   ```

3. **Test the wrapper script:**
   ```bash
   ./run_digest.sh
   ```

## Project Structure

```
Cherokee/
├── ai_news_digest.py      # Main Python script
├── requirements.txt        # Python dependencies
├── .env.example           # Example configuration file
├── .env                   # Your configuration (not in git)
├── setup_schedule.sh      # Automated scheduling setup
├── run_digest.sh          # Wrapper script (auto-generated)
├── digest.log             # Execution logs
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Security Notes

- ⚠️ Never commit `.env` file to version control (it's in `.gitignore`)
- Use App Passwords, not your main email password
- Keep your credentials secure
- Regularly rotate your App Passwords

## How It Works

1. **Search Phase**: The script searches for AI news using multiple queries focused on Google's generative AI developments
2. **Aggregation**: Results are collected and deduplicated
3. **Google AI Blog**: Recent posts are fetched directly from Google's official AI blog
4. **Formatting**: All articles are formatted into a clean, professional HTML email
5. **Delivery**: The digest is sent to your specified email address
6. **Scheduling**: Cron runs this process automatically at 7 AM daily

## Future Enhancements

Potential improvements you could make:
- Add AI-powered summarization of articles
- Include sentiment analysis
- Support for multiple recipients
- Web dashboard to view past digests
- RSS feed generation
- Slack/Discord integration
- Custom filters and keywords

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to submit issues and enhancement requests!
