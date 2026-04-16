import csv
import glob
import os

input_files = input_files = glob.glob(os.path.join("data", "*.csv"))

rows = []

#read the files and extract the relevant data for pink morsel and sales
for filepath in input_files:
    with open(filepath, "r",  encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["product"].strip().lower() != "pink morsel":
                continue
            
            quantity = float(row["quantity"])
            price = float(row["price"].replace("$", "").strip())
            sales = quantity * price

            rows.append({
                "sales": sales,
                "date": row["date"].strip(),
                "region": row["region"].strip()
            })

#write the extracted data to a new csv file
output_path = "output.csv"
with open(output_path, "w", newline="",  encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["sales", "date", "region"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Done! {len(rows)} rows written to {output_path}")