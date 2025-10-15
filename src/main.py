from .scraper import get_movies_for_week_by_dropdown, FILMHOUSE_URLS
from .html_generator import generate_overview_table
from .telegram_bot import send_document

def main():
    all_week_movies = {}
    for base_url in FILMHOUSE_URLS:
        print(f"\nCollecting weekly data for: {base_url}")
        week_movies = get_movies_for_week_by_dropdown(base_url)
        all_week_movies[base_url] = week_movies
    
    html_content = generate_overview_table(all_week_movies)
    html_file = "movies_schedule.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML table exported to:", html_file)
    
    send_document(html_file)

if __name__ == "__main__":
    main()
