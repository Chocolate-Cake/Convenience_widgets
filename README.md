# Convenience_widgets
Random pieces of code I made to optimize/automate tedious or annoying things. Code probably won't be formatted too nicely because the point was to have a thing that works asap.

---
pages.py

Given some powerpoint or similar where you want to print multiple slides on each page and (may) also want to skip certain slides, input the relevant info and get the page numbers to enter into the "print these specific pages" box in the printing interface. Get number sets for front and back of each page. Is my way of trying to save paper and ink when printing a bunch of powerpoints for class.

---

accounting.py

Randomly generate accounting Q&As to prepare for IB interviews. Create questions where some line item changes by some amount and create answers of effect on various other line items. Is my way of dealing with the fact that existing free practice questions are finite and I've already gone through all of them.

---

op_tree.py

Calculates the current price of call and put options using the replicating portfolio method and risk neutral pricing method, may have some issues with the h variable because I don't know what it's actually supposed to be so I assumed it's the same as the t variable. Was my way of trying to make a checking mechanism for my fnce 206 homework because the replicating portfolio method is insanely tedious and has a lot of room for mistakes when you have a billion rows of equations.

---

data_cleaner.py

Given a source folder, convert all csv files into cropped csv files of default 100 rows, convert all dta files into csv files of default 100 rows. Is my way of handling Stata with no UI and no local Stata software for research because the actual software was on a remote linux server.
