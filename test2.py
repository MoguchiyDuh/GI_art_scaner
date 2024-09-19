from test import parse

with open("2.txt", "r") as file:
    text = file.read()

parse(text)
