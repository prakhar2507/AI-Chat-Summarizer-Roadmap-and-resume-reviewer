from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from typing import List, Union
from dotenv import load_dotenv
import os
import groq
import json
import fitz

app=FastAPI()

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- Chat Extractor ----------

def chat_extractor(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content

# ---------- Chat Summarizer Function ----------

def chat_summarizer(chat: List[str]) -> dict:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional assistant that summarizes mentor-mentee conversations.\n\n"
                    "Your response MUST follow this **strict JSON format**:\n\n"
                    "{\n"
                    "  \"result\": {\n"
                    "    \"summary\": \"<Concise paragraph (100–150 words) summarizing the conversation, decisions made, and guidance given>\",\n"
                    "    \"key_takeaways\": [\n"
                    "      \"<Bullet point 1>\",\n"
                    "      \"<Bullet point 2>\",\n"
                    "      \"... up to 8 points\"\n"
                    "    ]\n"
                    "  }\n"
                    "}\n\n"
                    "Do NOT include any other keys like 'summary' above 'result'.\n"
                    "Do NOT wrap your output in markdown or code blocks.\n"
                    "Make sure all output is valid JSON.\n"
                    "Use fluent English. Keep it professional and clear."
                )
            },
            {
                "role": "user",
                "content": f"Summarize this chat: {chat}"
            }
        ],
        model="llama3-70b-8192"
    )

    response_text = chat_completion.choices[0].message.content.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()
    elif response_text.startswith("```"):
        response_text = response_text.replace("```", "").strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON received from LLM",
            "exception": str(e),
            "raw_output": response_text
        }

# ---------- Generate RoadMap Function ----------

def generate_career_roadmap(level: str, question: str) -> dict:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a highly knowledgeable career mentor for students. Your task is to create detailed, realistic, and up-to-date roadmaps based on the latest industry practices and hiring trends. Tailor the roadmap according to the student's current level.\n\n"
                    
                    "Output must be returned in strict JSON format like:\n\n"
                    "{\n"
                    "  \"overview\": [\"task1\", \"task2\", \"task3\"],\n"
                    "  \"description\": {\n"
                    "    \"task1\": {\n"
                    "      \"subtask_1\": \"<What to do>\",\n"
                    "      \"subtask_2\": \"<How to validate it>\",\n"
                    "      \"subtask_3\": \"<Optional extras for depth or edge>\"\n"
                    "    },\n"
                    "    \"task2\": {\n"
                    "      ...\n"
                    "    }\n"
                    "  }\n"
                    "}\n\n"

                    "Rules:\n"
                    "- 'overview' must be a list of task names in order.\n"
                    "- Use current industry technologies (e.g., GitHub, LeetCode, Kaggle, cloud platforms).\n"
                    "- No motivational fluff.\n"
                    "- All output must be valid JSON only.\n"
                    "- Do NOT include markdown, code blocks, or extra text.\n"
                    "- Do NOT include any keys other than 'overview' and 'description'."
                    "- Be consistent in your responses."
                )
            },
            {
                "role": "user",
                "content": f"I am at {level}. Provide me a roadmap {question}."
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct"
    )

    response_text = chat_completion.choices[0].message.content.strip()
    print(response_text)

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()
    elif response_text.startswith("```"):
        response_text = response_text.replace("```", "").strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON received from LLM",
            "exception": str(e),
            "raw_output": response_text
        }
        
# ---------- Resume Text Extractor ----------
def text_extractor_from_resume(file_bytes: bytes) -> str:
    doc = fitz.open("pdf", file_bytes)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

# ---------- Resume Reviewer ----------
def resume_reviewer(content: str) -> dict:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional resume reviewer and ATS optimization expert.\n\n"
                    "Your task is to analyze a resume and return structured feedback based on the following:\n\n"
                    "1. Rate the resume on 5 parameters (scale of 1 to 10):\n"
                    "   - length\n"
                    "   - clarity\n"
                    "   - relevance\n"
                    "   - accuracy\n"
                    "   - consistency\n\n"
                    "2. Provide an ATS score (scale of 1 to 10) — this reflects how well the resume will perform in an ATS system.\n\n"
                    "3. Give detailed feedback for each of the 5 parameters, clearly explaining what’s strong or weak.\n\n"
                    "4. Suggest specific, actionable improvements to increase the ATS score to 9 or 10.\n\n"
                    "5. Rewrite and return the improved version of the resume incorporating your suggestions.\n\n"
                    "**Output format must be strictly JSON**:\n\n"
                    "{\n"
                    "  \"ratings\": {\n"
                    "    \"length\": <1-10>,\n"
                    "    \"clarity\": <1-10>,\n"
                    "    \"relevance\": <1-10>,\n"
                    "    \"accuracy\": <1-10>,\n"
                    "    \"consistency\": <1-10>\n"
                    "  },\n"
                    "  \"ats_score\": <1-10>,\n"
                    "  \"feedback\": {\n"
                    "    \"length\": \"...\",\n"
                    "    \"clarity\": \"...\",\n"
                    "    \"relevance\": \"...\",\n"
                    "    \"accuracy\": \"...\",\n"
                    "    \"consistency\": \"...\"\n"
                    "  },\n"
                    "  \"improvement_suggestions\": [\n"
                    "    \"<Suggestion 1>\",\n"
                    "    \"<Suggestion 2>\",\n"
                    "    \"...\"\n"
                    "  ],\n"
                    "  \"improved_resume\": \"<Improved resume text here>\"\n"
                    "}\n\n"
                    "Rules:\n"
                    "- Do NOT return markdown or code block formatting.\n"
                    "- Output must be valid JSON.\n"
                    "- Be consistent across different resumes.\n"
                    "- Never fabricate data. Only improve what's provided."
                    "- Do NOT include unescaped line breaks in strings\n"
                )
            },
            {
                "role": "user",
                "content": f"Resume: {content}"
            }
        ],
        model="llama3-70b-8192"
    )

    response_text = chat_completion.choices[0].message.content.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()
    elif response_text.startswith("```"):
        response_text = response_text.replace("```", "").strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON received from LLM",
            "exception": str(e),
            "raw_output": response_text
        }

# ---------- Endpoints ----------

# ---------- Summarizer ----------

@app.post("/summarize")
async def summarize_chat_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported.")
    
    temp_file_path = f"/tmp/temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        chat = chat_extractor(temp_file_path)
        summary = chat_summarizer(chat)

        return summary
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# ---------- Career Roadmap ----------

@app.get("/career-roadmap")
async def career_roadmap_endpoint(level: str = Query(...), question: str = Query(...)):
    result = generate_career_roadmap(level, question)
    return result

# ---------- Resume Reviewer ----------

@app.post("/resume-reviewer")
async def resume_reviewer_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported.")

    file_bytes = await file.read()
    extracted_text = text_extractor_from_resume(file_bytes)

    if not extracted_text:
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF.")

    result = resume_reviewer(extracted_text)
    return result

@app.get("/")
def read_root():
    return {"response": "KYA KAR RAHA HAI BE SAHI ENDPOINT SE REQUEST BHEJ"}
