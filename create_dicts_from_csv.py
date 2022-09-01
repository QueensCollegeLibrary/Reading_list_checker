import csv
import json

books = []
#REMEMBER TO NAME YOUR CSV FILE "shelflist.csv"
with open("shelflist.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for book in reader:
        books.append(book)


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_title(book):
    if book["Title"] is None:
        return ""
    else:
        return book["Title"][:-1]


def get_author(book):
    if book["Author"] == "":
        author = ""
        return author
    if has_numbers(book["Author"]):
        for i, c in enumerate(book["Author"]):
            if c.isdigit():
                author = book["Author"][0:i - 1]
                break
    else:
        author = book["Author"]
    if author.count(",") > 1:
        author = author[0:find_nth(book["Author"], ",", 2)]
    if "author" in author:
        author = author.replace("author", "")[:-1]
    if "(" in author:
        author = author[0:find_nth(author, "(", 1)-1]
    if author[-1] == " ":
        author = author[:-1]
    if author[-1] == ",":
        author = author[:-1]
    if author[-1] == ".":
        author = author[:-1]
    if len(author.split()[-1]) == 1:
        author += "."
    else:
        author = author
    return author


book_dicts = []
for book in books:
    book_dict = {
    "location": book["\ufeffLocation Name"],
    "classmark": book["Permanent Call Number"],
    "title": get_title(book),
    "author": get_author(book),
    "date": book["Begin Publication Date"],
    "mmsid": book["MMS Id"]
    }
    book_dicts.append(book_dict)


with open("shelflist_dicts.txt", "w") as file:
    file.write(json.dumps(book_dicts))
