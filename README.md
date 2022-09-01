**Contents**
1.	Converting library holdings into compatible format
2.	Converting reading list into compatible format
3.	Running code to find matches between the two

# 1. Converting library holdings into compatible format
This step needs only to be done periodically in order to keep the file up to date with library holdings.

On Alma Analytics, run a Shelflist (holdings records) report for the locations you would like to check against

Download the report results as a csv file and name it “shelflist.csv”

Create a free account on https://replit.com/

Go to https://replit.com/@QueensCollegeLi

On the line Holdings_csv_to_python_dict, click the 3 dots on the right and click Fork, then Fork Repl. This creates your own copy of the code to work with and you need only go to your own Replit account to find it in the future

In the Files pane on the left, click on the three dots at the top and upload “shelflist.csv” (if the file size is too big, try deleting irrelevant columns in the file before uploading. Queens’ has about 40,000 holdings and our csv file is only 4MB so you should all be fine)

Click Run at the top. The code may take a while (no more than a minute depending on the csv file size) to run

Once the code has finished, you should see a file named “shelflist_dicts.txt” in the files pane. Download it. This is your library holdings in a compatible format

# 2. Converting reading list into compatible format
To extract metadata from citations in reading lists, use AnyStyle.io. This was created by some of the makers of Zotero and like Zotero, is open source.

Go to https://anystyle.io/

Paste your citations into the box (you should only paste the citations, not any of the other text on the reading lists; comments following citations e.g. “essential reading”, “recommended edition” etc. should be fine; asterisks before citations should also fine; please report if these additional comments after citations cause complications)

Click Parse X references

Save as xml (if this opens in a new window, you can just leave it there; you might receive a warning about downloading xml files – AnyStyle.io is a trustworthy tool so I wouldn’t worry)

# 3. Running code to find matches between reading list and holdings
Go to https://replit.com/@QueensCollegeLi

On the line Reading_list_checker, click the 3 dots on the right and click Fork, then Fork Repl. This creates your own copy of the code to work with and you need only go to your own Replit account to find it in the future

In the “metadata.xml” file, paste your xml from AnyStyle.io

Upload the “shelflist_dicts.txt” (if you haven’t already)

Run the code to see results
