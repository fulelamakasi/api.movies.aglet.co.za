import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cronFetchMovies import get_movies, save_movies, get_language_id


class MockResponse:

    def json(self):
        return {
            "results": [
                {
                    "id": 123,
                    "title": "Test Movie",
                    "overview": "A test movie",
                    "release_date": "2025-01-01",
                    "poster_path": "/test.jpg",
                    "backdrop_path": "/backdrop.jpg",
                    "popularity": 50.0,
                    "vote_average": 7.5,
                    "vote_count": 100,
                    "original_language": "en"
                }
            ]
        }


def test_get_movies(mocker):

    mocker.patch("cronFetchMovies.requests.get", return_value=MockResponse())

    movies = get_movies(limit=1)

    assert len(movies) == 1
    assert movies[0]["title"] == "Test Movie"


def test_get_movies_pagination(mocker):

    mocker.patch("cronFetchMovies.requests.get", return_value=MockResponse())

    movies = get_movies(limit=1)

    assert len(movies) <= 1


def test_save_movies(mocker):

    mock_cursor = mocker.Mock()
    mock_connection = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor

    mocker.patch("cronFetchMovies.get_db_connection", return_value=mock_connection)
    mocker.patch("cronFetchMovies.get_language_id", return_value=1)

    movies = [
        {
            "id": 999,
            "title": "Unit Test Movie",
            "overview": "Testing save",
            "release_date": "2024-10-10",
            "poster_path": "/poster.jpg",
            "backdrop_path": "/backdrop.jpg",
            "popularity": 10.0,
            "vote_average": 6.0,
            "vote_count": 50,
            "original_language": "en"
        }
    ]

    save_movies(movies)

    assert mock_cursor.execute.called
    assert mock_connection.commit.called
    assert mock_cursor.close.called
    assert mock_connection.close.called


def test_get_language_id_found(mocker):

    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = {"id": 5}

    mock_connection = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor

    mocker.patch("cronFetchMovies.get_db_connection", return_value=mock_connection)

    result = get_language_id("en")

    assert result == 5


def test_get_language_id_not_found(mocker):

    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = None

    mock_connection = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor

    mocker.patch("cronFetchMovies.get_db_connection", return_value=mock_connection)

    result = get_language_id("xx")

    assert result == 1
