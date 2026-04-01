import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/120WqMn4f6OM0mvrmY-ic5Y-uNUUCTiEoDcPQSOzh9Gk/export?format=csv&gid=0'
df = pd.read_csv(url)

md_lines = []
for i in range(len(df)):
    val_id = str(df.iloc[i, 0])
    if '2026-03-23' in val_id or '260323' in val_id:
        val_subject = str(df.iloc[i].get('目的', ''))
        val_result = str(df.iloc[i].get('結果', ''))
        
        if val_subject == 'nan': val_subject = ""
        if val_result == 'nan': val_result = ""
        
        # Check next line for comment
        if i + 1 < len(df):
            next_row = df.iloc[i+1]
            if str(next_row.iloc[0]).strip().startswith('Comment'):
                comment_text = str(next_row.iloc[1])
                if pd.notna(next_row.iloc[1]) and comment_text != 'nan':
                    if val_result:
                        val_result += f"，{comment_text}"
                    else:
                        val_result = comment_text
                        
        md_lines.append(f"#### 實驗編號：{val_id}")
        md_lines.append(f"- **研究對象：** {val_subject}")
        md_lines.append(f"- **結果**：{val_result}")
        md_lines.append("")

with open("c:/Users/markd/Obsidian/Obsidian/temp_20260323.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
