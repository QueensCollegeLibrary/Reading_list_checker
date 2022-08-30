# Reading_list_checker
Method for automatically checking word-processed reading lists against Alma holdings.

# Turn Alma holdings into python dictionary
[This only needs to be done periodically to keep holdings updated, not for every reading list you check]
1. In Alma Analytics, use the Shelflist (holdings records) report for your library and the records you want to check against.
2. Download your holdings as XML.
3. Input the file path in the create_dicts.py code and run.

# Extract metadata from reading lists
1. Copy and paste citations from reading lists into https://anystyle.io/.
2. Save metadata as XML.
3. In the XML file, find all container-title tags and change to containertitle.
  
# Check reading list XML against holdings dictionary
In the main.py file, put in the correct path to reading list metadata XML file and run.

  The code will check for matches in the following ways:
  1. Title: If the citation title in the reading list is wholly contained in any title in your holdings (case and punctuation are ignored) it will be a title match. NOTE: the flaw in this is that a book entitled e.g. "Ancient Rome" will be matched with any title with the words "ancient rome" consecutively in the title.
  2. Author: The code attempts to find the surname in citations by using the second word in the author string, or third word if the second is only 1 initial. It then checks if this surname appears in author fields in your holdings. NOTE: multiple flaws with this. Names that don't use Given_name Surname structure might not be checked properly; editors are not checked; when there are multiple authors, it checks only the first author given in the citation against the author in the 100 field of the MARC record; the citation will generally use the author's name as it is written in the book, while a MARC 100 field will use the authorised form.
  3. Date: Checks the citation date against the "Begin publication date" in the holdings.
  
# Output
  The code will print to the console the following:
  1. "Perfect matches": titles in holdings matching title, author, and date to a citation.
  2. "Author and title matches": author, title, and MMSID of a holding matching auhtor and title to a citation. (could indicate a different edition)
  3. "Date and title matches": title and MMSID of a holding matching date and title to a citation. (books with editors rather than authors)
  4. "Title matches": titles and MMSIDs in your holdings that contain titles from citations. These contain innaccuracies and the MMSIDs should be checked.
