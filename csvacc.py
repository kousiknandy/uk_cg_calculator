import csv
import sys

writer = None
with open(sys.argv[1]) as csvfile:
    with open(sys.argv[2], "w") as outfile:
        reader = csv.DictReader(csvfile)
        share, value = 0, 0
        for r in reader:
            if not writer:
                    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + ["Accumulated", "Avg Price", "Gain/Loss"])
                    writer.writeheader()
            if r["Action"] == "Lapse":
                share += int(r["NetSharesDeposited"])
                value += int(r["NetSharesDeposited"]) * float(r["FairMarketValuePrice"].replace("$",""))
                r["Accumulated"] = share
                r["Avg Price"] = round(value / share, 2)
            if r["Action"] == "Sale":
                r["Avg Price"] = round(value / share, 2)
                share -= int(r["Quantity"])
                r["Accumulated"] = share
                r["Gain/Loss"] = round((float(r["SalePrice"].replace("$",""))-r["Avg Price"]) * int(r["Quantity"]), 2)
                value =  r["Avg Price"] * share
            writer.writerow(r)
