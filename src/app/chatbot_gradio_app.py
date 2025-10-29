# KMS_lib — Smart FAQ Assistant (approved UI)
import gradio as gr
from src.app.config import FAQ_PATH, EMBEDDING_MODEL, HF_FALLBACK_MODEL, TOP_K, UI
from src.engines.faq_engine import FAQEngine
from src.engines.llm_router import LLMRouter

# ---------- engines ----------
faq = FAQEngine(FAQ_PATH, EMBEDDING_MODEL)
router = LLMRouter(hf_model=HF_FALLBACK_MODEL)

def respond(user_text: str):
    if not user_text or not user_text.strip():
        return "Please enter a question.", "[]"
    reformulated = router.reformulate(user_text.strip())
    answer, score, debug = faq.answer(reformulated, k=TOP_K)
    out = (
        f"**Reformulated**: {reformulated}\n\n"
        f"**Answer**: {answer}\n\n"
        f"**Confidence**: {score:.2f}"
    )
    return out, str(debug)

# ---------- styles (brown & ash, warm gradient) ----------
CUSTOM_CSS = """
:root{
  --kms-brown:#5a3e2b;
  --kms-ash:#f5f5f5;
  --kms-gold:#c49a6c;
}
body, .gradio-container { background: linear-gradient(135deg,#faf7f4 0%,#efe8e3 35%,#ece8ff 100%) !important; }
.kms-header {
  background:#fff; border:1px solid #eee; border-radius:18px; padding:14px 18px;
  box-shadow:0 8px 22px rgba(0,0,0,.06);
}
.kms-title { color:var(--kms-brown); font-weight:800; font-size:22px; letter-spacing:.2px; }
.kms-sub   { color:#6b6b6b; margin-top:4px; }
.kms-ask-card { background:#fff7e9; border:1px solid #f1e1c9; border-radius:16px; padding:12px; }
.kms-button-primary button{
  background: linear-gradient(90deg,#8a5a3e 0%, #5a3e2b 100%) !important; color:#fff !important;
  border:none !important; border-radius:12px !important; padding:10px 18px !important; font-weight:700 !important;
}
.kms-chip button{
  background:#fff; border:1px solid #eee; border-radius:999px; padding:6px 12px;
  box-shadow:0 2px 6px rgba(0,0,0,.06);
}
.kms-answer { background:#eafff0; border-radius:8px; padding:8px 10px; }
"""

theme = gr.themes.Soft()

with gr.Blocks(css=CUSTOM_CSS, theme=theme, title=UI.get("title","KMS_lib — Smart FAQ Assistant")) as demo:
    # Header
    with gr.Row(elem_classes=["kms-header"]):
        with gr.Column(scale=8):
            gr.HTML('<div class="kms-title">🤖 KMS_lib — Smart FAQ Assistant</div>')
            gr.HTML('<div class="kms-sub">Ask about reports, templates, or access issues — I’ll find your answer.</div>')
        with gr.Column(scale=4):
            ask_btn = gr.Button("🤖 Ask Assistant", elem_classes=["kms-button-primary"])

    # Ask panel
    with gr.Row():
        with gr.Column(scale=8, elem_classes=["kms-ask-card"]):
            inp = gr.Textbox(
                label="✍️ Ask",
                placeholder="e.g., How can I reserve a book?",
                lines=3
            )
            with gr.Row():
                b1 = gr.Button("📌 Reserve a book", elem_classes=["kms-chip"])
                b2 = gr.Button("📄 Template", elem_classes=["kms-chip"])
                b3 = gr.Button("🔒 Access denied", elem_classes=["kms-chip"])
                b4 = gr.Button("📝 Format guide", elem_classes=["kms-chip"])
        with gr.Column(scale=4):
            gr.Markdown(" ")

    # Answer panel
    gr.Markdown("📚 **Answer**", elem_classes=["kms-answer"])
    out = gr.Markdown()
    dbg = gr.Textbox(label="Debug (top matches)", lines=6, visible=True)

    # ---- presets (helpers) ----
    def preset_reserve(): return "How can I reserve a book?"
    def preset_template(): return "Where is the final-year report template?"
    def preset_access():  return "Why is my access denied and how do I fix it?"
    def preset_format():  return "What is the correct formatting guide to use?"

    # ---- events ----
    ask_btn.click(respond, inputs=[inp], outputs=[out, dbg])
    inp.submit(respond, inputs=[inp], outputs=[out, dbg])

    # preset buttons set the textbox value directly (compatible with Gradio 4.44.0)
    b1.click(preset_reserve, inputs=None, outputs=inp)
    b2.click(preset_template, inputs=None, outputs=inp)
    b3.click(preset_access,  inputs=None, outputs=inp)
    b4.click(preset_format,  inputs=None, outputs=inp)

if __name__ == "__main__":
    demo.launch(
        share=bool(UI.get("enable_share", False)),
        server_name=UI.get("server_name","127.0.0.1"),
        server_port=int(UI.get("server_port",7860)),
    )
