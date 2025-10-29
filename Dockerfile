# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Metadata ----------
LABEL maintainer="KMS_lib Contributors"
LABEL description="Lightweight NLP-based Knowledge Management System for digital libraries."

# ---------- Environment ----------
WORKDIR /app
COPY . /app

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update &&     apt-get install -y git &&     pip install --upgrade pip &&     pip install -r requirements.txt &&     python -m spacy download en_core_web_sm &&     rm -rf /var/lib/apt/lists/*

EXPOSE 7860

# ---------- Run ----------
CMD ["python", "src/app/chatbot_gradio_app.py"]
