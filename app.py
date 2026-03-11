from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# 你的 MiniMax API Key
API_KEY = "sk-cp-Nv7SThHQAmYAswKXsAE_MS6u3RW_7kcnOQ3YHg8vbgUX6b_r8Hb5egwD21x1TRXSOEhFKqRr_2YtGeV5QGx3rKqre9K7Dj0VIrilnEiAjL5HGQHH7EE9R_w"
BASE_URL = "https://api.minimax.chat/v1"

# 配置客户端
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 首页
@app.route("/")
def home():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    role = data.get("role", "面试候选人")
    
    # 系统提示词
    system_prompt = f"""你是一个专业的{role}面试官。
请根据用户申请的岗位提出面试问题，并给出专业的评价和建议。
保持友好、专业的态度。"""
    
    try:
        response = client.chat.completions.create(
            model="MiniMax-M2.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return jsonify({
            "reply": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({"reply": f"出错啦: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)