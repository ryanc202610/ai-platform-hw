import os
import datetime
from dotenv import load_dotenv
from openai import OpenAI

# 1. 自動載入同目錄下的 .env 檔案環境變數
load_dotenv(override=True)

# 2. 讀取環境變數
base_url = os.getenv("LLM_BASE_URL")
api_key = os.getenv("LLM_API_KEY")
model_name = os.getenv("LLM_MODEL")

# 檢查變數是否正確載入
if not api_key or "your_api_key" in api_key:
    raise ValueError("請先在 .env 檔案中填入正確的 LLM_API_KEY！")

print(f"正在初始化客戶端...")
print(f"Base URL: {base_url}")
print(f"使用模型: {model_name}\n")

# 3. 初始化 OpenAI 客戶端（串接 Gemini OpenAI-Compatible Endpoint）
client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

try:
    # 4. 發送對話請求
    print("正在發送請求給 Gemini...請耐心等候")
    response = client.chat.completions.create(
        model=model_name,
        messages=[
          {"role": "user", "content": "你好！請用繁體中文打個招呼。"}
        ]
    )

    # 5. 印出模型回覆的內容
    reply = response.choices[0].message.content
    print("\n==== Gemini 回覆 ====\n")
    print(reply)
    print("\n=====================\n")

    # 將回覆內容包裝成簡單的 HTML 檔案，儲存在專案根目錄的 index.html (github actions使用)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <title>Gemini AI 對話結果</title>
        <style>
            body {{ font-family: sans-serif; margin: 40px; line-height: 1.6; background: #f4f4f9; color: #333; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; }}
            .reply {{ background: #f8f9fa; padding: 20px; border-left: 5px solid #007bff; white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Gemini 最新對話回應</h1>
            <p><strong>執行時間：</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="reply">{reply}</div>
        </div>
    </body>
    </html>
    """
    # 自動計算出專案的「最外層根目錄」路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)

    # 強制指定 index.html 必須建立在根目錄
    html_path = os.path.join(root_dir, "index.html")

    # 寫入檔案
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"網頁檔案已成功產生至：{html_path}")
    
    # 6. 觀察並印出 Token 費用與消耗狀況
    if response.usage:
        print("【Token 消耗統計】:")
        print(f" ├─ 輸入 Token 數 (Prompt): {response.usage.prompt_tokens}")
        print(f" ├─ 輸出 Token 數 (Completion): {response.usage.completion_tokens}")
        print(f" └─ 總共消耗 Token 數: {response.usage.total_tokens}")
    else:
        print("\n無法取得 Token 消耗數據。")

except Exception as e:
    print(f"\n❌ 呼叫 API 時發生錯誤: {e}")
    print("提示：請檢查 .env 中的 API Key 是否正確，以及網路連線是否正常。")
