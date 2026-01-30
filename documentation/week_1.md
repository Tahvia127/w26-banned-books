The current CSV I am using doesn't have location or ban date, so I'm unable to complete all the tasks for the data exploration Jupyter Notebook. At this moment, I also cannot do the 10 book test because I am lacking some of the required information.

Update: I have chosen to start with the PEN 2024 - 2025 CSV found online. I have been able to finish work for my Jupyter Notebook, and will be looking to run through the next few tasks as I have all the data set up now.

I have three major problems:

1. The test script wants dates in YYYY-MM-DD format. All dates in CSV do not follow this (most are some combination of month and year). However, even as they are formmated without day, the formatting of month/year isn't consistent, which makes trying to sort the data super difficult.

To approach this problem, I want to first get everything in the correct format, so if day is excluded I'll just assume the first of the month. I've asked LLM to write a function that converts stuff, but the formatting of the current dates are so inconsistent, it doesn't really work.

2. When I finally got 10 books that were in the correct format, running through the test script took about 12 minutes. This is an egregious amount of time, so at this point I can't follow through on trying the entire dataset becasuse it would take too long.

3. After the test script finished running, I accesses the data on my new CSV. However, most of the books didn't have avg_search_before and avg_search_after, and I think that because the script kept retrying to find the info (and eventually reaching the limit), it took the program so long to run. But that means I also have a lack of data, so many of the books likely won't have anything significant to report.
