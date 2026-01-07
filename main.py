from flask import Flask, request, jsonify, render_template
import PyPDF2
import os
from google import genai

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyBQrp9jakN40JJYPDA5dEO4rix7QFYHpQk")


def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
    return extracted_text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("message")

        if not prompt:
            return jsonify({"error": "Message is required"}), 400

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=1000)