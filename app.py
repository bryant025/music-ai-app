import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# 允許前端進行跨域請求 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 Gemini Client (自動讀取環境變數 GEMINI_API_KEY)
client = genai.Client()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/api/recommend")
async def recommend_music(req: PromptRequest):
    try:
        system_instruction = """
        你是一個專業的 AI 音樂推薦與解析引擎。請分析使用者的提示詞，並嚴格以 JSON 格式回傳以下結構：
        {
          "artist_reference": "對標的藝人或樂團風格",
          "mood_vibe": "情緒與情境描述",
          "melody_structure": "旋律與結構特徵",
          "tempo_bpm": "節拍與速度 (例如 75 BPM)",
          "instrumentation": "演出樂器清單",
          "tracks": [
            {
              "title": "推薦曲目名稱 1",
              "artist_style": "風格來源 1",
              "match_score": "匹配度 98%",
              "tags": ["標籤1", "標籤2"]
            },
            {
              "title": "推薦曲目名稱 2",
              "artist_style": "風格來源 2",
              "match_score": "匹配度 94%",
              "tags": ["標籤1", "標籤2"]
            },
            {
              "title": "推薦曲目名稱 3",
              "artist_style": "風格來源 3",
              "match_score": "匹配度 90%",
              "tags": ["標籤1", "標籤2"]
            }
          ]
        }
        請確保回傳內容為嚴格合法的 JSON 格式，切勿包含任何 markdown 程式碼區塊標記（如 ```json）。
        """

        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=req.prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
        )
        
        # 清理可能夾帶的 markdown 標記
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        result_data = json.loads(raw_text)
        return result_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)