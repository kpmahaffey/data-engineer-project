import csv
import ast
import logging
import pandas as pd
import datetime as dt
from dateutil.parser import parse

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the variables used throughout the code
movie_list = []
production_company_list = []
movie_production_company_list = []
genre_list = []
movie_genre_list = []
error_list = []


def setup_movie(src_row):
    # Setting values as long as it is valid
    if src_row["release_date"] in ("", None):
        release_year = None
    else:
        release_year = str(parse(src_row["release_date"]).year)
    if src_row["budget"] in ("", None):
        budget = 0
    else:
        budget = int(src_row["budget"])
    if src_row["revenue"] in ("", None):
        revenue = 0
    else:
        revenue = int(src_row["revenue"])
    if src_row["popularity"] in ("", None):
        popularity = 0
    else:
        popularity = float(src_row["popularity"])

    # Appending to the movie list
    movie_list.append(
        {
            "movie_id": int(src_row["id"]),
            "movie_title": src_row["title"],
            "release_date": src_row["release_date"],
            "release_year": release_year,
            "budget": budget,
            "revenue": revenue,
            "profit": revenue - budget,
            "popularity": popularity
        }
    )


def setup_production_company(src_row):
    # Checking for Valid values
    if src_row["production_companies"] not in (None, "", "False"):
        for prod_com in ast.literal_eval(src_row["production_companies"]):
            # Add each production company to individual list and bridge table list with movie
            production_company_list.append(
                {
                    "production_company_id": int(prod_com["id"]),
                    "production_company_name": prod_com["name"]
                }
            )
            movie_production_company_list.append(
                {
                    "movie_id": int(src_row["id"]),
                    "production_company_id": int(prod_com["id"])
                }
            )


def setup_genre(src_row):
    # Checking for valid values
    if src_row["genres"] not in (None, "", "False"):
        for genre in ast.literal_eval(src_row["genres"]):
            # Add each genre to individual list and bridge table list with movie
            genre_list.append(
                {
                    "genre_id": int(genre["id"]),
                    "genre_name": genre["name"]
                }
            )
            movie_genre_list.append(
                {
                    "movie_id": int(src_row["id"]),
                    "genre_id": int(genre["id"])
                }
            )


def load_and_transform(filename):
    with open(filename, "r", encoding='utf-8-sig') as src_fo:
        src_read = csv.DictReader(src_fo)
        # For each source row, execute the setup process
        for src_row in src_read:
            try:
                setup_movie(src_row)
                setup_production_company(src_row)
                setup_genre(src_row)
            except Exception as exc:
                logger.error(f"Error setting up tables: Error Code:{str(exc)}, Error Row: {src_row}")
                error_list.append(
                    {
                        "error_row": src_row,
                        "error_reason": str(exc)
                    }
                )


def export_to_csv(load_trans_time):
    # Convert all lists to DataFrames. Remove duplicates for Genre and Production Company
    # Then sort the DateFrames by the ID columns for non-bridge tables
    movie_df = pd.DataFrame(movie_list).sort_values(by=['movie_id'])
    production_company_df = pd.DataFrame(production_company_list)\
        .drop_duplicates(ignore_index=True).sort_values(by=['production_company_id'])
    genre_df = pd.DataFrame(genre_list). \
        drop_duplicates(ignore_index=True).sort_values(by=['genre_id'])
    movie_production_company_df = pd.DataFrame(movie_production_company_list)
    movie_genre_df = pd.DataFrame(movie_genre_list)
    error_df = pd.DataFrame(error_list)

    # Use pandas to push to csvs without the DataFrame index
    movie_df.to_csv(r'files/output/movie_csv.csv', index=False)
    genre_df.to_csv(r'files/output/genre_csv.csv', index=False)
    production_company_df.to_csv(r'files/output/production_company_csv.csv', index=False)
    movie_production_company_df.to_csv(r'files/output/movie_production_company_csv.csv', index=False)
    movie_genre_df.to_csv(r'files/output/movie_genre_csv.csv', index=False)
    error_df.to_csv(r'files/output/error_data.csv')
    export_time = dt.datetime.now()
    logger.info(f"Export Runtime: {export_time - load_trans_time}, Movies Exported: {len(movie_df.index)}"
                f", Genres Exported: {len(genre_df.index)}, Prod Comps Exported: {len(production_company_df.index)}")


def execute_program(filename):
    # Executes the main loader/transformer and then exports to csv and logs all steps
    begin_time = dt.datetime.now()
    logger.info("Starting Program - Load and Transform")
    load_and_transform(filename)
    load_time = dt.datetime.now()
    logger.info(f"Transform Runtime: {load_time - begin_time}, Movies List: {len(movie_list)}"
                f", Genres List: {len(genre_list)}, Prod Comps List: {len(production_company_list)}")
    export_to_csv(load_time)
    end_time = dt.datetime.now()
    logger.info(f"Program Full Runtime: {end_time - begin_time}, "
                f"Records Loaded: {len(movie_list)}, Number of Errors: {len(error_list)}")
