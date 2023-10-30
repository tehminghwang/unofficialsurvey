from app import process_query
import re

def test_knows_about_dinosaurs():
    assert (
        process_query("dinosaurs") ==
        "Dinosaurs ruled the Earth 200 million years ago"
    )


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_does_not_know_about_name():
    assert process_query("name") == "teamimperial"


def test_does_not_know_greatest_number():
    assert process_query("largest: 45, 20, 73?") == "73"
