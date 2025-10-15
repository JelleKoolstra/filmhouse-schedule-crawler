# html_generator.py
import pandas as pd

def generate_overview_table(all_week_movies):
    """
    Build a styled HTML overview table from the scraped data.
    The table has columns: Day, Title, Times (with clickable hyperlinks).
    Rows are sorted by day (in the order they appear in the data) and filmhouse order.
    Background colors are set based on filmhouse.
    Returns the HTML string.
    """
    # Flatten the nested data into a list of rows.
    rows = []
    for filmhouse, week_data in all_week_movies.items():
        for day, movies in week_data.items():
            for movie in movies:
                times_html = "<br>".join(
                    [f'<a href="{playing["ticket_link"]}" target="_blank">{playing["time"]}</a>'
                     for playing in movie["playings"]]
                )
                rows.append({
                    "Filmhouse": filmhouse,  # used internally for sorting & styling
                    "Day": day,
                    "Title": movie["title"],
                    "Times": times_html
                })
    
    df = pd.DataFrame(rows)
    
    # Derive the day order dynamically.
    day_order = df["Day"].unique().tolist()
    df["Day"] = pd.Categorical(df["Day"], categories=day_order, ordered=True)
    
    # Helper column for filmhouse order.
    def get_filmhouse_order(filmhouse):
        filmhouse = filmhouse.lower()
        if "springhaver" in filmhouse:
            return 1
        elif "hartlooper" in filmhouse:
            return 2
        elif "slachtstraat" in filmhouse:
            return 3
        else:
            return 99
    df["FilmhouseOrder"] = df["Filmhouse"].apply(get_filmhouse_order)
    df.sort_values(["Day", "FilmhouseOrder"], inplace=True)
    
    # Define row background colors based on filmhouse.
    def get_color(filmhouse):
        filmhouse = filmhouse.lower()
        if "springhaver" in filmhouse:
            return "#DAA06D"  # light orange
        elif "hartlooper" in filmhouse:
            return "lightgreen"  # light green
        elif "slachtstraat" in filmhouse:
            return "#FF6F73"  # light red
        else:
            return "white"
    df["Color"] = df["Filmhouse"].apply(get_color)
    
    # Prepare DataFrame for display.
    display_df = df.drop(columns=["Filmhouse", "FilmhouseOrder"])
    display_df["Color"] = df["Color"]
    
    def color_row(row):
        color = display_df.loc[row.name, "Color"]
        return ['background-color: ' + color] * len(row)
    
    final_df = display_df.drop(columns=["Color"])
    styled_df = (final_df.style
                 .apply(color_row, axis=1)
                 .set_properties(**{'text-align': 'left'})
                 .set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}])
                )
    
    html_content = styled_df.to_html()
    return html_content
