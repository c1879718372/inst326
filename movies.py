#Bruce Reyes Tongkai Chen
"""Identify the most popular movie ratings based on data in two CSV files."""

from argparse import ArgumentParser
import pandas as pd
import sys


def best_movies(movies_path, ratings_path):
    """takes in two parameters: The path to file of movie and path to a file of rating data
    reads each CSV file in own Data Frame
    merges Data frames by item id and movie id
    Returns a stored version of Series by average rattings to the var.
    """
    
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    
    merged_df = pd.merge(ratings_df, movies_df, left_on='item id', right_on = 'movie id')
    
    average_ratings = merged_df.groupby('movie title')['rating'].mean()
    
    return average_ratings.sort_values(ascending=False)


def parse_args(arglist):
    """ Parse command-line arguments.
    
    Args:
        arglist (list of str): a list of command-line arguments.
    
    Returns:
        namespace: the parsed command-line arguments as a namespace with
        variables movie_csv and rating_csv.
    """
    parser = ArgumentParser()
    parser.add_argument("movie_csv", help="CSV containing movie data")
    parser.add_argument("rating_csv", help="CSV containing ratings")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    movies = best_movies(args.movie_csv, args.rating_csv)
    print(movies.head())
