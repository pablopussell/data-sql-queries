# pylint: disable=C0103, missing-docstring
import sqlite3

conn = sqlite3.connect('data/movies.sqlite')
db = conn.cursor()

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    db.execute('''SELECT movies.title, movies.genres, directors.name
                FROM movies
                JOIN directors ON movies.director_id = directors.id''')
    result = db.fetchall()
    # print(result)
    return result


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    db.execute('''SELECT movies.title
                FROM movies
                JOIN directors ON movies.director_id = directors.id
                WHERE movies.start_year  > directors.death_year''')
    result = db.fetchall()
    late_released_movies_list = []
    for title in result:
        late_released_movies_list.append(title[0])
    return late_released_movies_list


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    db.execute(f'''SELECT movies.genres, COUNT(movies.title), AVG(movies.minutes)
                    FROM movies
                    GROUP BY movies.genres
                    HAVING movies.genres = "{genre_name}"''')
    result = db.fetchall()
    stats_dict = {"genre": str(genre_name), "number_of_movies": result[0][1], "avg_length": round(result[0][2], 2)}
    # print(stats_dict)
    return stats_dict


def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    db.execute(f'''SELECT directors.name, COUNT(movies.title) AS movie_count
                FROM movies
                JOIN directors ON movies.director_id = directors.id
                WHERE movies.genres = "{genre_name}"
                GROUP BY directors.name
                ORDER BY movie_count DESC, directors.name ASC
                LIMIT 5
                ''')
    result = db.fetchall()
    return result


def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    top_limit = 30
    bottom_limit = 0
    result_list = []

    db.execute(f'''SELECT MAX(minutes)
                   FROM movies
                    ''')
    result_max_time = db.fetchall()
    max_time = result_max_time[0][0]

    while bottom_limit <= max_time:
        db.execute(f'''SELECT COUNT(*)
                   FROM movies
                   WHERE minutes < {top_limit} AND minutes >= {bottom_limit}
                    ''')
        result = db.fetchall()
        if result[0][0] != 0:
            result_list.append((top_limit, result[0][0]))
        top_limit += 30
        bottom_limit += 30

    return result_list


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    db.execute(f'''SELECT directors.name, movies.start_year-directors.birth_year AS first_movie
                FROM directors
                JOIN movies ON directors.id = movies.director_id
                WHERE first_movie IS NOT NULL
                ORDER BY first_movie ASC
                LIMIT 5''')
    result = db.fetchall()
    return result
