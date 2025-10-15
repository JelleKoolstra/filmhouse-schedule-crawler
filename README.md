# MovieCrawler

MovieCrawler scrapes weekly agenda pages from a small set of filmhouses in Utrecht, builds
an HTML overview table of films and showtimes, and (optionally) sends the
resulting HTML file to configured Telegram chats.

This repository contains `main.py`, a scraper module (`scraper.py`), an HTML generator
(`html_generator.py`) and a small Telegram uploader (`telegram_bot.py`).

Quick start (for contributors / users)

1. Install the dependencies listed in `requirements.txt`:

```powershell
pip install -r requirements.txt
```

2. Configure your Telegram credentials:

 - Copy `config_template.py` to `config.py` and fill in `BOT_TOKEN` and
   `CHAT_IDS` (list of chat ids as strings).

3. Run the crawler manually (Windows PowerShell) or make a .bat file to add it to a Windows scheduled task:

```powershell
python main.py
```

This will produce `movies_schedule.html` in the project root and will attempt to
send it to the configured Telegram chats.

Notes 

- `FILMHOUSE_URLS` (the public agenda pages the scraper visits) are defined in
  `scraper.py` 
 - The scraper uses Selenium. This project uses `webdriver-manager` to fetch
   and manage the correct ChromeDriver automatically, so contributors do not
   need to install chromedriver manually. `webdriver-manager` is listed in
   `requirements.txt`.
- The HTML generator uses `pandas` styling to keep clickable links in the table.

Contributing

- Improvements to the HTML layout are welcome.

