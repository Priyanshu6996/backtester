import pymysql
import csv
import pandas as pd


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Bearcap2006',
    database='backtest'
)

ma1 = int(input("Enter MA period (e.g., 50 for MA50): "))
ma2 = int(input("Enter MA period (e.g., 100 for MA100): "))
cursor = conn.cursor()

if ma1 > ma2:
    ma1, ma2 = ma2, ma1

#MA 50 AND MA 100
# when MA 50 crosses MA100 , consider it a buy, hold it and sell it once, MA50 crosses below MA100
#we will take the last date as the ref

cursor.execute(f"""
     select * from (
                   select DATE, ADJ_CLOSE, ma_1, ma_2,
                   LAG(ma_1,1) OVER (ORDER BY DATE) AS prev_ma1,
                     LAG(ma_2,1) OVER (ORDER BY DATE) AS prev_ma2
                    FROM (
        SELECT
            DATE,
            ADJ_CLOSE,
            AVG(ADJ_CLOSE) OVER (
                ORDER BY DATE
                ROWS BETWEEN {ma1-1} PRECEDING AND CURRENT ROW
            ) AS ma_1,
            AVG(ADJ_CLOSE) OVER (
                ORDER BY DATE
                ROWS BETWEEN {ma2-1} PRECEDING AND CURRENT ROW
            ) AS ma_2
        FROM history
    ) m
) s
WHERE prev_ma1 <= prev_ma2
  AND ma_1 > ma_2
ORDER BY DATE;
""")
    
result = cursor.fetchall()
print()
print("-----BUY SIGNALS-----")
print()
for row in result:
    print(f"{row[0]} | price={row[1]} | ma{ma1}={row[2]} | ma{ma2}={row[3]}")
cursor.execute(f"""
     select * from (
                   select DATE, ADJ_CLOSE, ma_1, ma_2,
                   LAG(ma_1,1) OVER (ORDER BY DATE) AS prev_ma1,
                     LAG(ma_2,1) OVER (ORDER BY DATE) AS prev_ma2
                    FROM (
        SELECT
            DATE,
            ADJ_CLOSE,
            AVG(ADJ_CLOSE) OVER (
                ORDER BY DATE
                ROWS BETWEEN {ma1-1} PRECEDING AND CURRENT ROW
            ) AS ma_1,
            AVG(ADJ_CLOSE) OVER (
                ORDER BY DATE
                ROWS BETWEEN {ma2-1} PRECEDING AND CURRENT ROW
            ) AS ma_2
        FROM history
    ) m
) s
WHERE prev_ma1 >= prev_ma2
  AND ma_1 < ma_2
ORDER BY DATE;
""")
print()
print("-----SELL SIGNALS-----")
print()
result2 = cursor.fetchall()
for row in result2:
    print(f"{row[0]} | price={row[1]} | ma{ma1}={row[2]} | ma{ma2}={row[3]}")
total_profit = 0
tl = len(result2)

print("\n-----TRADE SUMMARY-----\n")
for i in range(tl):
    pnl_percentage = (result2[i][1] - result[i][1]) / result[i][1] * 100
    print(f"Trade {i+1}: Buy at {result[i][1]}, Sell at {result2[i][1]}, Profit: {pnl_percentage:.2f}%")
    total_profit += result2[i][1] - result[i][1]
print()
print(f"Total Profit from strategy: {total_profit}")
cursor.close()

conn.close()
