import json
from bs4 import BeautifulSoup


def remove_punctuation(string):
    punctuation = '''!()-[]{};:'’‘"\;,<>./?@#$%^&*_~'''
    no_punc = ""
    for char in string:
        if char not in punctuation:
            no_punc += char
    return no_punc


def format_author(author):
    no_punctuation = remove_punctuation(author)
    formatted_names = no_punctuation.split(" ")
    initials_particles = []
    for name in formatted_names:
        if len(name) == 1:
            initials_particles += name
        if name in ["le", "la", "de", "di"]:
            initials_particles += name
    if len(initials_particles) > 0:
        for initial in initials_particles:
            formatted_names.remove(initial)
    return formatted_names


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

total_citations = 0
counter = 0
for citation in metadata_soup.find_all("sequence"):
    total_citations += 1

print(""" ___              _  _             _    _        _
| . \ ___  ___  _| |<_>._ _  ___  | |  <_> ___ _| |_
|   // ._><_> |/ . || || ' |/ . | | |_ | |<_-<  | |
|_\_\\\___.<___|\___||_||_|_|\_. | |___||_|/__/  |_|
                            <___'
 ___  _              _
|  _>| |_  ___  ___ | |__ ___  _ _
| <__| . |/ ._>/ | '| / // ._>| '_>
`___/|_|_|\___.\_|_.|_\_\\\___.|_|     \n[by HB @ Q]\n""")


for citation in metadata_soup.find_all("sequence"):
    counter += 1
    print("checking " + str(int(counter/total_citations*100)) + "% complete")
    citation_titles = []
    if citation.find("container-title") is not None:
        citation_titles.append(citation.find("container-title").string)
    if citation.title is not None:
        citation_titles.append(citation.title.string)
    if citation.journal is not None and len(citation.journal) > 1:
        citation_titles.append(citation.journal.string)
    if len(citation_titles) == 0:
        continue
    xml_titles = []
    for title in citation_titles:
        xml_titles.append(format_title(title))
    if citation.editor is not None:
        main_entry = citation.editor.string
    elif citation.author is not None:
        main_entry = citation.author.string
    else:
        main_entry = ""
    if citation.date is not None:
        citation_date = citation.date.string
    else:
        citation_date = "[no date]"
    formatted_citation = main_entry + " " + citation_titles[0] + " (" + remove_punctuation(citation_date) + ")"
    for book in shelflist_dicts:
        dict_title = format_title(book["title"])
        for xml_title in xml_titles:
            if xml_title == dict_title or xml_title in dict_title:
                book["citation_title"] = xml_title
                title_matches.append({"citation": formatted_citation, "book": book})
                if citation.author is not None:
                    xml_author_names = format_author(citation.author.string.lower())
                    dict_author = remove_punctuation(book["author"].lower())
                    for name in xml_author_names:
                        if name in dict_author:
                            author_matches.append({"citation": formatted_citation, "book": book})
                if citation.date is not None:
                    xml_date = remove_punctuation(citation.date.string)
                    dict_date = book["date"]
                    if xml_date == dict_date:
                        date_matches.append({"citation": formatted_citation, "book": book})


perfect_matches = []
for match in author_matches:
    if match in date_matches:
        perfect_matches.append(match)

print("\n\n----PERFECT MATCHES---")
for match in perfect_matches:
    print("\n" + match["citation"])
    print("⮩ " + match["book"]["location"] + ": " + match["book"]["classmark"] + " " + match["book"]["mmsid"])

print("\n\n---AUTHOR AND TITLE MATCHES---")
for match in author_matches:
    if match not in perfect_matches:
        print("\n" + match["citation"])
        print(f"⮩ {match['book']['location']}: {match['book']['classmark']} ~ {match['book']['author']}, {match['book']['title']} ({match['book']['date']}) [{match['book']['mmsid']}]")

print("\n\n---DATE AND TITLE MATCHES---")
for match in date_matches:
    if match not in perfect_matches:
        print("\n" + match["citation"])
        print(f"⮩ {match['book']['location']}: {match['book']['classmark']} ~ {match['book']['author']}, {match['book']['title']} ({match['book']['date']}) [{match['book']['mmsid']}]")

print("\n\n---TITLE MATCHES---")
for match in title_matches:
    if match not in author_matches:
        if match not in date_matches:
            print("\n" + match["citation"])
            print(f"⮩ {match['book']['location']}: {match['book']['classmark']} ~ {match['book']['author']}, {match['book']['title']} ({match['book']['date']}) [{match['book']['mmsid']}]")
