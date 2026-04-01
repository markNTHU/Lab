import pandas as pd
import sys

url = 'https://docs.google.com/spreadsheets/d/120WqMn4f6OM0mvrmY-ic5Y-uNUUCTiEoDcPQSOzh9Gk/export?format=csv'
try:
    df = pd.read_csv(url)
except Exception as e:
    with open('c:/Users/markd/Obsidian/Obsidian/temp_output.md', 'w', encoding='utf-8') as f:
        f.write(f"讀取錯誤: {e}")
    sys.exit(1)

col_id, col_subject, col_result = df.columns[0], df.columns[1], df.columns[2]

md_lines = []
for index, row in df.iterrows():
    val_id = str(row[col_id]) if pd.notna(row[col_id]) else ""
    val_subject = str(row[col_subject]) if pd.notna(row[col_subject]) else ""
    val_result = str(row[col_result]) if pd.notna(row[col_result]) else ""
    
    if val_id.endswith('.0'): val_id = val_id[:-2]
    
    md_lines.append(f"#### 實驗編號：{val_id}")
    md_lines.append(f"- **研究對象：** {val_subject}")
    md_lines.append(f"- **結果**：{val_result}")
    md_lines.append("")

with open('c:/Users/markd/Obsidian/Obsidian/temp_output.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))
