## 台灣旅遊 AI 助理

本專案為一份課程作業，旨在透過大型語言模型（LLM）自動生成台灣旅遊資訊，並將結構化的輸出結果呈現在網頁上。專案導入套件管理工具 `uv` 與 GitHub Actions 自動部署等完整 CI/CD 流程。每次提交程式碼，GitHub Pages 都會自動更新並公開展示最新的台灣旅遊資訊網頁！

## 專案核心功能

*   **景點智能推薦**：使用語言模型推薦三個台灣知名景點。
*   **旅遊資訊整合**：自動整理並生成各景點的精簡介紹、當地天氣資訊及旅遊注意事項。
*   **標籤化分類**：為各景點加入相關的標籤，提升閱讀體驗。
*   **結構化網頁輸出**：將 AI 回覆以 JSON 模式（Structured Outputs）解析，並自動更新至網頁。
*   **Token 用量統計**：精確計算每次 API 呼叫所消耗的 Token 數量，以便進行成本控制。
*   **自動化雲端部署**：透過 GitHub Actions 自動觸發執行流程，並使用 GitHub Pages 公開展示產生的網頁。

---

## 使用技術與工具

*   **Python**：負責核心程式執行、邏輯控制與 API 呼叫。
*   **OpenAI Python SDK**：用於串接 Google Gemini 官方提供的 OpenAI 相容 Endpoint 雲端 API，並使用程式內指定的 Gemini LLM 模型。
*   **Structured Outputs / JSON Mode**：強制語言模型輸出標準 JSON 格式，確保資料能準確地填入網頁範本。
*   **python-dotenv**：管理與讀取本機環境變數。
*   **HTML & CSS**：用於建構與呈現旅遊資訊的前端網頁介面。
*   **GitHub Actions**：負責在雲端自動化執行 Python 腳本並啟動部署流程。
*   **GitHub Pages**：展示專案生成網頁的靜態網站託管服務。

---

## 專案結構說明

```text
├── .github/workflows/    # GitHub Actions 自動化腳本
│   └── deploy.yml        # 推送時自動執行 Python 腳本並部署至 GitHub Pages
├── .venv/                # uv 自動建立的 Python 虛擬環境 (本機開發用，納入 .gitignore)
├── .vscode/              # VS Code 編輯器設定
├── src/                  # 專案核心原始碼目錄
│   └── chat.py           # 主要執行程式（負責呼叫語言模型、整理回覆並生成 index.html）
├── .env                  # 環境變數設定檔（用來存放本機金鑰，納入 .gitignore）
├── .gitignore            # Git 忽略檔案清單
├── .python-version       # 專案所使用的 Python 版本（由 uv 自動管理）
├── image.png             # 專案文檔或網頁所需的圖片資源
├── index.html            # 呈現旅遊資訊的網頁介面（由 chat.py 動態覆寫生成）
├── pyproject.toml        # 專案核心設定檔，記錄 Python 專案資訊及第三方套件範圍
├── uv.lock               # 由 uv 自動產生的鎖定檔，鎖定套件版本以確保環境一致
└── README.md             # 說明文件
```

---

## 本地開發 vs 雲端 CI/CD 環境比較表

| 比較項目 | 本地開發環境 (Local Environment) | 雲端自動化環境 (GitHub Actions CI/CD) |
| :--- | :--- | :--- |
| **執行載體** | 開發者本機電腦（Windows） | 雲端虛擬伺服器（GitHub 託管的 `ubuntu-latest`） |
| **觸發方式** | 開發者在終端機手動輸入指令執行 | 程式碼推送（`git push`）至 Github 時自動觸發 |
| **金鑰管理** | 存放於根目錄的 `.env` 檔案（受 `.gitignore` 保護） | 存放於 GitHub 的 `Repository Secrets` 經加密保護 |
| **變數讀取** | 透過 `python-dotenv` 套件載入至程式中 | 透過工作流設定檔（`.yml`）的 `env:` 段落載入環境變數 |
| **套件管理** | 使用 `uv sync` 於本機 `.venv` 中安裝並解析 | 使用 `pip install uv` 搭配 `uv pip install` 於全域環境部署 |
| **產出物呈現** | 直接覆寫本機 `index.html`，需手動用瀏覽器開啟 | 自動封裝產出物並部署至 GitHub Pages 形成公開網站 |

---

## 執行流程與運作機制

```text
[程式啟動] ──> [讀取環境變數/設定] ──> [發送旅遊主題至 Gemini API (經由 OpenAI SDK)]
                                                           │
[顯示 Token 使用量] <── [整理內容並覆寫 index.html] <── [回傳 JSON 結構化資料]
```

1.  **讀取配置**：程式啟動後，會先讀取模型服務的 API 網址、API 金鑰及模型名稱。
2.  **模型請求**：將旅遊主題及結構化需求傳送給語言模型。
3.  **資料處理**：模型回傳景點資料後，`chat.py` 程式會解析內容，並將資料填入、覆寫產生最新的 `index.html` 網頁。
4.  **統計檢視**：最後於終端機顯示本次 API 呼叫的 Token 使用量，產生的網頁可直接使用瀏覽器開啟查看。

---

## Token 使用量說明

為了觀察模型呼叫成本，程式會在執行完畢後統計並輸出本次請求的 Token 使用量，包含以下三個項目：
*   **Prompt Tokens**：傳送給模型的輸入提示內容（含系統指令與使用者需求）所使用的 Token 數量。
*   **Completion Tokens**：模型產生結構化回覆時所消耗的輸出 Token 數量。
*   **Total Tokens**：本次請求的輸入與輸出合計使用的總 Token 數量。
*   *備註：實際使用量會依所選用的模型及模型回覆的文字長度而有所不同。*

---
