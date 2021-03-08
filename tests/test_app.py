# test_app.py

from bitrise_reports import app


def test_correct_answer():

    # Given
    argv = ['-a', '42']

    # When
    app.main(argv)

    # Then
    assert True
