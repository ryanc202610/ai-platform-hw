import os
import datetime
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. 自動載入同目錄下的 .env 檔案環境變數
load_dotenv(override=True)

# 2. 讀取環境變數
base_url = os.getenv("LLM_BASE_URL")
api_key = os.getenv("LLM_API_KEY")
model_name = os.getenv("LLM_MODEL")

if not api_key or "your_api_key" in api_key:
    raise ValueError("請先在 .env 檔案中填入正確的 LLM API KEY！")

print(f"正在初始化客戶端(Client)...")
print(f"Base URL: {base_url}")
print(f"使用模型: {model_name}\n")

# 初始化 OpenAI 客戶端
client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

try:
    print("正在發送請求給 LLM (使用 JSON Mode 結構化輸出) ... 請耐心等候")

    # 3. 在提示詞 (Prompt) 中, 規範 JSON 的欄位結構
    prompt_message = """
    你好！請幫我生成今日問候。你必須回傳一個 JSON 物件，且精確包含以下四個欄位：
    1. "greeting": 親切的繁體中文問候語。
    2. "ai_status": 你目前的模擬心情或狀態（例如：電力充沛、思路清晰）。
    3. "daily_tip": 給使用者的一句今日正能量短語或實用小建議。
    4. "tags": 一個字串列表（Array of strings），包含 2-3 個繁體中文的標籤分類。

    請注意：只回傳純 JSON 字串，不要包含任何 markdown 標記（如 ```json）。
    """

    # 4. 發送請求
    response = client.chat.completions.create(
        model=model_name,
        messages=[
          {"role": "user", "content": prompt_message}
        ],
        response_format={ "type": "json_object" },
        stream=False
    )
    
    # 5. 解析與讀取結構化資料
    full_json_str = response.choices[0].message.content
    result_data = json.loads(full_json_str)

    print("\n==== LLM 回覆 (結構化 JSON 成果) ====\n")
    print(json.dumps(result_data, indent=2, ensure_ascii=False))
    print("\n=========================================\n")

    # 6. 將結構化內容包裝成 HTML 檔案
    tags_html = "".join([f"<span class='tag'>#{tag}</span>" for tag in result_data.get("tags", [])])

    print("\n==== LLM 回覆 ====\n")
    print(result_data.get("greeting"))
    print("\n=====================\n")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <title>LLM AI 結構化對話結果</title>
        <style>
            body {{ font-family: sans-serif; margin: 40px; line-height: 1.6; background: #f4f4f9; color: #333; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 600px; margin: auto; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .status-bar {{ font-size: 0.9em; color: #666; margin-bottom: 20px; }}
            .reply {{ background: #f8f9fa; padding: 20px; border-left: 5px solid #007bff; border-radius: 4px; font-size: 1.2em; font-weight: bold; margin-bottom: 20px; }}
            .tip {{ background: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
            .tag {{ display: inline-block; background: #e2e8f0; color: #4a5568; padding: 5px 10px; border-radius: 15px; margin-right: 5px; font-size: 0.85em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>LLM 智慧自動化回應</h1>
            <div class="status-bar">
                <p><strong>執行時間：</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>AI 模擬狀態：</strong> <span style="color: #28a745;">{result_data.get("ai_status", "正常")}</span></p>
            </div>
            
            <div class="reply">
                {result_data.get("greeting", "你好！")}
            </div>
            
            <div class="tip">
                <strong>💡 今日小建議：</strong><br>{result_data.get("daily_tip", "保持微笑，迎接美好的一天。")}
            </div>
            
            <div class="tags-container">
                {tags_html}
            </div>
        </div>
    </body>
    </html>
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    html_path = os.path.join(root_dir, "index.html")

    # 寫入最外層根目錄的 index.html
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✨ 網頁檔案已成功產生至：{html_path}")
    print("💡 結構化資料已成功解析並渲染至對應的 HTML 區塊中！")

    # 7. Token 消耗狀況
    if response.usage:
        print("\n【Token 消耗統計】:")
        print(f" ├─ 輸入 Token 數 (Prompt): {response.usage.prompt_tokens}")
        print(f" ├─ 輸出 Token 數 (Completion): {response.usage.completion_tokens}")
        print(f" └─ 總共消耗 Token 數: {response.usage.total_tokens}")

except Exception as e:
    print(f"\n❌ 發生錯誤: {e}")
