import csv
import glob
import re

csv_files = glob.glob('/Users/dognnguyen/Sites/keyword-searcher/data/google_planner/halong/*.csv')
merged_data = {}

for f in csv_files:
    with open(f, 'r', encoding='utf-16le', errors='replace') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        try:
            next(reader) # stats name
            next(reader) # date range
            header = next(reader)
        except StopIteration:
            continue
        
        for row in reader:
            if not row or len(row) < 9: continue
            kw = row[0].strip().lower()
            vol = row[2]
            yoy = row[4]
            comp_str = row[5]
            comp_idx = row[6]
            bid = row[8]
            
            comp_map = {
                "Cao": "High",
                "Vừa": "Medium",
                "Trung bình": "Medium",
                "Thấp": "Low",
                "Không xác định": "Unknown",
                "High": "High",
                "Medium": "Medium",
                "Low": "Low"
            }
            comp_eng = comp_map.get(comp_str, comp_str)
            if comp_idx:
                comp_final = f"{comp_eng} ({comp_idx})"
            else:
                comp_final = f"{comp_eng} (0)" if comp_eng != "Unknown" else "Unknown"
            
            bid_fmt = bid if bid else "N/A"
            if bid and bid.isdigit():
                bid_fmt = f"{int(bid):,}".replace(',', '.')
                
            if yoy == "-" or not yoy:
                yoy = "N/A"
                
            if vol == "0" or not vol:
                vol = "N/A"

            merged_data[kw] = {
                'vol': vol,
                'yoy': yoy,
                'comp': comp_final,
                'bid': bid_fmt
            }
            
print(f"Loaded {len(merged_data)} keywords from CSVs.")

md_file = '/Users/dognnguyen/Sites/keyword-searcher/destination/Hạ Long - keyword.md'
with open(md_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_group_b = False
match_count = 0
for i, line in enumerate(lines):
    if "NHÓM 2: TỪ KHÓA MỚI" in line:
        in_group_b = True
    elif line.startswith("## 5. QUALITY GATE"):
        in_group_b = False
        
    if in_group_b and line.strip().startswith('|') and 'STT' not in line and ':---' not in line:
        cols = line.split('|')
        if len(cols) > 10: 
            raw_kw = cols[4].strip()
            # Extract kw from **keyword**
            m = re.match(r'\*\*(.*)\*\*', raw_kw)
            if m:
                kw = m.group(1).lower()
                if kw in merged_data:
                    data = merged_data[kw]
                    cols[6] = f" {data['vol']} "
                    cols[7] = f" {data['yoy']} "
                    cols[8] = f" {data['comp']} "
                    cols[9] = f" {data['bid']} "
                    lines[i] = '|'.join(cols)
                    match_count += 1

with open(md_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Updated {match_count} keywords in the Markdown file.")
