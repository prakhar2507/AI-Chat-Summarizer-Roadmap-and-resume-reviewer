# AI-Chat-Summarizer-Roadmap-and-resume-reviewer
This API project is a comprehensive toolkit for students and professionals to enhance their career development through automated document analysis and personalized guidance. 
# Career Toolkit API

A FastAPI-powered backend for career development: chat summarization, personalized career roadmaps, and advanced resume review with ATS optimization.

## Features

- **Chat Summarization:**  
  Upload `.txt` files of mentor-mentee conversations to get a structured summary and key takeaways.

- **Career Roadmap Generation:**  
  Receive a detailed, actionable roadmap for your career growth, tailored to your level and query.

- **Resume Reviewer:**  
  Upload your `.pdf` resume for an in-depth review, ATS scoring, improvement suggestions, and an improved resume draft.

## Endpoints

| Endpoint               | Method | Description                                                       | Input Type    |
|------------------------|--------|-------------------------------------------------------------------|---------------|
| `/summarize`           | POST   | Summarize mentor-mentee chat from a `.txt` file                   | File (.txt)   |
| `/career-roadmap`      | GET    | Generate a career roadmap based on level and question             | Query params  |
| `/resume-reviewer`     | POST   | Review and improve a resume from a `.pdf` file                    | File (.pdf)   |
| `/`                    | GET    | Health check / Root endpoint                                      | -             |

## Usage

### 1. Summarize Chat

```
curl -X POST "http://localhost:8000/summarize"
-F "file=@your_conversation.txt
```


### 2. Generate Career Roadmap

```
curl -X GET "http://localhost:8000/career-roadmap?level=beginner&question=How%20to%20become%20a%20data%20scientist"
```


### 3. Resume Reviewer

```
curl -X POST "http://localhost:8000/resume-reviewer"
-F "file=@your_resume.pdf"
```


## Requirements

- Python 3.8+
- FastAPI
- groq
- PyMuPDF (`fitz`)

Install dependencies:

```
pip install fastapi groq pymupdf uvicorn
```


## Running the API

```
uvicorn app:app --reload
```


## Notes

- Ensure you have a valid Groq API key set in the code.
- Only `.txt` files are accepted for chat summarization; only `.pdf` files for resume review.
- All endpoints return responses in strict JSON format for easy parsing and integration.

## License

MIT License

---

*Empowering students and professionals with AI-driven career tools.*
