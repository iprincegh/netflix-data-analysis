from preprocessing import PreProcessData
from analysis import MovieStats
import analysis

ppd = PreProcessData(filename='netflix_titles.csv', index_column='show_id', null_fill='No item specified')

# ------- load cleaned data ----------------------------------
df = ppd.load_clean_df(save_cd_as='netflix_titles_cleaned.csv')

# ------- load raw data ----------------------------------
df_raw = ppd.load_raw_df()

# -------- plot heat map of null values in data --------
analysis.create_heatplot(raw_data=df_raw, filename='sum_of_nulls_in_columns')

# -------- analysis of types and count of netflix movie/tv show ratings
analysis.netflix_ratings(df=df, plot_filename='netflix_content_ratings', csv_filename='netflix_content_ratings.csv')

# -------- Number of Movies and TV shows in the dataset -----------
analysis.movies_vrs_series(df, 'movies_vrs_series')

# -------- Netflix content production trend over the years -----------
analysis.content_prod_trend(df, plot_filename='content_prod_trend', csv_filename='content_prod_trend.csv')


# -------- Sentiment of content on Netflix -----------------------------
analysis.content_sentiment(df, plot_filename='content_sentiment', csv_filename='content_sentiment.csv')


# --------------- Basic Stats of data ------------

ms = MovieStats(dataframe=df)

ms.basic_stats(sort_column='listed_in', value_column='duration')

ms.basic_stats(sort_column='director', value_column='duration')

ms.basic_stats(sort_column='type', value_column='duration')

ms.basic_stats(sort_column='cast', value_column='duration')

ms.basic_stats(sort_column='country', value_column='duration', float_point=0)

ms.basic_stats(sort_column='rating', value_column='release_year', float_point=0)

ms.basic_stats(sort_column='listed_in', value_column='release_year', float_point=0)

ms.distribution_plots(plot_filename='dist_plot_of_movie_rating_vrs_duration', x_column='rating',
                      y_column='duration',
                      labels=['Rating', 'Movie Duration', 'Distribution of movie rating and duration'], kind='violin')

ms.distribution_plots(plot_filename='dist_plot_of_movie_durations_vrs_countries', x_column='country',
                      y_column='duration',
                      labels=['Country', 'Duration', 'Distribution of movie duration and countries'])

ms.distribution_plots(plot_filename='dist_plot_of_movie_released-yr_vrs_countries', x_column='country',
                      y_column='release_year',
                      labels=['Country', 'release_year', 'Distribution of movie released and country'], kind='violin')
