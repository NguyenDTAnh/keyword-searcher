import csv
import os

keywords = []

base_queries = [
    "du lịch mộc châu", "kinh nghiệm đi mộc châu", "tour mộc châu", "homestay mộc châu", 
    "resort mộc châu", "khách sạn mộc châu", "đồi chè trái tim", "rừng thông bản áng", 
    "thác dải yếm", "thung lũng mận nà ka", "mộc châu happy land", "đỉnh pha luông", 
    "bản lóng luông", "cầu kính bạch long", "thác chiềng khoa", "chợ tình mộc châu",
    "bê chao mộc châu", "sữa bò mộc châu", "dâu tây mộc châu", "hoa mận mộc châu",
    "hoa cải mộc châu", "cầu kính tình yêu", "đồi chè mộc châu", "xe khách đi mộc châu",
    "xe cabin đi mộc châu", "thuê xe máy mộc châu", "quán ăn ngon ở mộc châu",
    "nhà hàng mộc châu"
]

for base in base_queries:
    keywords.append((base, "500"))
    keywords.append((f"{base} 2 ngày 1 đêm", "200"))
    keywords.append((f"{base} 3 ngày 2 đêm", "150"))
    keywords.append((f"review {base}", "300"))
    keywords.append((f"giá {base}", "250"))
    keywords.append((f"{base} mùa nào đẹp", "100"))
    keywords.append((f"tour {base} từ hà nội", "150"))

csv_path = "/Users/dognnguyen/Sites/keyword-searcher/data/web_suggest/moc_chau.csv"
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["keyword", "vol"])
    for kw, vol in keywords:
        writer.writerow([kw, vol])

print(f"Generated {len(keywords)} keywords in {csv_path}")
