
import os
import logging
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
<title>Trí Tuệ Nhân Tạo K26</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<h1>Trí Tuệ Nhân Tạo K26</h1>
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    color: #f5f3ff;
    font-family: Arial, sans-serif;
    background: radial-gradient(circle at top, #312e81, #090b1b 65%);
}

main {
    max-width: 850px;
    margin: auto;
    padding: 35px 18px;
}

header {
    text-align: center;
    padding: 25px 0;
}

.logo { font-size: 45px; }

h1 {
    font-size: clamp(28px, 5vw, 44px);
    margin: 12px 0;
}

header p { color: #c4b5fd; }

.panel {
    background: #11152b;
    border: 1px solid #373568;
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 15px 50px #0005;
}

#chat {
    height: 360px;
    overflow-y: auto;
    padding: 5px;
}

.msg {
    padding: 13px 15px;
    border-radius: 15px;
    margin: 12px 0;
    white-space: pre-wrap;
    line-height: 1.6;
    overflow-wrap: anywhere;
}

.user {
    background: #4338ca;
    margin-left: 12%;
}

.bot {
    background: #202642;
    margin-right: 8%;
}

form {
    display: flex;
    gap: 9px;
    margin-top: 15px;
}

input {
    min-width: 0;
    flex: 1;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #514b85;
    background: #090d20;
    color: white;
    font-size: 16px;
}

button {
    border: 0;
    border-radius: 12px;
    padding: 12px 17px;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    color: #101027;
    font-weight: bold;
    cursor: pointer;
}

button:disabled { opacity: .5; }

.suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 15px;
}

.suggestions button {
    background: #28264b;
    color: #e9d5ff;
}

.note {
    text-align: center;
    color: #a5b4fc;
    font-size: 13px;
    margin-top: 18px;
}
</style>
</head>

<body>
<main>
<header>
    <div class="logo">✦</div>
    <h1>Trí Tuệ Nhân Tạo K26</h1>
    <p>Khám phá tri thức · Sáng tạo không giới hạn</p>
</header>

<section class="panel">
    <div id="chat">
        <div class="msg bot">
            Xin chào! 👋 Mình là trợ lý AI K26.
            Bạn muốn tìm hiểu điều gì hôm nay?
        </div>
    </div>

    <div class="suggestions">
        <button type="button"
            onclick="suggest('Trí tuệ nhân tạo là gì?')">
            AI là gì?
        </button>

        <button type="button"
            onclick="suggest('Viết giúp tôi một bài thơ về tương lai AI')">
            Sáng tác thơ
        </button>

        <button type="button"
            onclick="suggest('Hướng dẫn tôi học Python từ đầu')">
            Học Python
        </button>
    </div>

    <form id="form">
        <input id="question"
            placeholder="Nhập câu hỏi của bạn..."
            autocomplete="off" required>
        <button id="send" type="submit">Gửi ↗</button>
    </form>

    <div class="note">
        AI có thể trả lời chưa chính xác.
        Hãy kiểm chứng thông tin quan trọng.
    </div>
</section>
</main>

<script>
const chat = document.getElementById('chat');
const form = document.getElementById('form');
const input = document.getElementById('question');
const send = document.getElementById('send');
const historyMessages = [];

function addMessage(text, cls) {
    const el = document.createElement('div');
    el.className = 'msg ' + cls;
    el.textContent = text;
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;
    return el;
}

function suggest(text) {
    input.value = text;
    form.requestSubmit();
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const text = input.value.trim();
    if (!text || send.disabled) return;

    addMessage(text, 'user');
    historyMessages.push({
        role: 'user',
        content: text
    });

    input.value = '';
    send.disabled = true;

    const waiting = addMessage('AI đang suy nghĩ...', 'bot');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                messages: historyMessages
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Có lỗi xảy ra.');
        }

        waiting.textContent =
            data.reply || data.error || 'Có lỗi xảy ra.';

        if (data.reply) {
            historyMessages.push({
                role: 'assistant',
                content: data.reply
            });
        }
    } catch (error) {
        waiting.textContent =
            error.message || 'Không kết nối được máy chủ.';
    } finally {
        send.disabled = false;
        input.focus();
        chat.scrollTop = chat.scrollHeight;
    }
});
</script>
</body>
</html>
"""


@app.route("/tro-ly")
@app.route("/chatbot")
def home():
    return render_template_string(HTML)



    safe_messages = []

    for item in messages[-12:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if (
            role not in ("user", "assistant")
            or not isinstance(content, str)
        ):
            continue

        safe_messages.append({
            "role": role,
            "content": content[:4000]
        })
@app.route("/chat", methods=["POST"])
def chat():
    """Chat văn bản qua Gemini API; API key chỉ đọc từ biến môi trường Render."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify(error="Chưa cấu hình GEMINI_API_KEY trong Render > Environment."), 503

    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not isinstance(messages, list) or not messages:
        return jsonify(error="Bạn hãy nhập câu hỏi."), 400

    contents = []
    for item in messages[-12:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content", "")
        if role not in ("user", "assistant") or not isinstance(content, str):
            continue
        content = content.strip()[:4000]
        if not content:
            continue
        contents.append({
            "role": "user" if role == "user" else "model",
            "parts": [{"text": content}]
        })

    if not contents or contents[-1]["role"] != "user":
        return jsonify(error="Tin nhắn chưa hợp lệ."), 400

    payload = {
        "systemInstruction": {
            "parts": [{
                "text": (
                    "Bạn là trợ lý AI thân thiện của website Trí Tuệ Nhân Tạo K26. "
                    "Trả lời bằng tiếng Việt, rõ ràng, hữu ích và phù hợp với người mới học."
                )
            }]
        },
        "contents": contents,
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
    }

    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": api_key
            },
            json=payload,
            timeout=60
        )
        if response.status_code >= 400:
            app.logger.error("Gemini chat lỗi HTTP %s: %s", response.status_code, response.text[:1500])
            if response.status_code in (401, 403):
                return jsonify(error="Gemini từ chối API key. Hãy kiểm tra GEMINI_API_KEY trong Render."), 502
            if response.status_code == 429:
                return jsonify(error="Gemini đang hết hạn mức hoặc gửi quá nhanh. Hãy thử lại sau."), 429
            return jsonify(error="Gemini chưa xử lý được yêu cầu. Hãy kiểm tra model và nhật ký Render."), 502

        result = response.json()
        parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        reply = "\n".join(part.get("text", "") for part in parts if isinstance(part, dict))
        if not reply.strip():
            return jsonify(error="Gemini chưa tạo được câu trả lời. Hãy thử câu hỏi khác."), 502
        return jsonify(reply=reply.strip())

    except requests.exceptions.Timeout:
        return jsonify(error="Gemini phản hồi quá lâu. Bạn hãy thử lại."), 504
    except requests.exceptions.RequestException:
        app.logger.exception("Lỗi kết nối Gemini")
        return jsonify(error="Không kết nối được Gemini. Hãy kiểm tra Internet hoặc thử lại sau."), 502

# ================= TTT AI — TRí Tuệ Nhân Tạo K26 =================
# Trang phân tích ảnh là trang chủ; ảnh gốc được giữ trong trình duyệt.
# Tệp tối đa 500 MB có thể được chọn. Khi gửi để AI mô tả/hỏi đáp,
# trình duyệt tạo bản JPEG thu nhỏ để giảm tải cho máy chủ và API.

app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024

