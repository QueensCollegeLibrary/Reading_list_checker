import json
from bs4 import BeautifulSoup

def remove_punctuation(string):
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punc = ""
    for char in string:
        if char not in punctuation:
            no_punc += char
    return no_punc


def get_surname(author):
    if len(author.split()) > 1:
        if len(remove_punctuation(author.split()[1])) > 1:
            return remove_punctuation(author.split()[1])
        else:
            return remove_punctuation(author.split()[2])
    else:
        return remove_punctuation(author)


def format_title(string):
    formatted_string = remove_punctuation(string).lower().strip()
    split_string = formatted_string.split()
    new_string = " ".join(split_string)
    return new_string


with open("shelflist_dicts.txt", "r") as file:
    contents = file.read()
    shelflist_dicts = json.loads(contents)

with open("metadata.xml", encoding="utf8") as file:
    metadata_soup = BeautifulSoup(file, 'html.parser')

title_matches = []
author_matches = []
date_matches = []

for citation in metadata_soup.find_all("sequence"):
    if citation.journal is not None:
        continue
    if citation.containertitle is not None:
        xml_title = format_title(citation.containertitle.string)
    elif citation.title is not None:
        xml_title = format_title(citation.title.string)
    else:
        continue
    for book in shelflist_dicts:
        dict_title = format_title(book["title"])
        if xml_title == dict_title or xml_title in dict_title:
            book["citation_title"] = xml_title
            title_matches.append(book)
            if citation.author is not None:
                xml_author = get_surname(citation.author.string.lower())
                dict_author = remove_punctuation(book["author"].lower())
                if xml_author in dict_author:
                    author_matches.append(book)
            if citation.date is not None:
                xml_date = remove_punctuation(citation.date.string)
                dict_date = book["date"]
                if xml_date == dict_date:
                    date_matches.append(book)

perfect_matches = []
for book in author_matches:
    if book in date_matches:
        perfect_matches.append(book)

print("---PERFECT MATCHES---")
for book in perfect_matches:
    print(book["title"])

print("\n---AUTHOR AND TITLE MATCHES---")
for book in author_matches:
    if book not in perfect_matches:
        print(book["author"] + ": " + book["title"])
        print(book["mmsid"])

print("\n---DATE AND TITLE MATCHES---")
for book in date_matches:
    if book not in perfect_matches:
        print(book["title"])
        print(book["mmsid"])

print("\n---TITLE MATCHES---")
for book in title_matches:
    if book not in author_matches:
        if book not in date_matches:
            print(book["citation_title"].upper())
            print(">" + book["title"])
            print(">" + book["mmsid"])