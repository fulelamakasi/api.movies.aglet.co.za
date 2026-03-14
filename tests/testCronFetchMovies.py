from cronFetchMovies import fetch_movies
from cronFetchMovies import insert_movie
from cronFetchMovies import run_sync

class MockResponse:

    def json(self):
        return {
            "results": [
                {
                    "id": 123,
                    "title": "Test Movie",
                    "overview": "A test movie",
                    "release_date": "2025-01-01"
                }
            ]
        }

def test_fetch_movies(mocker):

    mocker.patch("requests.get", return_value=MockResponse())

    headers = {"Authorization": "Bearer test"}

    movies = fetch_movies(headers, pages=1)

    assert len(movies) == 1
    assert movies[0]["title"] == "Test Movie"

def test_insert_movie():

    class MockCursor:

        def __init__(self):
            self.executed = False

        def execute(self, sql, params):
            self.executed = True
            self.params = params

    cursor = MockCursor()

    movie = {
        "id": 999,
        "title": "Unit Test Movie",
        "overview": "Testing insert",
        "release_date": "2024-10-10"
    }

    insert_movie(cursor, movie)

    assert cursor.executed
    assert cursor.params[1] == "Unit Test Movie"

def test_run_sync(mocker):

    mock_connection = mocker.Mock()

    mock_cursor = mocker.Mock()

    mock_connection.cursor.return_value = mock_cursor

    mocker.patch(
        "fetch_movies.fetch_movies",
        return_value=[
            {
                "id": 1,
                "title": "Cron Test Movie",
                "overview": "Test",
                "release_date": "2024-01-01"
            }
        ]
    )

    headers = {"Authorization": "Bearer test"}

    run_sync(headers, mock_connection)

    assert mock_cursor.execute.called
    assert mock_connection.commit.called
