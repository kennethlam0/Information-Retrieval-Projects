Title: The YouTube Tutorial Timestamp Search Engine 

Authors: 
Halle Frey (hallefr), Josh Montroy (montroy), Thomas Bates (trbates), Nick Gaty (nickgaty), and Kenneth Lam (lamken)

Description: 
This project aims to enable users to swiftly locate exact moments in videos where concepts are discussed in the video. The user can search using a query, and then 10 videos will be returned. Additionally, the most relevant part of the video will be indicated, and the link will go straight to that point.

Usage details:
Testing:
use the command line and use: python3 main.py [txt file with queries]
The program will return the ten most relevant videos for each query in the txt document.
Make sure to have each query on its own line.

Launching the UI:
Note: you need to have flask downloaded (pip install flask) and PLEASE USE Google Chrome to view
use the command line and use: python3 run_app.py
Here there will be a local server created and you can go to the main part of the website.
There will be a place to enter a query and when you hit enter, the ten most relevant videos
and times will be returned to you. There will be links to go straight to the videos as well.
To go back to the original page, click the three dashes in the upper left hand corner.

Helpful notes:
- Anything with _pr at the end of the file and subset_term_weights.py is used for evaluation
  purposes. Two sets of files were needed due to using a subset of the data. 
- To run with the entire dataset, call python main.py queryfile
- To run with the subset, call python main_pr.py queryfile

To evaluate the subset output: 
- Run python main_pr.py queries-for-recall-tests.txt > output_pr.txt
This uses the testing queries and redirects the output into the correct file to be read in by evaluation.py
- run python evaluation.py
This will output the MAP and MAR based on the youtubereljudge file compared to the output based on the queries for evaluation (queries in queries-for-recall-tests.txt)

To generate the document_text.py file, comment out everything in main and call the function load_doc_text() and use output redirection to create the .py file. To generate the within_doc_text.py file, comment out main and use output redirection to create the file. Note: you need to manually add the variable name (it has to match the name of the file) and set it equal to the python dictionary.

To make within_doc_termweights.py, comment out everything in main except for the line below the comment “within document output - kenneth”. Then, run the command python main.py > within_doc_termweights.py. This will create the file. Note: you need to manually add the variable name (it has to match the name of the file) and set it equal to the dictionary.

To generate a new document_term_weights or subset_term_weights file first uncomment load_doc_text() in main and run that to generate the necessary txt file. Then uncomment main in the vsm.py file to run a series of functions that will generate, depending on the youtube video json file used, either the document_term_weights or subset_term_weights dictionary that is printed into either file.