# Project description
The clociduck project is a project which pupose is to fetch you logged time entries in the Clockify (https://clockify.me) web application, using its api described at https://docs.clockify.me

The projects needs to have scripts or functions that can 
* Fetch all transactions from clockify since the last time you fetched transactions, and save those transactions into a duckdb database table.
* Process transactions in a given date intervall so that logged duration per transactions is rounded up to the nearset 15 minutes given number of hours, so 1 hour and 15 minutes is equal to a durtion of 1,25
* Process the rounded transactions within the same workday, so that the calculated rounded duration of the time is acumulated grouped by the description. So you can get a total duration of hors worked on a given tasks. It must be a sum of the rounded duration.
* Process the summed rounded durations so that they are given calculated start and stop times, for the entire day. Not actual start and stop times but starting at 08:00 and going forward. So if you have two transactions at differnet times but with the same project description, and the first transaction has a rounded duration of 0.75, and the second transaction has a rounded duration of 1.50, then the total duration will be 2.25, meaning that the start time for that task (if we are curently at 8:00 oclock) will be 08:00 and the end time will be 10:15.
* The final processed summed rounded transactions must be shown visually and editabelly using the Streamlit framework
* The final processed summed rounded transactions must also be exportable to an excel spreadsheet.
