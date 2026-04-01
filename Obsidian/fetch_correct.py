import pandas as pd
import sys

url = 'https://docs.google.com/spreadsheets/d/120WqMn4f6OM0mvrmY-ic5Y-uNUUCTiEoDcPQSOzh9Gk/export?format=csv'
try:
    df = pd.read_csv(url)
except Exception as e:
    sys.exit(1)

md_lines = ["# 🧪 Google Sheet 實驗紀錄匯入\n"]

for i in range(len(df)):
    row = df.iloc[i]
    val_id = str(row.iloc[0])
    
    # 略過空行或 Comment 行
    if pd.isna(row.iloc[0]) or val_id.strip() == '' or val_id.strip().startswith('Comment'):
        continue
        
    val_subject = str(row.get('目的', ''))
    val_result = str(row.get('結果', ''))
    
    # 將下一行的 Comment 合併進結果中
    if i + 1 < len(df):
        next_row = df.iloc[i+1]
        if str(next_row.iloc[0]).strip().startswith('Comment'):
            comment_text = str(next_row.iloc[1])
            if pd.notna(next_row.iloc[1]) and comment_text != 'nan':
                val_result += f" （備註：{comment_text}）"
                
    if val_subject == 'nan': val_subject = ""
    if val_result == 'nan': val_result = ""
    
    if val_id.endswith('.0'): val_id = val_id[:-2]
    
    md_lines.append(f"#### 實驗編號：{val_id}")
    md_lines.append(f"- **研究對象：** {val_subject}")
    md_lines.append(f"- **結果**：{val_result}")
    md_lines.append("")

output_path = "C:/Users/markd/Obsidian/Obsidian/GoogleSheet實驗紀錄.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"成功輸出至 {output_path}")
