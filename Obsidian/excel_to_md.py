import pandas as pd
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="將 Excel 檔轉換成 Obsidian 實驗紀錄 Markdown 格式")
    parser.add_argument("excel_path", help="輸入的 Excel 檔案路徑")
    parser.add_argument("-o", "--output", help="輸出的 Markdown 檔案路徑 (選填，不填則輸出到螢幕)", default=None)
    
    args = parser.parse_args()
    
    if not os.path.exists(args.excel_path):
        print(f"錯誤：找不到檔案 {args.excel_path}")
        sys.exit(1)
        
    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(args.excel_path)
    except Exception as e:
        print(f"讀取 Excel 檔案時發生錯誤：{e}")
        print("請確認您已安裝必要的套件，您可以執行以下指令安裝：")
        print("pip install pandas openpyxl")
        sys.exit(1)
        
    # 定義預定的欄位名稱
    col_id = '實驗編號'
    col_subject = '研究對象'
    col_result = '結果'
    
    # 檢查 Excel 欄位是否存在
    columns = df.columns.tolist()
    if col_id not in columns or col_subject not in columns or col_result not in columns:
        print(f"⚠️ 警告：找不到預期的標題 ({col_id}, {col_subject}, {col_result})。")
        print(f"目前您的 Excel 中的欄位有：{columns}")
        if len(columns) >= 3:
            print("👉 系統將自動使用「前三個欄位」進行轉換...\n")
            col_id, col_subject, col_result = columns[0], columns[1], columns[2]
        else:
            print("❌ 錯誤：您的 Excel 檔案至少需要有 3 個欄位。")
            sys.exit(1)
            
    md_lines = []
    
    # 逐行處理 Excel 資料
    for index, row in df.iterrows():
        # 若遇到空白欄位則轉換為空字串
        val_id = str(row[col_id]) if pd.notna(row[col_id]) else ""
        val_subject = str(row[col_subject]) if pd.notna(row[col_subject]) else ""
        val_result = str(row[col_result]) if pd.notna(row[col_result]) else ""
        
        # 將浮點數結尾 .0 去除 (例如 2026.0 變成 2026)
        if val_id.endswith('.0'): val_id = val_id[:-2]
        
        md_lines.append(f"#### 實驗編號：{val_id}")
        md_lines.append(f"- **研究對象：** {val_subject}")
        md_lines.append(f"- **結果**：{val_result}")
        md_lines.append("") # 每筆紀錄之間空一行
        
    md_output = "\n".join(md_lines)
    
    # 輸出結果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(md_output)
        print(f"✅ 成功將轉換結果儲存至：{args.output}")
    else:
        print("=" * 45)
        print("以下是轉換結果 (您可以直接複製貼上到 Obsidian)：")
        print("=" * 45 + "\n")
        print(md_output)
        print("=" * 45)

if __name__ == "__main__":
    main()
