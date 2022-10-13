This method is being tested. Comments and feedback are welcome and encouraged.

**Contents**
1.	Converting library holdings into compatible format
2.	Converting reading list into compatible format
3.	Running code to find matches between the two
4.  Interpreting the results

# 1. Converting library holdings into compatible format
This step needs only to be done periodically in order to keep the file up to date with library holdings.

On Alma Analytics, run a Shelflist (holdings records) report for the locations you would like to check against

Download the report results as a csv file and name it “shelflist.csv”

Create a free account on https://replit.com/

Go to https://replit.com/@QueensCollegeLi

On the line Holdings_csv_to_python_dict, click the 3 dots on the right and click Fork, then Fork Repl. This creates your own copy of the code to work with and you need only go to your own Replit account to find it in the future

In the Files pane on the left, click on the three dots at the top and upload “shelflist.csv”

Click Run at the top. The code may take a while (no more than a minute depending on the csv file size) to run

Once the code has finished, you should see a file named “shelflist_dicts.txt” in the files pane. Download it. This is your library holdings in a compatible format

# 2. Converting reading list into compatible format
To extract metadata from citations in reading lists, use AnyStyle.io. This was created by some of the makers of Zotero and like Zotero, is open source.

Go to https://anystyle.io/

Paste your citations into the box (you should only paste the citations, not any of the other text on the reading lists)

Click Parse X references

Save as xml

# 3. Running code to find matches between reading list and holdings
Go to https://replit.com/@QueensCollegeLi

On the line Reading_list_checker, click the 3 dots on the right and click Fork, then Fork Repl. This creates your own copy of the code to work with and you need only go to your own Replit account to find it in the future

In the “metadata.xml” file, paste your xml from AnyStyle.io

Upload the “shelflist_dicts.txt” (if you haven’t already)

Run the code to see results

# 4/ Interpreting the results
The code compares the following data elements:

Title: the code compares the title string in the reading list citation with the 245 field of bib records (excluding $c), excluding capitalisation and punctuation. If a title from your holdings contains the reading list title string, it will be a title match

Author: the code compares authors or editors from the reading list citations with the 100 field of bib records, excluding capitalisation, punctuation, and initials. If any of the words in the reading list author string appear in the 100 field of your holdings, it will be an author match. This would be better checked against 245 $c, but that is not currently included in the Alma holdings report

Date: the code compares dates from the reading list citations with the 008 date 1 from holdings. If they are the same, it will be a date match

The results are then presented in 6 sections:

Perfect matches: title, author & date

Title & author – usually indicates different edition

Title & date – records that do not have a 100 field cannot have an author match

Just title – these should be checked closely to verify they actually match

Too many matches – citations that have one-word titles can potentially have lots of incorrect title matches. If there are more than 7, they are put here. These will need to be checked in the traditional way

No matches

