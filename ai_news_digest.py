#!/usr/bin/env python3
"""
AI News Digest Automation
Searches for recent generative AI updates, particularly from Google,
and sends a daily email digest.
"""

import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote


class AINewsDigest:
    def __init__(self):
        """Initialize the AI News Digest with configuration from environment variables."""
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')

        # Search configuration
        self.search_queries = [
            "Google generative AI latest updates",
            "Google Gemini AI news",
            "Google AI announcements",
            "generative AI breakthroughs Google"
        ]

        # User agent for web requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def search_news(self, query, max_results=5):
        """
        Search for news articles using DuckDuckGo HTML search.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing title, url, and snippet
        """
        results = []
        try:
            # Use DuckDuckGo HTML search
            search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
            response = requests.get(search_url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all result containers
                result_divs = soup.find_all('div', class_='result')

                for div in result_divs[:max_results]:
                    try:
                        # Extract title and URL
                        title_tag = div.find('a', class_='result__a')
                        snippet_tag = div.find('a', class_='result__snippet')

                        if title_tag:
                            title = title_tag.get_text(strip=True)
                            url = title_tag.get('href', '')
                            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ''

                            # Filter for recent and relevant content
                            if url and title:
                                results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'query': query
                                })
                    except Exception as e:
                        print(f"Error parsing result: {e}")
                        continue

            time.sleep(1)  # Be respectful with requests

        except Exception as e:
            print(f"Error searching for '{query}': {e}")

        return results

    def search_google_ai_blog(self):
        """
        Scrape recent posts from Google AI Blog.

        Returns:
            List of dictionaries containing blog post information
        """
        results = []
        try:
            url = "https://blog.google/technology/ai/"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find blog post entries (adjust selectors based on actual page structure)
                articles = soup.find_all('article', limit=5)

                for article in articles:
                    try:
                        title_tag = article.find('h2') or article.find('h3')
                        link_tag = article.find('a', href=True)
                        desc_tag = article.find('p')

                        if title_tag and link_tag:
                            title = title_tag.get_text(strip=True)
                            url = link_tag['href']

                            # Make URL absolute if needed
                            if url.startswith('/'):
                                url = f"https://blog.google{url}"

                            snippet = desc_tag.get_text(strip=True) if desc_tag else ''

                            results.append({
                                'title': title,
                                'url': url,
                                'snippet': snippet,
                                'query': 'Google AI Blog'
                            })
                    except Exception as e:
                        print(f"Error parsing blog post: {e}")
                        continue

        except Exception as e:
            print(f"Error fetching Google AI Blog: {e}")

        return results

    def gather_news(self):
        """
        Gather news from all sources.

        Returns:
            List of all news articles found
        """
        all_news = []

        # Search using queries
        print("Searching for AI news...")
        for query in self.search_queries:
            print(f"  Searching: {query}")
            results = self.search_news(query, max_results=3)
            all_news.extend(results)
            time.sleep(1)

        # Get Google AI Blog posts
        print("Fetching Google AI Blog...")
        blog_posts = self.search_google_ai_blog()
        all_news.extend(blog_posts)

        # Remove duplicates based on URL
        unique_news = []
        seen_urls = set()

        for item in all_news:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_news.append(item)

        print(f"Found {len(unique_news)} unique articles")
        return unique_news

    def create_digest_html(self, news_items):
        """
        Create an HTML email digest from news items.

        Args:
            news_items: List of news article dictionaries

        Returns:
            HTML string for email body
        """
        today = datetime.now().strftime("%B %d, %Y")

        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #1a73e8;
                    border-bottom: 3px solid #1a73e8;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #5f6368;
                    font-size: 14px;
                    text-transform: uppercase;
                    margin-top: 30px;
                }}
                .article {{
                    margin: 20px 0;
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-left: 4px solid #1a73e8;
                    border-radius: 4px;
                }}
                .article-title {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 8px;
                }}
                .article-title a {{
                    color: #1a73e8;
                    text-decoration: none;
                }}
                .article-title a:hover {{
                    text-decoration: underline;
                }}
                .article-snippet {{
                    color: #5f6368;
                    font-size: 14px;
                    margin-top: 8px;
                }}
                .source {{
                    font-size: 12px;
                    color: #80868b;
                    margin-top: 8px;
                    font-style: italic;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #dadce0;
                    font-size: 12px;
                    color: #80868b;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <h1>🤖 Your Daily AI News Digest</h1>
            <h2>{today}</h2>
            <p>Here are the latest updates on generative AI, with a focus on Google's developments:</p>
        """

        if not news_items:
            html += "<p><em>No new articles found today. Check back tomorrow!</em></p>"
        else:
            for item in news_items[:15]:  # Limit to top 15 articles
                html += f"""
                <div class="article">
                    <div class="article-title">
                        <a href="{item['url']}" target="_blank">{item['title']}</a>
                    </div>
                    <div class="article-snippet">{item['snippet']}</div>
                    <div class="source">Source: {item.get('query', 'Web Search')}</div>
                </div>
                """

        html += """
            <div class="footer">
                <p>This digest was automatically generated by your AI News Automation.</p>
                <p>You're receiving this because you configured this automation to run daily.</p>
            </div>
        </body>
        </html>
        """

        return html

    def send_email(self, subject, html_content):
        """
        Send an email with the news digest.

        Args:
            subject: Email subject line
            html_content: HTML content for email body
        """
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            print("ERROR: Email configuration is incomplete!")
            print("Please set SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL environment variables.")
            return False

        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = self.recipient_email

            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)

            # Send email
            print(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                print("Logging in...")
                server.login(self.sender_email, self.sender_password)
                print("Sending email...")
                server.send_message(message)

            print(f"✓ Email sent successfully to {self.recipient_email}")
            return True

        except Exception as e:
            print(f"✗ Error sending email: {e}")
            return False

    def run(self):
        """Main execution method - gather news and send digest."""
        print(f"\n{'='*60}")
        print(f"AI News Digest - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # Gather news
        news_items = self.gather_news()

        # Create digest
        print("\nCreating digest...")
        html_content = self.create_digest_html(news_items)

        # Send email
        subject = f"🤖 AI News Digest - {datetime.now().strftime('%B %d, %Y')}"
        print("\nSending email...")
        success = self.send_email(subject, html_content)

        if success:
            print("\n✓ Digest sent successfully!")
        else:
            print("\n✗ Failed to send digest.")
            # Save to file as backup
            filename = f"digest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"  Digest saved to {filename}")

        print(f"\n{'='*60}\n")


def main():
    """Main entry point."""
    digest = AINewsDigest()
    digest.run()


if __name__ == "__main__":
    main()
