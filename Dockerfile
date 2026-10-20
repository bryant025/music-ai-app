# 使用輕量級 Python 3.10 映像檔
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製依賴套件檔並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製後端與前端程式碼
COPY app.py .
COPY index.html .

# 開放 FastAPI 預設對外的 8000 連接埠
EXPOSE 8000

# 啟動 Uvicorn 伺服器 (請確認 app.py 內變數名稱為 app)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]