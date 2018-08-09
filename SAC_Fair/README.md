Purpose = auto generate UI for dealing with the giant pile of SAC fair registrations
---
csv_extractor_div.py

Inputs = 
1. CSV file with the following column contents in order but actual column names don't matter:
	time stamp
	group name
	group category
	description
	events
	recruiting practices
	recruiter name
	recruiter email
	urls
2. number of rows to skip at the beginning
3. target location of generated divs code

Outputs = 
A.
	1. html + css + js for 1 page of buttons where each item is a div controlled by the button
or B.
	1. html + css + js for dropdown menu page 
	2. files separated by category, each containing html + css formatting that displays the info of club, sorted alphabetically in each category, to be copy-pasted onto some webpage
	3. processing results log

----
deprecated csv_extractor.py

Mostly the same as the above but made using tables instead of divs, probably somewhat unfinished, main problem was that the layout would look bad for certain screen sizes like mobile so I switched to divs