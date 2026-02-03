This is a backtester for Moving AVG. 
The data for NVDIA stock of last 4 years was taken from Yahoo Finance as a csv file.
Then pandas was used to take the data from csv file to enter into MySQL database.
About Moving AVG case:
      - For example, user entered 50 and 100 for MA values, the code will calculate the MA50 and MA100 from the
        data of last 4 years of the stock and then provide the data where MA50 crosses the MA100, signaling as
        a buying position and same when MA100 crosses MA50, signalling as a selling position.
      - Then from the extracted data, the total PnL amount from all the trades and amount of PnL percentage per
        trade is provided to the user.
This tester takes the strategy when the user buys at when MA(smaller) crosses MA(bigger) and sell when MA(bigger)
crosses MA(50).


---------
finance.csv consists of the OHLC data with date and volume of NVDIA stock(which was taken for reference data)
