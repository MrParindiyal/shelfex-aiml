from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import os
from pydantic import BaseModel

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API"))


class Card(BaseModel):
    question: str
    answer: str


difficulty_matrix = {
    "easy": "one word",
    "medium": "a short phrase",
    "hard": "6-7 lines long paragraph",
}


def get_response(input_text, difficulty, subject, amount):

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=f"""
                You are tasked with building a lightweight yet robust Flashcard Generation Tool that utilizes Large Language Models (LLMs) 
                to convert educational content into effective question-answer flashcards. You need to output a minimum of 10-15 flashcards
                per input submission. Each flashcard must include: a Question (clear, concise) and an Answer (factually correct, self-contained).
                For example consider the following example input text and one sample flash card:

                Input : Cloud services are considered "public" when they are delivered over the public Internet, and they may be offered as a paid subscription, or free of charge. Architecturally, there are few differences between public- and private-cloud services, but security concerns increase substantially when services (applications, storage, and other resources) are shared by multiple customers. Most public-cloud providers offer direct-connection services that allow customers to securely link their legacy data centers to their cloud-resident applications. Several factors like the functionality of the solutions, cost, integrational and organizational aspects as well as safety & security are influencing the decision of enterprises and organizations to choose a public cloud or on-premises solution.
                
                Output (as a pure JSON. Expand the level of difficulty of question and length of answer based on target difficulty from user.):  
                
                [{{"question" : "What is a major security concern with public cloud services compared to private cloud services?",
                "answer" : "In public cloud services, security concerns increase substantially because applications, storage, and other resources are shared by multiple customers over the public Internet."}}]

                Questions must be from the input text, and answers must be from the input text. Neither ask questions NOR give answers with information that is not included in the input text.
            """,
            response_mime_type="application/json",
            response_schema=list[Card],
        ),
        contents=f"Generate {amount} flashcards of {difficulty} difficulty, subject related to {subject}, in {difficulty_matrix[difficulty.lower()]}."
        + input_text,
    )
    return listify(response.text)


def listify(json_output):
    data = json.loads(json_output)
    return data


def custom_css():
    return """
<style>
    /* Navigation bar styling */
    .navbar {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
   
    .navbar h1 {
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
   
    .spinner > div {
        border-top-color: #555500; 
    }
    /* Flashcard styling */
    .flashcard {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #6fff7f;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
   
    .flashcard:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        border-color: #93f59e;
    }
   
    .flashcard-front {
        background: linear-gradient(135deg, #33092d 0%, #4a295a 100%);
        color: white;
        border-color: #8756a3;
    }
   
    .flashcard-back {
        background: linear-gradient(135deg, #33092d 0%, #4a295a 100%);
        color: #93f59ee;
        border-color: #8756a3;
    }
   
    .flashcard-content {
        font-size: 1.1rem;
        line-height: 1.6;
        font-weight: 500;
    }
   
    .flashcard-label {
        position: absolute;
        top: 10px;
        right: 15px;
        background: rgba(255, 255, 255, 0.2);
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
   
    /* Generate button styling */
    .stButton > button {
        background: linear-gradient(90deg, #585e4c 0%, #425e3e 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
   
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover:active {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        color: #93f59e;
    }
   
    /* Input field styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
        box-sizing: border-box;
    }

    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }

    .stMarkdown h3 {
        font-size: 10rem !important;
    }
   
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
   
    .spinner {
        border: 4px solid #ff0000;
        border-top: 4px solid #0000ff;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
   
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
"""
