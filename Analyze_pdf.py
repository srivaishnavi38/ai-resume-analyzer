from google import genai 
from google.genai import types
import os  
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
configuration = types.GenerateContentConfig(
    max_output_tokens=2048,
    response_mime_type="text/plain"
)
def analyse_resume_gemini(resume_content, job_description):
    prompt = f"""
    You are a professional resume analyzer.
    Resume:
    {resume_content}

    Job Description:
    {job_description}

    Task:
    - Analyze the resume against the job description.
    - Give a match score out of 100.
    - Identify the skills and requirements that match.
    - Highlight missing skills, qualifications, or experiences.
    - Suggest specific improvements to the resume.
    - Provide a brief summary of the candidate's suitability for the role.

    Return the result in the following structured format:

    Match Score: XX/100

    Matching Skills:
    - ...
    - ...

    Missing Skills:
    - ...
    - ...

    Suggestions:
    - ...
    - ...

    Summary:
    ...
    """
    response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt,
    config=configuration
)
    
    return response.text