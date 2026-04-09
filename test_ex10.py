def test_length_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f'The phrase is longer than 15 characters: {len(phrase)}'
