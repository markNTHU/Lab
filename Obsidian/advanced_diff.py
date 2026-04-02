import pandas as pd

def parse_param(val):
    return str(val).strip() if pd.notna(val) else ""

def diff_segments(a, b, col_name):
    if a == b: return None
    
    # If not a curve format (no '-' or '/'), just simple diff
    if '-' not in a and '/' not in a:
        return f"{col_name}：由 {a} ➡️ 改為 {b}"
        
    segs_a = a.split('-')
    segs_b = b.split('-')
    
    # If segments length mismatch, just print raw
    if len(segs_a) != len(segs_b):
        return f"{col_name}：由 {a} ➡️ 改為 {b}"
        
    diffs = []
    for (sa, sb) in zip(segs_a, segs_b):
        if sa == sb: continue
        
        parts_a = sa.split('/')
        parts_b = sb.split('/')
        if len(parts_a) == 2 and len(parts_b) == 2:
            t_a, m_a = parts_a
            t_b, m_b = parts_b
            
            if t_a != t_b:
                diffs.append(f"溫度 {t_a}➡️{t_b}度")
        else:
            diffs.append(f"段落 {sa}➡️{sb}")
            
    if diffs:
        return f"{col_name}之差異：{', '.join(diffs)}"
    return None

def main():
    url = 'https://docs.google.com/spreadsheets/d/120WqMn4f6OM0mvrmY-ic5Y-uNUUCTiEoDcPQSOzh9Gk/export?format=csv&gid=0'
    df = pd.read_csv(url)
    
    # Define columns to check
    check_cols = ['HfCl4含量(mg)', '硫含量(mg)', 'HfCl4加熱帶加熱曲線', 'S加熱帶加熱曲線', '加熱爐加熱曲線', 'Ar/H2(SCCM)']
    
    md_lines = []
    
    # Filter valid rows
    valid_idxs = [i for i in range(len(df)) if str(df.iloc[i, 0]).startswith('2025-') or str(df.iloc[i, 0]).startswith('2026-')]
    
    for _idx, i in enumerate(valid_idxs):
        val_id = str(df.iloc[i, 0])
        val_subject = str(df.iloc[i].get('目的', ''))
        val_result = str(df.iloc[i].get('結果', ''))
        
        if val_subject == 'nan': val_subject = ""
        if val_result == 'nan': val_result = ""
        
        # Merge comment if exists
        if i + 1 < len(df):
            next_row = df.iloc[i+1]
            if str(next_row.iloc[0]).strip().startswith('Comment'):
                comment_text = str(next_row.iloc[1])
                if pd.notna(next_row.iloc[1]) and comment_text != 'nan':
                    if val_result: val_result += f"，{comment_text}"
                    else: val_result = comment_text
                    
        # Compare with previous experiment
        diff_strs = []
        if _idx > 0:
            prev_i = valid_idxs[_idx - 1]
            for col in check_cols:
                v_prev = parse_param(df.iloc[prev_i].get(col, ''))
                v_curr = parse_param(df.iloc[i].get(col, ''))
                
                # Treat ending .0 as integer for display
                if v_prev.endswith('.0'): v_prev = v_prev[:-2]
                if v_curr.endswith('.0'): v_curr = v_curr[:-2]
                
                diff_str = diff_segments(v_prev, v_curr, col)
                if diff_str:
                    diff_strs.append(diff_str)
                    
        # Output ONLY for 2026-04-02 as a demo
        if '2026-04-02' in val_id or '260402' in val_id:
            md_lines.append(f"#### 實驗編號：{val_id}")
            md_lines.append(f"- **研究對象：** {val_subject}")
            
            if diff_strs:
                md_lines.append(f"- **參數變化：** {'; '.join(diff_strs)}")
            else:
                md_lines.append(f"- **參數變化：** 與前組完全相同")
                
            md_lines.append(f"- **結果**：{val_result}")
            md_lines.append("")

    with open("c:/Users/markd/Obsidian/Obsidian/temp_20260402_diff.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

if __name__ == '__main__':
    main()
