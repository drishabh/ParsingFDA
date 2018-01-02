# ParsingFDA

Two programs to parse the FDA safety reports available from their website.

1. query_hard.py ... makes use of FDA API to query required safety reports based on a particular drug. Since FDA API only provides
                     5000 safety reports for each query. The program decomposes the query into smaller time periods (per year, per half year,
                     per quarter year, per month) if a particalar search has more than 5000 safety reports (which will happen quite often.
                     Worst case aspirin ~300,000 safety reports).
                     
2. unzipping.py ... downloads abut ~500 zipped files provided by FDA (json format), unzips them, converts json files to txt, uploads required
                    info in a given MySQL account. Although the program expects a given database with columns to be there in the MySQL 
                    account, it can be easily upgraded to create database and columns from the program (i already had the database set up 
                    so I did not make it completely automatic). It also has an inbuilt json to txt convertor so that we can use the "LOAD" command to load all the data easily into MySQL.
