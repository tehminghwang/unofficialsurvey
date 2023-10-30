from app import process_query


def test_knows_about_dinosaurs():
    assert (
        process_query("dinosaurs") ==
        "Dinosaurs ruled the Earth 200 million years ago"
    )


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_does_not_know_about_name():
    assert process_query("name") == "teamDOCSSE"


def test_does_not_know_greatest_number():
    assert process_query("largest: 45, 20, 73?") == 73


def test_does_not_know_sum():
    assert process_query("What is 86 plus 39?") == 125


def test_does_not_know_multiply():
    assert process_query("What is 34 multiplied by 14?") == 476