VISION_HTML = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#101416">
<h1>Trí Tuệ Nhân Tạo K26</h1>
<style>
:root{--bg:#101416;--panel:#151b1e;--panel2:#101518;--line:#293438;--text:#e8f1f2;--muted:#829397;--cyan:#5bf0f4;--teal:#42d9cf;--pink:#f27fd2;--green:#7cf0b6;--amber:#ffd479}
*{box-sizing:border-box}html{background:var(--bg)}body{margin:0;background:radial-gradient(ellipse at 82% 18%,rgba(23,100,105,.20),transparent 33%),linear-gradient(180deg,#121719,#0e1214 75%);color:var(--text);font-family:Inter,Segoe UI,Arial,sans-serif;min-height:100vh}body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.19;background-image:linear-gradient(rgba(146,170,175,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(146,170,175,.13) 1px,transparent 1px);background-size:34px 34px;mask-image:linear-gradient(#000,transparent 92%)}button,input{font:inherit}button{cursor:pointer}.page{max-width:1500px;margin:auto;padding:27px 26px 36px;position:relative;z-index:1}.page-heading{text-align:center;margin:0 0 24px}.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:.22em;color:#8c9fa4;margin-bottom:9px}.page-heading h1{font-size:clamp(27px,4vw,42px);margin:0;font-weight:800;letter-spacing:-.035em}.page-heading p{font-size:12px;color:var(--muted);margin:10px 0 0}.shell{border:1px solid #39474b;border-radius:20px;overflow:hidden;background:rgba(13,17,19,.94);box-shadow:0 26px 90px #0008,0 0 0 5px #ffffff03;min-height:650px}.topbar{height:58px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;border-bottom:1px solid var(--line);background:linear-gradient(90deg,#141b1e,#111719)}.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:13px;letter-spacing:.04em}.brand-mark{width:27px;height:27px;border-radius:8px;background:linear-gradient(135deg,#55f4f7,#48b6c6);display:grid;place-items:center;color:#071619;font-size:16px;font-weight:900;box-shadow:0 0 20px #54eff42a}.brand small{display:block;margin-top:3px;color:#82969b;font-size:9px;letter-spacing:.17em;font-weight:600}.top-right{display:flex;align-items:center;gap:15px;color:#819296;font-size:12px}.status-dot{display:inline-block;width:7px;height:7px;background:#7bf0b4;box-shadow:0 0 12px #7bf0b4;border-radius:50%;margin-right:7px}.mobile-menu{display:none}.appbody{display:grid;grid-template-columns:78px minmax(0,1fr)}.sidebar{border-right:1px solid var(--line);padding:17px 9px;display:flex;flex-direction:column;align-items:center;gap:7px;background:#111719}.navitem{width:58px;min-height:57px;border:0;border-radius:10px;background:transparent;color:#829196;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;font-size:9px;position:relative;transition:.18s}.navitem .ico{font-size:18px;line-height:1}.navitem:hover,.navitem.active{background:linear-gradient(115deg,#203235,#19282b);color:#78f3f1}.navitem.active:before{content:"";position:absolute;left:-9px;top:11px;bottom:11px;width:3px;background:var(--cyan);box-shadow:0 0 12px var(--cyan);border-radius:0 3px 3px 0}.nav-spacer{flex:1}.mainarea{min-width:0;padding:20px}.sectionhead{display:flex;align-items:flex-start;justify-content:space-between;gap:15px;margin-bottom:17px}.sectionhead h2{font-size:20px;margin:0 0 5px;letter-spacing:-.02em}.sectionhead p{font-size:11px;color:var(--muted);margin:0}.chip{border:1px solid #34484c;background:#152023;color:#93cacc;border-radius:6px;padding:7px 9px;font-size:9px;letter-spacing:.08em;white-space:nowrap}.workspace{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(235px,.72fr);gap:14px}.leftcol,.rightcol{min-width:0}.card{border:1px solid #29373b;border-radius:13px;background:linear-gradient(150deg,rgba(25,32,35,.95),rgba(16,21,23,.95));overflow:hidden;box-shadow:inset 0 1px #ffffff05}.cardhead{padding:14px 15px;display:flex;align-items:center;justify-content:space-between;gap:10px;border-bottom:1px solid #283337}.cardtitle{font-size:12px;font-weight:750}.cardsub{font-size:9px;color:var(--muted);margin-top:4px}.tiny{font-size:9px;color:#8b9b9f;letter-spacing:.08em}.preview{position:relative;min-height:270px;max-height:550px;margin:12px;border:1px dashed #40575b;border-radius:9px;background:radial-gradient(ellipse at 50% 40%,#2132357a,transparent 63%),#0a1012;display:flex;justify-content:center;align-items:center;overflow:hidden;transition:border-color .2s,box-shadow .2s}.preview.dragover{border-color:var(--cyan);box-shadow:inset 0 0 35px #5bf0f417}.preview.has-image{border-style:solid;min-height:100px}.preview img{display:block;width:100%;height:auto;max-height:520px;object-fit:contain;position:relative;z-index:1}.preview canvas{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none}.empty{text-align:center;max-width:370px;padding:28px 18px}.uploadico{height:52px;width:52px;margin:0 auto 14px;display:grid;place-items:center;border:1px solid #42666a;background:#163034;border-radius:14px;color:var(--cyan);font-size:23px;box-shadow:0 0 25px #52edf30e}.empty h3{font-size:14px;margin:0 0 8px}.empty p{color:#89999d;font-size:11px;line-height:1.7;margin:0}.btn{border:1px solid #45666a;border-radius:8px;padding:10px 13px;background:linear-gradient(110deg,#6ef1ef,#65cfd7);color:#071517;font-size:11px;font-weight:800;box-shadow:0 0 20px #54e9e915}.btn:hover{filter:brightness(1.08);transform:translateY(-1px)}.btn.secondary{background:#192528;border-color:#35464a;color:#d7e5e7;box-shadow:none}.btn:disabled{opacity:.45;cursor:not-allowed;transform:none}.actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:0 12px 12px}.filebar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:0 13px 12px;color:#87989c;font-size:10px}.fileinfo{overflow-wrap:anywhere}.hidden{display:none!important}.scanline{position:absolute;left:0;right:0;height:3px;top:-5px;opacity:0;z-index:3;background:linear-gradient(90deg,transparent,#59f0f4,#a0ffff,transparent);box-shadow:0 0 18px #59f0f4}.scanning .scanline{opacity:1;animation:scan 2s linear infinite}@keyframes scan{0%{top:0}100%{top:100%}}.pulse{animation:pulse 1.2s ease-in-out infinite alternate}@keyframes pulse{from{opacity:.55}to{opacity:1}}.bottomgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:12px}.metric{border:1px solid #2b3a3d;border-radius:11px;padding:12px;background:linear-gradient(140deg,#192326,#111719);min-width:0}.metrichead{font-size:9px;letter-spacing:.08em;color:#8ba0a4;text-transform:uppercase;display:flex;align-items:center;justify-content:space-between;gap:5px}.metricnum{font-size:23px;font-weight:800;letter-spacing:-.04em;margin-top:10px;color:#7ff5f0}.metricnote{font-size:9px;line-height:1.5;color:#7e9094;margin-top:6px;overflow-wrap:anywhere}.mini-bars{height:4px;border-radius:99px;background:#28383c;overflow:hidden;margin-top:10px}.mini-bars span{display:block;height:100%;width:0;background:linear-gradient(90deg,#5bf0f4,#b17dff);transition:width .4s}.rightcol{display:flex;flex-direction:column;gap:12px}.resultcard{flex:1}.detailbody{padding:15px}.modelrow{display:flex;align-items:center;gap:10px;border:1px solid #344145;background:#12191b;border-radius:9px;padding:10px}.modelicon{width:33px;height:33px;display:grid;place-items:center;border-radius:8px;background:#193437;color:#74efee;font-size:16px}.modelname{font-size:11px;font-weight:750}.modeldesc{font-size:9px;color:#829398;line-height:1.45;margin-top:4px}.modelstate{margin-left:auto;font-size:9px;color:var(--amber);text-align:right;min-width:56px}.detail-section{margin-top:18px}.detailtitle{display:flex;align-items:center;justify-content:space-between;font-size:10px;font-weight:800;letter-spacing:.06em;margin-bottom:10px}.detailtitle span{font-weight:500;color:#7d9094;letter-spacing:0}.kv{display:flex;justify-content:space-between;gap:10px;margin:9px 0;font-size:10px}.kv span:first-child{color:#7f9195}.kv span:last-child{text-align:right;color:#d0dddf;overflow-wrap:anywhere}.divider{height:1px;background:#283538;margin:15px 0}.results{display:flex;flex-direction:column;gap:8px}.emptyresults{border:1px dashed #314246;background:#111719;border-radius:9px;padding:18px 10px;text-align:center;font-size:10px;line-height:1.7;color:#85979b}.resultitem{background:#121a1c;border:1px solid #29393d;padding:10px;border-radius:9px}.resulttop{display:flex;align-items:center;gap:8px}.resulticon{width:27px;height:27px;display:grid;place-items:center;border-radius:7px;background:#20373a;color:#7cf5f1;flex-shrink:0}.resultname{font-size:10px;font-weight:700;flex:1}.percent{font-size:10px;color:#79f4ee;font-weight:800}.bar{height:3px;background:#2a393c;border-radius:99px;margin-top:9px;overflow:hidden}.barfill{height:100%;background:linear-gradient(90deg,#4bd4d5,#80f7ed);border-radius:99px}.description{font-size:11px;line-height:1.75;color:#cbd8da;white-space:pre-wrap;overflow-wrap:anywhere}.questionbox{display:flex;gap:6px;margin-top:10px}.questionbox input{min-width:0;flex:1;padding:10px;border-radius:7px;border:1px solid #344448;background:#0c1214;color:var(--text);font-size:11px;outline:none}.questionbox input:focus{border-color:#55dfe1}.questionbox button{padding:0 12px;border:0;border-radius:7px;background:#65e9e8;color:#071719;font-weight:850}.fineprint{font-size:9px;color:#718387;line-height:1.6;margin-top:9px}.footer{display:flex;justify-content:space-between;gap:15px;color:#6f8084;font-size:9px;line-height:1.6;margin-top:17px}.toast{position:fixed;bottom:22px;left:50%;transform:translate(-50%,15px);opacity:0;pointer-events:none;background:#e3ffff;color:#071719;padding:11px 15px;border-radius:9px;font-size:12px;font-weight:750;box-shadow:0 10px 30px #0006;transition:.25s;z-index:99;max-width:calc(100% - 32px)}.toast.show{opacity:1;transform:translate(-50%,0)}
@media(max-width:960px){.page{padding:19px 13px}.workspace{grid-template-columns:minmax(0,1.4fr) minmax(220px,.8fr)}.mainarea{padding:15px}.bottomgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.shell{min-height:0}}
@media(max-width:720px){.appbody{grid-template-columns:1fr}.sidebar{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:4px;padding:7px;border-right:0;border-bottom:1px solid var(--line)}.navitem{width:auto;min-height:48px;font-size:8px}.navitem .ico{font-size:16px}.navitem.active:before{left:8px;right:8px;top:auto;bottom:-7px;width:auto;height:2px}.nav-spacer{display:none}.workspace{grid-template-columns:1fr}.rightcol{display:grid;grid-template-columns:1fr}.mainarea{padding:12px}.sectionhead h2{font-size:18px}.preview{min-height:230px}.page-heading{margin-bottom:17px}.topbar{padding:0 12px}.top-right .status-text{display:none}.footer{flex-direction:column}.bottomgrid{gap:7px}.metric{padding:10px}.metricnum{font-size:21px}}

/* TTT AI hologram assistant */
.holo-launch{position:fixed;right:24px;bottom:24px;width:82px;height:92px;border:0;background:transparent;z-index:120;cursor:pointer;filter:drop-shadow(0 0 14px #48f3f0aa);transition:transform .25s}
.holo-launch:hover{transform:translateY(-5px) scale(1.04)}
.holo-orb{position:absolute;left:15px;top:2px;width:52px;height:52px;border-radius:50%;border:1px solid #8fffff;background:radial-gradient(circle at 35% 28%,#d8ffff 0,#70ffff 8%,#218d9c 25%,#102e43 58%,#081319 76%);box-shadow:inset 0 0 16px #a1ffffaa,0 0 18px #39f4f4aa,0 0 45px #36cde455;animation:holoFloat 3s ease-in-out infinite}
.holo-orb:before,.holo-orb:after{content:"";position:absolute;inset:-8px;border:1px solid #61f5f4a8;border-radius:50%;transform:rotateX(68deg);animation:holoRing 5s linear infinite}
.holo-orb:after{inset:-13px;border-color:#8b7dff99;transform:rotateY(68deg);animation-duration:7s;animation-direction:reverse}
.holo-beam{position:absolute;left:25px;top:55px;width:32px;height:21px;background:linear-gradient(180deg,#65ffff88,transparent);clip-path:polygon(25% 0,75% 0,100% 100%,0 100%);filter:blur(2px);opacity:.9}
.holo-base{position:absolute;left:12px;bottom:5px;width:58px;height:10px;border:1px solid #74ffff;background:radial-gradient(ellipse,#66ffff99,#173d4a 55%,transparent 75%);border-radius:50%;box-shadow:0 0 18px #38f3f4aa;animation:holoPulse 2s ease-in-out infinite}
.holo-label{position:absolute;left:-22px;right:-22px;bottom:-13px;color:#a9ffff;font-size:9px;font-weight:800;letter-spacing:.17em;text-shadow:0 0 9px #46ffff;text-align:center;white-space:nowrap}
.holo-panel{position:fixed;right:24px;bottom:125px;width:min(350px,calc(100vw - 28px));border:1px solid #54e9eea8;border-radius:17px;overflow:hidden;background:linear-gradient(145deg,#101f27f5,#0b1118f8);box-shadow:0 0 0 1px #5ffaff20,0 0 35px #29d9e52e,0 20px 70px #000b;z-index:121;backdrop-filter:blur(18px);transform-origin:bottom right;animation:holoPanelIn .25s ease-out}
.holo-panel[hidden]{display:none}.holo-head{display:flex;align-items:center;gap:10px;padding:13px 14px;border-bottom:1px solid #31545a;background:linear-gradient(90deg,#173239,#121a24)}.holo-mini{width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#d9ffff,#3ce8ed 18%,#173e57 65%);box-shadow:0 0 18px #42f4f4a8;animation:holoFloat 3s ease-in-out infinite}.holo-headtext{flex:1}.holo-headtext strong{display:block;font-size:12px;color:#d9ffff;letter-spacing:.04em}.holo-headtext small{font-size:10px;color:#83b7bd}.holo-close{border:1px solid #426268;border-radius:8px;background:#13262c;color:#b8ffff;padding:6px 9px}.holo-chat{padding:13px;max-height:260px;overflow:auto}.holo-message{font-size:11px;line-height:1.7;color:#d2e9ec;background:#122329;border:1px solid #2a5159;border-radius:10px;padding:10px 11px;white-space:pre-wrap;overflow-wrap:anywhere}.holo-message.user{margin:9px 0 9px 24px;background:#163438;border-color:#34777b}.holo-form{display:flex;gap:7px;padding:0 12px 12px}.holo-form input{flex:1;min-width:0;background:#0a141a;border:1px solid #31565d;border-radius:9px;color:#e7ffff;padding:10px;font-size:11px;outline:none}.holo-form input:focus{border-color:#62f4f2;box-shadow:0 0 0 2px #54f1f21b}.holo-form button{border:0;border-radius:9px;background:linear-gradient(110deg,#7cffff,#56cbd9);color:#07171b;font-weight:900;padding:0 13px}.holo-hint{padding:0 13px 12px;font-size:9px;line-height:1.5;color:#77999e}
@keyframes holoFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}@keyframes holoRing{to{transform:rotateX(68deg) rotateZ(360deg)}}@keyframes holoPulse{0%,100%{opacity:.6;transform:scaleX(.88)}50%{opacity:1;transform:scaleX(1.08)}}@keyframes holoPanelIn{from{opacity:0;transform:translateY(10px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
@media(max-width:600px){.holo-launch{right:13px;bottom:17px;transform:scale(.9);transform-origin:bottom right}.holo-panel{right:12px;bottom:105px;width:min(350px,calc(100vw - 24px))}}
@media(prefers-reduced-motion:reduce){.holo-orb,.holo-orb:before,.holo-orb:after,.holo-base,.holo-mini{animation:none}}

</style>
</head>
<body>
<div class="page">
  <header class="page-heading"><div class="eyebrow">TRÍ TUỆ NHÂN TẠO K26 VIP </div><h1><span style="color:#72ecec">TTT AI</span></h1><p>Tải ảnh lên · Nhận diện vật thể · Khám phá nội dung bằng AI</p></header>
  <section class="shell">
    <div class="topbar"><div class="brand"><div class="brand-mark">T</div><div>TTT AI<small>IMAGE INTELLIGENCE</small></div></div><div class="top-right"><span><i class="status-dot"></i><span class="status-text">Hệ thống phân tích ảnh</span></span><span>⌕</span><span>◉</span></div></div>
    <div class="appbody">
      <nav class="sidebar" aria-label="Điều hướng"><button class="navitem" type="button" title="Tổng quan"><span class="ico">▦</span><span>Tổng quan</span></button><button class="navitem" type="button" title="Dự án"><span class="ico">▱</span><span>Dự án</span></button><button class="navitem" type="button" title="Bộ dữ liệu"><span class="ico">◉</span><span>Dữ liệu</span></button><button class="navitem active" type="button" title="Phân tích ảnh"><span class="ico">◉</span><span>Phân tích</span></button><button class="navitem" type="button" title="Báo cáo" id="reportNav"><span class="ico">▤</span><span>Báo cáo</span></button><button class="navitem" type="button" title="Cài đặt" id="settingsNav"><span class="ico">⚙</span><span>Cài đặt</span></button><div class="nav-spacer"></div><button class="navitem" type="button" title="Trợ giúp" id="helpNav"><span class="ico">ⓘ</span><span>Trợ giúp</span></button></nav>
      <main class="mainarea">
        <div class="sectionhead"><div><h2>Phân tích hình ảnh</h2><p>Chọn ảnh để bắt đầu nhận diện và hỏi AI về nội dung ảnh.</p></div><div class="chip"><span class="status-dot"></span>SẴN SÀNG PHÂN TÍCH</div></div>
        <div class="workspace">
          <div class="leftcol">
            <section class="card"><div class="cardhead"><div><div class="cardtitle">01 / Ảnh đầu vào</div><div class="cardsub">Kéo thả ảnh vào khung hoặc chọn tệp từ thiết bị</div></div><div class="tiny">XEM TRƯỚC</div></div>
              <input type="file" id="fileInput" accept="image/*" hidden>
              <div style="display:flex;gap:8px;flex-wrap:wrap;padding:12px">
  <button id="cameraBtn" class="btn" type="button">📷 MỞ CAMERA</button>
  <button id="captureBtn" class="btn secondary" type="button" disabled>📸 CHỤP ẢNH</button>
  <button id="stopCameraBtn" class="btn secondary" type="button" disabled>TẮT CAMERA</button>
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;padding:0 12px 12px">
  <input id="targetObject" type="text" maxlength="80"
    placeholder="Nhập vật cần tìm, ví dụ: điện thoại, cái ly, người..."
    aria-label="Vật thể cần tìm"
    style="flex:1;min-width:220px;padding:11px 12px;border:1px solid #45666a;border-radius:8px;background:#0c1214;color:#e8f1f2">
  <button id="findTargetBtn" class="btn" type="button">🔎 TÌM & KHOANH TRÒN</button>
</div>
<div style="padding:0 13px 12px;color:#829397;font-size:10px;line-height:1.6">
  Nhập tên vật trước khi chụp để tự động khoanh tròn sau khi chụp. COCO-SSD hỗ trợ các loại vật thể đã được huấn luyện.
</div>

<video id="cameraVideo" autoplay playsinline muted
  style="display:none;width:100%;max-height:400px;object-fit:contain;background:#000">
</video>
              <div id="previewBox" class="preview"><div class="empty" id="emptyState"><div class="uploadico">⇧</div><h3>Tải ảnh lên để phân tích</h3><p>Hỗ trợ ảnh JPG, PNG, WEBP và các định dạng ảnh trình duyệt đọc được. Tệp tối đa <b>500 MB</b>.</p><button id="chooseBtn" class="btn" type="button" style="margin-top:16px">＋ &nbsp; CHỌN HÌNH ẢNH</button><div class="fineprint">Ảnh gốc được giữ trên thiết bị. Để phân tích bằng mô hình thị giác, hệ thống gửi bản ảnh đã thu nhỏ và nén.</div></div><img id="preview" class="hidden" alt="Ảnh xem trước"><canvas id="overlay" class="hidden"></canvas><div class="scanline"></div></div>
              <div class="filebar"><div id="fileInfo" class="fileinfo">Chưa chọn ảnh · Giới hạn 500 MB</div><button id="changeBtn" class="btn secondary hidden" type="button" style="padding:7px 9px;font-size:9px">Đổi ảnh</button></div>
              <div class="actions"><button id="detectBtn" class="btn" type="button" disabled>✦ &nbsp; PHÂN TÍCH TOÀN DIỆN</button><button id="boxBtn" class="btn secondary" type="button" disabled>⌗ Hiện / ẩn khung</button><button id="clearBtn" class="btn secondary" type="button" disabled>Xóa ảnh</button></div>
            </section>
            <div class="bottomgrid"><div class="metric"><div class="metrichead">Vật thể phát hiện <span>⌗</span></div><div class="metricnum" id="objectCount">—</div><div class="metricnote" id="objectNote">Chưa phân tích ảnh</div></div><div class="metric"><div class="metrichead">Nhóm đối tượng <span>◈</span></div><div class="metricnum" id="classCount">—</div><div class="metricnote">Số loại vật thể khác nhau</div></div><div class="metric"><div class="metrichead">Độ tin cậy cao nhất <span>⌁</span></div><div class="metricnum" id="topScore">—</div><div class="mini-bars"><span id="scoreBar"></span></div><div class="metricnote">Theo mô hình phát hiện vật thể</div></div><div class="metric"><div class="metrichead">AI thị giác <span>✦</span></div><div class="metricnum" id="visionState" style="font-size:15px">Sẵn sàng</div><div class="metricnote" id="visionNote">Mô tả ảnh và hỏi đáp cần API key</div></div></div>
          </div>
          <aside class="rightcol">
            <section class="card resultcard"><div class="cardhead"><div><div class="cardtitle">02 / Kết quả chi tiết</div><div class="cardsub">Vật thể và thông tin từ ảnh</div></div><div class="tiny">LIVE DATA</div></div><div class="detailbody">
              <div class="modelrow"><div class="modelicon">◎</div><div><div class="modelname">Bộ nhận diện vật thể</div><div class="modeldesc">COCO-SSD · chạy cục bộ trên trình duyệt</div></div><div class="modelstate" id="modelState">Đang tải…</div></div>
              <div class="detail-section"><div class="detailtitle">THÔNG TIN ẢNH <span id="imageStatus">Chờ ảnh</span></div><div class="kv"><span>Tên tệp</span><span id="metaName">—</span></div><div class="kv"><span>Kích thước</span><span id="metaSize">—</span></div><div class="kv"><span>Độ phân giải</span><span id="metaResolution">—</span></div><div class="kv"><span>Định dạng</span><span id="metaType">—</span></div></div>
              <div class="divider"></div><div class="detail-section"><div class="detailtitle">NHẬN DIỆN ĐỐI TƯỢNG <span id="resultCount">Chưa phân tích</span></div><div id="results" class="results"><div class="emptyresults">Chọn ảnh và nhấn <b>PHÂN TÍCH TOÀN DIỆN</b> để xem các vật thể mà mô hình phát hiện được.</div></div></div>
            </div></section>
            <section class="card"><div class="cardhead"><div><div class="cardtitle">03 / AI mô tả & hỏi đáp</div><div class="cardsub">Dùng mô hình thị giác để hiểu ảnh</div></div><div class="tiny">AI VISION</div></div><div class="detailbody"><div id="description" class="description">Sau khi chọn ảnh, nhấn “Phân tích toàn diện” để AI mô tả ảnh bằng tiếng Việt. Bạn cũng có thể hỏi câu hỏi riêng về ảnh.</div><form id="questionForm" class="questionbox"><input id="questionInput" maxlength="500" placeholder="Ví dụ: Đây là con gì?" autocomplete="off"><button id="askBtn" type="submit" title="Hỏi AI" disabled>➤</button></form><div class="fineprint" id="apiNote">Tính năng mô tả và hỏi ảnh cần GEMINI_API_KEY được cài trên máy chủ. Nếu chưa có khóa, nhận diện vật thể cục bộ vẫn dùng được.</div></div></section>
          </aside>
        </div>
        <div class="footer"><div><b style="color:#aabfc2">TTT AI · K26</b><br>Phòng phân tích hình ảnh bằng trí tuệ nhân tạo.</div><div>Không thể cam kết độ chính xác cố định cho mọi ảnh. COCO-SSD chỉ nhận diện các lớp đã được huấn luyện; mô hình thị giác có thể mô tả rộng hơn.</div></div>
      </main>
    </div>
  </section>
</div><div id="toast" class="toast" role="status" aria-live="polite"></div>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js"></script>
<script>
(()=>{
 const $=id=>document.getElementById(id);const input=$('fileInput'),previewBox=$('previewBox'),preview=$('preview'),overlay=$('overlay'),empty=$('emptyState'),detectBtn=$('detectBtn'),boxBtn=$('boxBtn'),clearBtn=$('clearBtn'),changeBtn=$('changeBtn'),chooseBtn=$('chooseBtn'),fileInfo=$('fileInfo'),modelState=$('modelState'),resultsBox=$('results'),description=$('description'),toast=$('toast');
 let model=null,file=null,objectUrl=null,preds=[],showBoxes=true,aiImageData=null,busy=false,toastTimer=null,autoFindAfterLoad=false,targetMode=false;
 const vn={'person':'Người','bicycle':'Xe đạp','car':'Ô tô','motorcycle':'Xe máy','airplane':'Máy bay','bus':'Xe buýt','train':'Tàu hỏa','truck':'Xe tải','boat':'Thuyền','traffic light':'Đèn giao thông','fire hydrant':'Trụ cứu hỏa','stop sign':'Biển báo dừng','parking meter':'Trụ đỗ xe','bench':'Ghế băng','bird':'Chim','cat':'Mèo','dog':'Chó','horse':'Ngựa','sheep':'Cừu','cow':'Bò','elephant':'Voi','bear':'Gấu','zebra':'Ngựa vằn','giraffe':'Hươu cao cổ','backpack':'Ba lô','umbrella':'Ô / dù','handbag':'Túi xách','tie':'Cà vạt','suitcase':'Va li','frisbee':'Đĩa ném','skis':'Ván trượt tuyết','snowboard':'Ván trượt tuyết','sports ball':'Bóng thể thao','kite':'Diều','baseball bat':'Gậy bóng chày','baseball glove':'Găng bóng chày','skateboard':'Ván trượt','surfboard':'Ván lướt sóng','tennis racket':'Vợt tennis','bottle':'Chai','wine glass':'Ly thủy tinh','cup':'Cốc','fork':'Nĩa','knife':'Dao','spoon':'Thìa','bowl':'Bát','banana':'Chuối','apple':'Táo','sandwich':'Bánh mì kẹp','orange':'Cam','broccoli':'Bông cải xanh','carrot':'Cà rốt','hot dog':'Xúc xích','pizza':'Pizza','donut':'Bánh donut','cake':'Bánh kem','chair':'Ghế','couch':'Ghế sofa','potted plant':'Chậu cây','bed':'Giường','dining table':'Bàn ăn','toilet':'Bồn cầu','tv':'TV','laptop':'Máy tính xách tay','mouse':'Chuột máy tính','remote':'Điều khiển từ xa','keyboard':'Bàn phím','cell phone':'Điện thoại','microwave':'Lò vi sóng','oven':'Lò nướng','toaster':'Máy nướng bánh mì','sink':'Bồn rửa','refrigerator':'Tủ lạnh','book':'Sách','clock':'Đồng hồ','vase':'Bình hoa','scissors':'Kéo','teddy bear':'Gấu bông','hair drier':'Máy sấy tóc','toothbrush':'Bàn chải đánh răng'};
 const icons={person:'♙',cat:'♧',dog:'♧',car:'▰',bicycle:'⚙','cell phone':'▯',laptop:'▣',book:'▤',bottle:'♜',chair:'▱',cup:'◡',clock:'◷',tv:'▣',keyboard:'⌨',mouse:'⌁',apple:'●',banana:'↗',bird:'♧'};
 function notify(s){toast.textContent=s;toast.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.classList.remove('show'),3600)}
 function setModel(s,color){modelState.textContent=s;modelState.style.color=color||'#ffd479'}
 function clearCanvas(){const c=overlay.getContext('2d');c.clearRect(0,0,overlay.width,overlay.height)}
 function resetAnalysis(){preds=[];aiImageData=null;targetMode=false;clearCanvas();$('objectCount').textContent='—';$('classCount').textContent='—';$('topScore').textContent='—';$('objectNote').textContent='Chưa phân tích ảnh';$('scoreBar').style.width='0';$('resultCount').textContent='Chưa phân tích';resultsBox.innerHTML='<div class="emptyresults">Ảnh đã sẵn sàng. Nhấn <b>PHÂN TÍCH TOÀN DIỆN</b> để bắt đầu.</div>';description.textContent='Ảnh đã chọn. Nhấn “Phân tích toàn diện” để AI mô tả ảnh bằng tiếng Việt.';$('visionState').textContent='Sẵn sàng';$('visionNote').textContent='Mô tả ảnh và hỏi đáp cần API key';$('askBtn').disabled=!file}
 function formatSize(bytes){return bytes>=1024*1024*1024?(bytes/1024/1024/1024).toFixed(2)+' GB':(bytes/1024/1024).toFixed(2)+' MB'}
 function chooseFile(f){if(!f)return;if(!f.type.startsWith('image/')){notify('Tệp này không phải ảnh. Vui lòng chọn tệp hình ảnh.');return}if(f.size>500*1024*1024){notify('Ảnh vượt quá giới hạn 500 MB. Vui lòng chọn tệp nhỏ hơn.');return}if(objectUrl)URL.revokeObjectURL(objectUrl);file=f;objectUrl=URL.createObjectURL(f);preview.onload=()=>{preview.classList.remove('hidden');empty.classList.add('hidden');previewBox.classList.add('has-image');overlay.classList.remove('hidden');$('metaResolution').textContent=preview.naturalWidth+' × '+preview.naturalHeight+' px';if(preds.length&&showBoxes){if(targetMode)drawTargetCircles(preds);else drawBoxes(preds);}if(autoFindAfterLoad){autoFindAfterLoad=false;setTimeout(()=>findTarget(),150);}};preview.onerror=()=>notify('Trình duyệt không mở được ảnh này. Hãy thử JPG hoặc PNG.');preview.src=objectUrl;fileInfo.textContent=f.name+' · '+formatSize(f.size);$('metaName').textContent=f.name;$('metaSize').textContent=formatSize(f.size);$('metaType').textContent=f.type||'Ảnh';$('imageStatus').textContent='Đã chọn';changeBtn.classList.remove('hidden');detectBtn.disabled=!model;boxBtn.disabled=false;clearBtn.disabled=false;$('askBtn').disabled=false;resetAnalysis();notify('Đã chọn ảnh. Sẵn sàng phân tích.');}
 chooseBtn.addEventListener('click',()=>input.click());changeBtn.addEventListener('click',()=>input.click());input.addEventListener('change',e=>{chooseFile(e.target.files[0]);input.value=''});['dragenter','dragover'].forEach(t=>previewBox.addEventListener(t,e=>{e.preventDefault();previewBox.classList.add('dragover')}));['dragleave','drop'].forEach(t=>previewBox.addEventListener(t,e=>{e.preventDefault();previewBox.classList.remove('dragover')}));previewBox.addEventListener('drop',e=>chooseFile(e.dataTransfer.files[0]));
 function drawBoxes(items){if(!preview.naturalWidth||!preview.clientWidth)return;const dpr=Math.min(window.devicePixelRatio||1,2),w=preview.clientWidth,h=preview.clientHeight;overlay.width=Math.max(1,Math.round(w*dpr));overlay.height=Math.max(1,Math.round(h*dpr));overlay.style.width='100%';overlay.style.height='100%';const ctx=overlay.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);if(!showBoxes)return;const scaleX=w/(preview.naturalWidth),scaleY=h/(preview.naturalHeight),font=Math.max(11,Math.min(15,w/45));ctx.lineWidth=2;ctx.font=`700 ${font}px Segoe UI,Arial`;items.forEach((p,i)=>{const [x0,y0,bw0,bh0]=p.bbox;const x=x0*scaleX,y=y0*scaleY,bw=bw0*scaleX,bh=bh0*scaleY;const color=i%3===0?'#5bf0f4':i%3===1?'#f27fd2':'#87f0b5';ctx.strokeStyle=color;ctx.shadowColor=color;ctx.shadowBlur=7;ctx.strokeRect(x,y,bw,bh);ctx.shadowBlur=0;const label=(vn[p.class]||p.class)+' '+Math.round(p.score*100)+'%';const tw=ctx.measureText(label).width+12,th=font+10,ly=Math.max(0,y-th);ctx.fillStyle=color;ctx.fillRect(x,ly,tw,th);ctx.fillStyle='#071517';ctx.fillText(label,x+6,ly+font+1);});}

 const targetInput=$('targetObject');
 const findTargetBtn=$('findTargetBtn');
 function normalizeSearch(value){return String(value||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').trim();}
 const targetAliases={
   'nguoi':'person','con nguoi':'person','people':'person',
   'dien thoai':'cell phone','dien thoai di dong':'cell phone','smartphone':'cell phone','phone':'cell phone',
   'cai ly':'cup','ly':'cup','coc':'cup','cai coc':'cup',
   'chai nuoc':'bottle','binh nuoc':'bottle','chai':'bottle',
   'xe may':'motorcycle','xe oto':'car','o to':'car','xe hoi':'car',
   'may tinh':'laptop','laptop':'laptop','may tinh xach tay':'laptop',
   'ban phim':'keyboard','chuot may tinh':'mouse','sach':'book',
   'cho':'dog','con cho':'dog','meo':'cat','con meo':'cat',
   'ghe':'chair','ghe sofa':'couch','ban':'dining table',
   'dong ho':'clock','ti vi':'tv','tivi':'tv','tv':'tv',
   'qua tao':'apple','tao':'apple','chuoi':'banana','cam':'orange',
   'xe dap':'bicycle','o du':'umbrella','du':'umbrella'
 };
 function drawTargetCircles(items){
   if(!preview.naturalWidth||!preview.naturalHeight)return;
   const dpr=Math.min(window.devicePixelRatio||1,2);
   const w=previewBox.clientWidth,h=previewBox.clientHeight;
   overlay.width=Math.max(1,Math.round(w*dpr));
   overlay.height=Math.max(1,Math.round(h*dpr));
   overlay.style.width='100%';overlay.style.height='100%';
   const ctx=overlay.getContext('2d');
   ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
   if(!showBoxes)return;
   const imageRect=preview.getBoundingClientRect();
   const boxRect=previewBox.getBoundingClientRect();
   const left=imageRect.left-boxRect.left,top=imageRect.top-boxRect.top;
   const scaleX=imageRect.width/preview.naturalWidth;
   const scaleY=imageRect.height/preview.naturalHeight;
   const font=Math.max(11,Math.min(15,w/45));
   ctx.lineWidth=3;ctx.font=`700 ${font}px Segoe UI,Arial`;
   items.forEach(p=>{
     const [x0,y0,bw0,bh0]=p.bbox;
     const x=left+x0*scaleX,y=top+y0*scaleY;
     const bw=bw0*scaleX,bh=bh0*scaleY;
     const cx=x+bw/2,cy=y+bh/2;
     ctx.beginPath();
     ctx.ellipse(cx,cy,Math.max(10,bw*.58),Math.max(10,bh*.58),0,0,Math.PI*2);
     ctx.strokeStyle='#ff4545';ctx.shadowColor='#ff3030';ctx.shadowBlur=10;ctx.stroke();ctx.shadowBlur=0;
     const label=(vn[p.class]||p.class)+' '+Math.round(p.score*100)+'%';
     const tw=ctx.measureText(label).width+12,th=font+10;
     const lx=Math.max(0,Math.min(w-tw,cx-tw/2));
     const ly=Math.max(0,cy-Math.max(10,bh*.58)-th-3);
     ctx.fillStyle='#ff4545';ctx.fillRect(lx,ly,tw,th);
     ctx.fillStyle='#fff';ctx.fillText(label,lx+6,ly+font+1);
   });
 }
 async function findTarget(){
   const raw=targetInput.value.trim();
   if(!raw){notify('Hãy nhập tên vật cần tìm trước khi chụp ảnh.');return;}
   if(!file||!preview.naturalWidth){notify('Hãy chụp ảnh hoặc chọn ảnh trước.');return;}
   if(!model){notify('COCO-SSD chưa sẵn sàng. Hãy chờ mô hình tải xong.');return;}
   if(busy){notify('AI đang xử lý, hãy đợi một chút.');return;}
   const query=normalizeSearch(raw);
   const wanted=targetAliases[query]||query;
   const oldText=findTargetBtn.textContent;
   findTargetBtn.disabled=true;findTargetBtn.textContent='ĐANG TÌM…';
   try{
     const ratio=Math.min(1,1024/Math.max(preview.naturalWidth,preview.naturalHeight));
     const canvas=document.createElement('canvas');
     canvas.width=Math.max(1,Math.round(preview.naturalWidth*ratio));
     canvas.height=Math.max(1,Math.round(preview.naturalHeight*ratio));
     canvas.getContext('2d').drawImage(preview,0,0,canvas.width,canvas.height);
     const detected=await model.detect(canvas,30,.35);
     const matches=detected.filter(p=>{
       const english=normalizeSearch(p.class);
       const vietnamese=normalizeSearch(vn[p.class]||'');
       return english===wanted||vietnamese===query;
     }).map(p=>({...p,bbox:p.bbox.map(v=>v/ratio)}));
     matches.sort((a,b)=>b.score-a.score);
     preds=matches;showBoxes=true;targetMode=true;
     boxBtn.disabled=false;boxBtn.textContent='⌗ Ẩn / hiện khoanh tròn';
     drawTargetCircles(preds);renderResults(preds);
     if(matches.length){
       description.textContent=`Đã tìm thấy ${matches.length} vật thể phù hợp với yêu cầu “${raw}”. Các vòng tròn màu đỏ đánh dấu vị trí được COCO-SSD nhận diện.`;
       setModel('Đã tìm thấy','#7cf0b6');
       notify(`Đã khoanh tròn ${matches.length} vật thể phù hợp.`);
     }else{
       description.textContent=`Không tìm thấy “${raw}” trong các lớp vật thể mà COCO-SSD hỗ trợ. Thử tên như người, điện thoại, cái ly, chai, xe máy, chó hoặc mèo.`;
       setModel('Không tìm thấy','#ffd479');
       notify('Không tìm thấy vật phù hợp. Thử tên vật thể khác nhé.');
     }
   }catch(error){
     console.error(error);notify('Không tìm được vật thể: '+(error.message||'Hãy thử lại.'));
   }finally{
     findTargetBtn.disabled=false;findTargetBtn.textContent=oldText;
   }
 }
 findTargetBtn.addEventListener('click',findTarget);
 targetInput.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();findTarget();}});

let cameraStream = null;

const cameraBtn = document.getElementById('cameraBtn');
const captureBtn = document.getElementById('captureBtn');
const stopCameraBtn = document.getElementById('stopCameraBtn');
const cameraVideo = document.getElementById('cameraVideo');

cameraBtn.addEventListener('click', async () => {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' },
            audio: false
        });

        cameraVideo.srcObject = cameraStream;
        cameraVideo.style.display = 'block';
        await cameraVideo.play();

        captureBtn.disabled = false;
        stopCameraBtn.disabled = false;
        notify('Camera đã mở!');
    } catch (error) {
        notify('Không mở được camera. Hãy kiểm tra quyền camera.');
    }
});

captureBtn.addEventListener('click', () => {
    if (!cameraVideo.videoWidth) {
        notify('Camera chưa sẵn sàng. Hãy đợi một chút.');
        return;
    }

    const canvas = document.createElement('canvas');
    canvas.width = cameraVideo.videoWidth;
    canvas.height = cameraVideo.videoHeight;
    canvas.getContext('2d').drawImage(
        cameraVideo, 0, 0, canvas.width, canvas.height
    );

    canvas.toBlob(blob => {
        if (!blob) {
            notify('Không chụp được ảnh.');
            return;
        }

        autoFindAfterLoad = Boolean(targetInput.value.trim());
        chooseFile(new File(
            [blob],
            'anh-camera.jpg',
            { type: 'image/jpeg' }
        ));

        stopCamera();
    }, 'image/jpeg', 0.92);
});

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }

    cameraVideo.srcObject = null;
    cameraVideo.style.display = 'none';
    captureBtn.disabled = true;
    stopCameraBtn.disabled = true;
}

stopCameraBtn.addEventListener('click', stopCamera);
 window.addEventListener('resize',()=>{if(preds.length){if(targetMode)drawTargetCircles(preds);else drawBoxes(preds)}});
 function renderResults(items){$('objectCount').textContent=items.length;$('classCount').textContent=new Set(items.map(p=>p.class)).size;$('topScore').textContent=items.length?Math.round(items[0].score*100)+'%':'0%';$('scoreBar').style.width=(items.length?Math.round(items[0].score*100):0)+'%';$('objectNote').textContent=items.length?'Đã phát hiện trong ảnh':'Không phát hiện vật thể rõ';$('resultCount').textContent=items.length+' kết quả';if(!items.length){resultsBox.innerHTML='<div class="emptyresults">Chưa phát hiện vật thể thuộc nhóm mà mô hình hỗ trợ. Hãy thử ảnh rõ hơn; AI mô tả vẫn có thể nhận ra nội dung khác.</div>';return}resultsBox.innerHTML='';items.forEach(p=>{const el=document.createElement('div');el.className='resultitem';const top=document.createElement('div');top.className='resulttop';const ico=document.createElement('div');ico.className='resulticon';ico.textContent=icons[p.class]||'✧';const name=document.createElement('div');name.className='resultname';name.textContent=vn[p.class]||p.class;const score=document.createElement('div');score.className='percent';score.textContent=Math.round(p.score*100)+'%';top.append(ico,name,score);const bar=document.createElement('div');bar.className='bar';const fill=document.createElement('div');fill.className='barfill';fill.style.width=Math.round(p.score*100)+'%';bar.append(fill);el.append(top,bar);resultsBox.append(el)})}
 async function loadModel(){try{if(!window.tf||!window.cocoSsd)throw Error('Thiếu thư viện AI');setModel('Đang tải mô hình…');model=await cocoSsd.load({base:'lite_mobilenet_v2'});setModel('SẴN SÀNG','#7cf0b6');$('visionState').textContent='Sẵn sàng';if(file)detectBtn.disabled=false}catch(e){console.error(e);setModel('Không tải được','#ff9dbb');$('visionState').textContent='Chưa tải';$('visionNote').textContent='Kiểm tra kết nối Internet và tải lại trang'} }
 async function compressImage(){if(aiImageData)return aiImageData;if(!preview.naturalWidth)throw Error('Trình duyệt chưa đọc xong ảnh.');const maxSide=1600,ratio=Math.min(1,maxSide/Math.max(preview.naturalWidth,preview.naturalHeight));let canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(preview.naturalWidth*ratio));canvas.height=Math.max(1,Math.round(preview.naturalHeight*ratio));const ctx=canvas.getContext('2d',{alpha:false});ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(preview,0,0,canvas.width,canvas.height);let blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',.84));while(blob&&blob.size>5*1024*1024&&Math.max(canvas.width,canvas.height)>640){const down=.75,nw=Math.max(1,Math.round(canvas.width*down)),nh=Math.max(1,Math.round(canvas.height*down));const c2=document.createElement('canvas');c2.width=nw;c2.height=nh;c2.getContext('2d',{alpha:false}).drawImage(canvas,0,0,nw,nh);canvas=c2;blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',.78));}if(!blob)throw Error('Không thể nén ảnh này trên trình duyệt.');if(blob.size>6*1024*1024)throw Error('Ảnh sau nén vẫn quá lớn. Hãy chọn ảnh nhỏ hơn hoặc giảm độ phân giải.');aiImageData=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=()=>reject(Error('Không đọc được ảnh sau nén.'));r.readAsDataURL(blob)});return aiImageData}
 async function askVision(question){if(!file)throw Error('Bạn cần chọn ảnh trước.');const dataUrl=await compressImage();const response=await fetch('/analyze-image',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:dataUrl,question})});let data={};try{data=await response.json()}catch(_){}if(!response.ok)throw Error(data.error||'Không phân tích được ảnh.');return data.reply}
 window.tttAskVision=askVision;
 async function runAll(question='Hãy mô tả chi tiết nội dung ảnh bằng tiếng Việt. Nêu các đối tượng chính, đặc điểm nhìn thấy, bối cảnh và điều gì chưa thể xác định chắc chắn.'){if(!file||busy)return;targetMode=false;busy=true;detectBtn.disabled=true;$('askBtn').disabled=true;previewBox.classList.add('scanning');detectBtn.innerHTML='◌ ĐANG PHÂN TÍCH…';$('visionState').textContent='Đang chạy';try{if(model){const ratio=Math.min(1,1024/Math.max(preview.naturalWidth,preview.naturalHeight)),canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(preview.naturalWidth*ratio));canvas.height=Math.max(1,Math.round(preview.naturalHeight*ratio));canvas.getContext('2d').drawImage(preview,0,0,canvas.width,canvas.height);preds=await model.detect(canvas,30,.40);preds.sort((a,b)=>b.score-a.score);preds=preds.map(p=>({...p,bbox:[p.bbox[0]/ratio,p.bbox[1]/ratio,p.bbox[2]/ratio,p.bbox[3]/ratio]}));drawBoxes(preds);renderResults(preds)}else{notify('Mô hình khoanh vùng chưa sẵn sàng; thử tải lại trang.')}description.textContent='Đang tạo bản ảnh tối ưu và gửi yêu cầu tới AI thị giác…';$('visionState').textContent='Đang gọi AI';$('visionNote').textContent='Đang xử lý';try{const reply=await askVision(question);description.textContent=reply;$('visionState').textContent='Hoàn tất';$('visionNote').textContent='Đã nhận phản hồi từ AI';$('apiNote').textContent='Kết quả do mô hình AI tạo ra có thể sai; hãy kiểm tra lại những thông tin quan trọng.';notify('Đã hoàn thành phân tích ảnh.')}catch(err){description.textContent=err.message;$('visionState').textContent='Cần kiểm tra';$('visionNote').textContent='Không hoàn tất mô tả AI';notify(err.message)}}catch(err){console.error(err);notify('Lỗi khi nhận diện vật thể: '+(err.message||'Vui lòng thử lại.'))}finally{busy=false;previewBox.classList.remove('scanning');detectBtn.disabled=!file||!model;detectBtn.innerHTML='✦ &nbsp; PHÂN TÍCH TOÀN DIỆN';$('askBtn').disabled=!file;}}
 detectBtn.addEventListener('click',()=>runAll());boxBtn.addEventListener('click',()=>{showBoxes=!showBoxes;if(targetMode)drawTargetCircles(preds);else drawBoxes(preds);boxBtn.textContent=showBoxes?(targetMode?'⌗ Ẩn / hiện khoanh tròn':'⌗ Ẩn / hiện khung'):(targetMode?'⌗ Hiện khoanh tròn':'⌗ Hiện khung')});$('questionForm').addEventListener('submit',async e=>{e.preventDefault();const q=$('questionInput').value.trim();if(!q||!file||busy)return;busy=true;$('askBtn').disabled=true;description.textContent='Đang hỏi AI về ảnh…';try{const a=await askVision(q);description.textContent=a;notify('AI đã trả lời câu hỏi.')}catch(err){description.textContent=err.message;notify(err.message)}finally{busy=false;$('askBtn').disabled=!file}});
 clearBtn.addEventListener('click',()=>{if(objectUrl)URL.revokeObjectURL(objectUrl);objectUrl=null;file=null;preds=[];aiImageData=null;targetMode=false;autoFindAfterLoad=false;preview.removeAttribute('src');preview.classList.add('hidden');overlay.classList.add('hidden');empty.classList.remove('hidden');previewBox.classList.remove('has-image','scanning');fileInfo.textContent='Chưa chọn ảnh · Giới hạn 500 MB';changeBtn.classList.add('hidden');detectBtn.disabled=true;boxBtn.disabled=true;clearBtn.disabled=true;$('askBtn').disabled=true;$('metaName').textContent='—';$('metaSize').textContent='—';$('metaResolution').textContent='—';$('metaType').textContent='—';$('imageStatus').textContent='Chờ ảnh';resetAnalysis()});
 $('reportNav').addEventListener('click',()=>{if(!file){notify('Hãy chọn và phân tích ảnh trước.');return}const text='BÁO CÁO PHÂN TÍCH ẢNH — TTT AI\nTệp: '+file.name+'\nKích thước: '+formatSize(file.size)+'\nĐộ phân giải: '+preview.naturalWidth+' x '+preview.naturalHeight+'\nSố vật thể: '+preds.length+'\n\nMÔ TẢ AI:\n'+description.textContent+'\n\nVẬT THỂ:\n'+preds.map(p=>(vn[p.class]||p.class)+' — '+Math.round(p.score*100)+'%').join('\n');const b=new Blob([text],{type:'text/plain;charset=utf-8'}),url=URL.createObjectURL(b),a=document.createElement('a');a.href=url;a.download='bao-cao-ttt-ai.txt';a.click();URL.revokeObjectURL(url);notify('Đã tạo báo cáo dạng TXT.')});$('settingsNav').addEventListener('click',()=>notify('Cấu hình API key trong Environment của máy chủ, không đặt khóa bí mật trong mã giao diện.'));$('helpNav').addEventListener('click',()=>notify('Chọn ảnh → Phân tích toàn diện → nhập câu hỏi riêng về ảnh nếu cần.'));
 loadModel();
})();
</script>

