# MovieCrawler

MovieCrawler scrapes weekly agenda pages from a small set of filmhouses in Utrecht, builds
an HTML overview table of films and showtimes, and (optionally) sends the
resulting HTML file to configured Telegram chats.

This repository contains the scraper and helper modules under `src/` plus a
small wrapper script in `scripts/`.

Project layout (important files):

```
MovieCrawler/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── config_template.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── scraper.py
│   ├── html_generator.py
│   ├── telegram_bot.py
│   └── config.py    # local secrets (gitignored)
├── scripts/
│   └── moviecrawler.bat
```

Quick start (for contributors / users)

1. Install the dependencies listed in `requirements.txt`:

```powershell
pip install -r requirements.txt
```

2. Configure your Telegram credentials:

 - Copy `config_template.py` to `src/config.py` and fill in `BOT_TOKEN` and
   `CHAT_IDS` (list of chat ids as strings). `src/config.py` is in `.gitignore`
   so it will not be committed.

3. Run the crawler manually (Windows PowerShell) or add it to a Windows scheduled
task using the provided batch file.

Options:

- Run the bundled batch (from project root):

```bat
scripts\moviecrawler.bat
```

- Or run the package entry point directly (python on PATH):

```bat
python -m src.main
```

This will produce `movies_schedule.html` in the project root and will attempt to
send it to the configured Telegram chats.

Notes 

 - `FILMHOUSE_URLS` (the public agenda pages the scraper visits) are defined in
   `src/scraper.py`.
 - The scraper uses Selenium. This project uses `webdriver-manager` to fetch
   and manage the correct ChromeDriver automatically, so contributors do not
   need to install chromedriver manually. `webdriver-manager` is listed in
   `requirements.txt`.
- The HTML generator uses `pandas` styling to keep clickable links in the table.

Contributing

- Improvements to the HTML layout are welcome.

