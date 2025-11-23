import csv
import sys
from collections import defaultdict

trades = defaultdict(list)

with open(sys.argv[1]) as csvfile:
    reader =  csv.DictReader(csvfile)
    for r in reader:
        #print(r)
        trades[r["Symbol"]].append((r["Date"], r["Action"], r["Quantity"], r["Price"]))
master = open("sorted_txns.csv", "w")
master_writer  = csv.DictWriter(master, fieldnames=reader.fieldnames + ["Accumulated", "Avg Price", "Gain/Loss"])
master_writer.writeheader()
for sym, trades in trades.items():
    s, v = 0, 0
    with open(sym + ".csv", "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + ["Accumulated", "Avg Price", "Gain/Loss"])
        writer.writeheader()
        for t in trades:
            if t[1] == "Sell":
                try:
                    a = v / s
                except ZeroDivisionError:
                    print("Skipping", sym)
                    break
                s -= int(t[2])
                gl = (float(t[3].replace("$",""))-a) * int(t[2])
                v = a * s
            elif t[1] == "Buy":
                v += int(t[2]) * float(t[3].replace("$", ""))
                s += int(t[2])
                a = v / s
                gl = 0
            else:
                continue
            w = {
                "Date": t[0],
                "Action": t[1],
                "Symbol": sym,
                "Quantity": t[2],
                "Price": t[3],
                "Accumulated": s,
                "Avg Price": round(a, 2),
                "Gain/Loss": round(gl, 2),
            }
            writer.writerow(w)
            master_writer.writerow(w)
master.close()
