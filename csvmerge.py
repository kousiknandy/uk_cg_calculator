import csv
import sys

writer = None
with open(sys.argv[1]) as csvfile:
    with open(sys.argv[2], "w") as outfile:
        reader = csv.DictReader(csvfile)
        p, c = None, None
        for r in reader:
            if not p:
                p = r
            else:
                c = r
                # print(p,c)
                p = {k:v for k,v in p.items() if v}
                c = {k:v.replace(",", "") for k,v in c.items() if v}
                d = {**c, **p}

                if not writer:
                    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                    writer.writeheader()
                writer.writerow(d)
                p, c = None, None