<div class="holo-panel" id="holoPanel" hidden role="dialog" aria-label="Trợ lý ảo TTT AI">
  <div class="holo-head"><div class="holo-mini" aria-hidden="true"></div><div class="holo-headtext"><strong>TTT AI · TRỢ LÝ ẢO</strong><small>Hologram thị giác · Sẵn sàng hỗ trợ</small></div><button class="holo-close" id="holoClose" aria-label="Đóng trợ lý">✕</button></div>
  <div class="holo-chat" id="holoChat"><div class="holo-message">Xin chào! ✨ Mình là trợ lý ảo TTT AI. Hãy tải ảnh lên khu vực phân tích, sau đó hỏi mình về nội dung ảnh nhé.</div></div>
  <form class="holo-form" id="holoForm"><input id="holoInput" maxlength="500" placeholder="Hỏi về ảnh đang chọn…" autocomplete="off"><button id="holoSend" type="submit">GỬI</button></form>
  <div class="holo-hint">Câu trả lời cần có ảnh đã chọn. AI có thể nhầm; hãy kiểm tra thông tin quan trọng.</div>
</div>
<button class="holo-launch" id="holoLaunch" aria-label="Mở trợ lý ảo TTT AI" aria-expanded="false"><span class="holo-orb"></span><span class="holo-beam"></span><span class="holo-base"></span><span class="holo-label">✦ TTT AI</span></button>
<script>
(()=>{const panel=document.getElementById('holoPanel'),launch=document.getElementById('holoLaunch'),close=document.getElementById('holoClose'),form=document.getElementById('holoForm'),input=document.getElementById('holoInput'),chat=document.getElementById('holoChat'),send=document.getElementById('holoSend');
function toggle(open){panel.hidden=!open;launch.setAttribute('aria-expanded',String(open));if(open)input.focus()}
function message(text,who='ai'){const el=document.createElement('div');el.className='holo-message'+(who==='user'?' user':'');el.textContent=text;chat.appendChild(el);chat.scrollTop=chat.scrollHeight;return el}
launch.addEventListener('click',()=>toggle(panel.hidden));close.addEventListener('click',()=>toggle(false));
form.addEventListener('submit', async e => {
    e.preventDefault();

    const q = input.value.trim();
    if (!q) return;

    input.value = '';
    message(q, 'user');

    const el = document.createElement('div');
    el.className = 'holo-message';
    el.textContent = 'AI đang suy nghĩ...';
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;

    send.disabled = true;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                messages: [{role: 'user', content: q}]
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Không gọi được AI.');
        }

        el.textContent = data.reply || 'AI chưa có câu trả lời.';
    } catch (err) {
        el.textContent = 'Lỗi: ' + err.message;
    } finally {
        send.disabled = false;
        input.focus();
        chat.scrollTop = chat.scrollHeight;
    }
});})();
</script>

