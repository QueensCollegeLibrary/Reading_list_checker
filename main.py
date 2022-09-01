import json
from bs4 import BeautifulSoup


def remove_punctuation(string):
    punctuation = '''!()-[]{};:'’"\;,<>./?@#$%^&*_~'''
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
    if citation.journal is not None:
        continue
    if citation.find("container-title") is not None:
        citation_title = citation.find("container-title").string
    elif citation.title is not None:
        citation_title = citation.title.string
    else:
        continue
    xml_title = format_title(citation_title)
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
    formatted_citation = main_entry + " " + citation_title + " (" + remove_punctuation(citation_date) + ")"
    for book in shelflist_dicts:
        dict_title = format_title(book["title"])
        if xml_title == dict_title or xml_title in dict_title:
            book["citation_title"] = xml_title
            title_matches.append({"citation": formatted_citation, "book": book})
            if citation.author is not None:
                xml_author = get_surname(citation.author.string.lower())
                dict_author = remove_punctuation(book["author"].lower())
                if xml_author in dict_author:
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
        print("⮩ " + match["book"]["location"] + ": " + match["book"]["classmark"] + " " + match["book"]["mmsid"])

print("\n\n---DATE AND TITLE MATCHES---")
for match in date_matches:
    if match not in perfect_matches:
        print("\n" + match["citation"])
        print("⮩ " + match["book"]["location"] + ": " + match["book"]["classmark"] + " " + match["book"]["mmsid"])

print("\n\n---TITLE MATCHES---")
for match in title_matches:
    if match not in author_matches:
        if match not in date_matches:
            print("\n" + match["citation"])
            print("⮩ " + match["book"]["location"] + ": " + match["book"]["classmark"] + " - " + match["book"]["author"] + ", " + match["book"]["title"] + " " + match["book"]["mmsid"])