</body></html>
"""

@app.route("/")
@app.route("/vision")
def vision_ai_page():
    return render_template_string(VISION_HTML)

@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    """Gửi ảnh và câu hỏi tới Gemini Vision; key không được gửi từ trình duyệt."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify(error="Chưa cấu hình GEMINI_API_KEY trong Render > Environment. COCO-SSD vẫn có thể nhận diện vật thể."), 503

    data = request.get_json(silent=True) or {}
    image = data.get("image")
    question = data.get("question", "Hãy mô tả chi tiết nội dung ảnh bằng tiếng Việt.")

    if not isinstance(image, str) or not image.startswith("data:image/") or "," not in image:
        return jsonify(error="Dữ liệu ảnh không hợp lệ. Hãy chọn ảnh và thử lại."), 400
    if len(image) > 8 * 1024 * 1024:
        return jsonify(error="Ảnh sau nén vẫn quá lớn. Hãy thử ảnh khác."), 413
    if not isinstance(question, str):
        question = "Hãy mô tả chi tiết nội dung ảnh bằng tiếng Việt."
    question = question[:1000]

    try:
        header, encoded = image.split(",", 1)
        mime_type = header[5:].split(";", 1)[0]
        if mime_type not in ("image/jpeg", "image/png", "image/webp", "image/gif"):
            mime_type = "image/jpeg"

        payload = {
            "systemInstruction": {
                "parts": [{
                    "text": (
                        "Bạn là TTT AI, trợ lý thị giác máy tính. Luôn trả lời bằng tiếng Việt tự nhiên. "
                        "Chỉ nêu chi tiết có thể suy ra hợp lý từ ảnh; không khẳng định chắc chắn điều không nhìn thấy. "
                        "Nếu không chắc, hãy nói rõ mức độ không chắc chắn. Không tự bịa độ chính xác phần trăm."
                    )
                }]
            },
            "contents": [{
                "role": "user",
                "parts": [
                    {"text": question},
                    {"inlineData": {"mimeType": mime_type, "data": encoded}}
                ]
            }],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1200}
        }

        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": api_key
            },
            json=payload,
            timeout=90
        )
        if response.status_code >= 400:
            app.logger.error("Gemini vision lỗi HTTP %s: %s", response.status_code, response.text[:1500])
            if response.status_code in (401, 403):
                return jsonify(error="Gemini từ chối API key. Hãy kiểm tra GEMINI_API_KEY trong Render."), 502
            if response.status_code == 429:
                return jsonify(error="Gemini đang hết hạn mức hoặc gửi quá nhanh. Hãy thử lại sau."), 429
            return jsonify(error="Gemini chưa phân tích được ảnh. Hãy kiểm tra nhật ký Render rồi thử lại."), 502

        result = response.json()
        parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        reply = "\n".join(part.get("text", "") for part in parts if isinstance(part, dict))
        return jsonify(reply=reply.strip() or "Gemini chưa tạo được câu trả lời cho ảnh này.")

    except requests.exceptions.Timeout:
        return jsonify(error="Gemini xử lý ảnh quá lâu. Hãy thử ảnh nhỏ hơn."), 504
    except requests.exceptions.RequestException:
        app.logger.exception("Lỗi khi phân tích ảnh bằng Gemini")
        return jsonify(error="Không kết nối được Gemini. Hãy thử lại sau."), 502
    except (ValueError, IndexError, KeyError, TypeError):
        app.logger.exception("Phản hồi Gemini không hợp lệ")
        return jsonify(error="Phản hồi từ Gemini không đúng định dạng. Hãy thử lại."), 502

if __name__ == "__main__":
    app.run(debug=False)
