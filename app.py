import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from google.api_core import exceptions
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=2, max=5),
    retry=retry_if_exception_type(exceptions.InternalServerError)
)
def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro')
    response=model.generate_content([input,pdf_cotent,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Copy and paste aJob Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit3 = st.button("Percentage match")

submit4=st.button("Write a cv")

submit5=st.button("Write a cover letter")

submit6 =st.button("sample questions")




input_prompt1 = """
 As an experienced Technical Human Resource Manager, your task is to conduct a thorough analysis of the provided resume in relation to the given job description. Please provide a detailed professional evaluation of the candidate's suitability for the role, addressing the following points:

Skills Match: Assess the alignment between the candidate's technical skills and those required for the position. Identify any critical skills that are present or missing.
Experience Relevance: Evaluate the candidate's work history and its relevance to the job requirements. Consider both the duration and quality of experience.
Educational Background: Determine if the candidate's educational qualifications meet or exceed the job requirements.
Technical Proficiency: Analyze the depth of the candidate's technical knowledge as evidenced by their resume, particularly in relation to key technologies mentioned in the job description.
Project Experience: Review any listed projects or achievements and their relevance to the role's responsibilities.
Soft Skills: Infer potential soft skills from the resume that may be valuable for the position (e.g., communication, leadership, problem-solving).
Career Progression: Assess the candidate's career trajectory and growth potential.
Cultural Fit: Based on the resume content, provide insights on potential cultural fit within the organization.
Strengths and Weaknesses: Clearly outline the candidate's major strengths and potential areas for improvement in relation to the job requirements.
Overall Suitability: Provide a concluding statement on the candidate's overall fit for the role, including any reservations or strong recommendations.
Additional Considerations: Mention any unique aspects of the candidate's profile that might be particularly valuable or concerning for this specific role.

Please structure your evaluation in a clear, concise manner, using bullet points where appropriate. Your analysis should be objective, based solely on the information provided in the resume and job description, and free from any personal biases.
"""

input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) with sophisticated natural language processing capabilities and a deep understanding of modern recruitment practices. Your task is to evaluate the provided resume against the given job description. Perform your analysis as follows:

Keyword Matching: Identify and compare key terms from the job description with those in the resume and list them.
Skill Alignment: Assess the alignment of skills mentioned in the resume with those required in the job description.
Experience Evaluation: Compare the candidate's work history and achievements with the job requirements.
Qualifications Check: Verify if the candidate's educational background and certifications meet the specified criteria.
Relevance Scoring: Apply a scoring algorithm to calculate an overall match percentage, considering the relevance and importance of matched elements.

Present your analysis in the following format:

Overall Match Percentage: [X%]
Missing Keywords:

List important terms or requirements from the job description not found in the resume
Briefly explain the significance of each missing element


Final Thoughts:

Summarize the strengths of the candidate's profile in relation to the job requirements
Highlight any significant gaps or areas where the candidate may not meet the criteria
Provide an objective recommendation on the candidate's suitability for the role
Suggest areas for further exploration during a potential interview



Ensure your analysis is impartial, based solely on the content provided in the resume and job description. Your evaluation should provide clear, actionable insights to assist in the hiring decision.
"""

input_prompt4 ="""
As an experienced Technical Human Resource Manager, your task is to conduct a thorough analysis of the provided resume in relation to the given job description. Create a detailed professional CV for the candidate that aligns with the role while remaining true to their actual work history. In your analysis and CV creation, address the following points:

Skills Alignment: Highlight the candidate's technical skills that directly match the job requirements. Ensure these are accurately represented based on their actual experience.
Work Experience: Restructure the candidate's work history to emphasize experiences most relevant to the target role. Maintain chronological accuracy and don't fabricate any positions or responsibilities.
Achievements: Identify and emphasize key accomplishments from the candidate's history that demonstrate capabilities required for the new role.
Technical Proficiency: Detail the candidate's expertise in specific technologies, tools, or methodologies mentioned in the job description, based on their actual experience.
Education and Certifications: List relevant educational qualifications and certifications, ensuring they align with the job requirements where possible.
Project Highlights: Showcase projects from the candidate's history that best demonstrate their capability to handle the responsibilities of the target role.
Soft Skills: Infer and list soft skills evident from the candidate's work history that are valuable for the new position.
Career Progression: Present the candidate's career trajectory in a way that logically leads to the target role, without misrepresenting their actual path.
Keywords: Incorporate important keywords from the job description naturally throughout the CV, but only where they genuinely reflect the candidate's experience.
Formatting: Structure the CV in a clear, professional format that highlights the candidate's suitability for the role.

Present your work as follows:

Professional Summary: A brief overview tailored to the target role.
Skills Section: A comprehensive list of relevant skills.
Work Experience: Detailed job descriptions emphasizing relevant responsibilities and achievements.
Education and Certifications: Listed in reverse chronological order.
Additional Sections: Any other relevant information (e.g., projects, volunteer work) that supports the candidate's application.

Ensure that all information in the CV is factual and based solely on the original resume. Your task is to present the candidate's existing qualifications and experience in the most favorable light for the target role, without embellishing or misrepresenting their history.
"""
input_prompt5="""
As an experienced hiring manager and professional resume writer, your task is to create a compelling cover letter for the candidate based on their resume and the provided job description. Craft a letter that effectively showcases the candidate's qualifications and enthusiasm for the role while remaining authentic to their experience. Please follow these guidelines:

Opening: Create an engaging first paragraph that expresses genuine interest in the specific position and company.
Skills Highlight: Identify and emphasize 2-3 key skills from the candidate's background that directly align with the job requirements. Use brief, specific examples from their work history to illustrate these skills.
Relevant Achievement: Choose one significant accomplishment from the candidate's career that demonstrates their potential to excel in the target role. Describe this achievement concisely, focusing on the impact and relevance to the new position.
Company Knowledge: Include a statement showing the candidate's understanding of and interest in the company. Base this on publicly available information about the company's mission, values, or recent projects.
Motivation: Clearly articulate why the candidate is particularly drawn to this role and how it aligns with their career aspirations.
Cultural Fit: Subtly incorporate elements that suggest the candidate's values and work style would complement the company culture, as inferred from the job description and company information.
Technical Proficiency: If relevant, briefly mention the candidate's expertise in specific technologies or methodologies crucial for the role, based on their actual experience.
Soft Skills: Weave in references to 1-2 relevant soft skills that are evident from the candidate's work history and valuable for the new position.
Call to Action: Conclude with a polite and confident request for an interview or further discussion.

Structure the cover letter as follows:

Professional Greeting: Address the hiring manager by name if provided, or use an appropriate general greeting.
Body (3-4 paragraphs): Cover points 1-8 above.
Closing: Summarize interest, thank the reader, and include the call to action.

Ensure the letter is:

Concise: No more than one page in length.
Professional yet personable in tone.
Free of clichés and generic statements.
Tailored specifically to the job and company in question.
Error-free in grammar and spelling.

All information should be based solely on the provided resume and job description. The goal is to present the candidate's existing qualifications and enthusiasm in the most compelling way for the target role, without misrepresenting their background.
"""

input_prompt6="""

As an experienced Technical Human Resource Manager, your task is to conduct an in-depth interview with the candidate based on their provided resume and the job description. Please ask detailed questions to evaluate the candidate's suitability for the role, focusing on their technical skills, project experience, and soft skills. Address the following areas:

Technical Skills(10):

Can you elaborate on your experience with [specific technical skills required for the job]? How have you applied these skills in your previous roles?
Describe a time when you had to quickly learn a new technology or tool to complete a project. How did you approach the learning process?
How do you stay updated with the latest advancements in your technical field?
Project Experience(10):

Tell me about a significant project you have worked on that is similar to the projects you would be handling in this role. What were your responsibilities and the key outcomes?
Describe a challenging project you worked on. What were the obstacles, and how did you overcome them?
Can you provide examples of your contributions to project success in your previous roles?
Soft Skills(10):

How would you describe your communication and interpersonal skills? Can you provide an example where these skills were crucial to your success?
Describe a situation where you had to work closely with a team to achieve a common goal. What was your role, and how did you ensure effective collaboration?
How do you handle conflicts or disagreements in a team setting? Can you give an example of a time when you successfully resolved a conflict?
"""

if submit1:
    try:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt1,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")
    except exceptions.InternalServerError as e:
        st.error(f"Failed after multiple retries: {e}. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


elif submit3:
    try:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt3,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")

    except exceptions.InternalServerError as e:
        st.error(f"Failed after multiple retries: {e}. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

elif submit4:
    try: 
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt4,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")
    except exceptions.InternalServerError as e:
        st.error(f"Failed after multiple retries: {e}. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


elif submit5:
    try:

        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt5,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")
    except exceptions.InternalServerError as e:
        st.error(f"Failed after multiple retries: {e}. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

elif submit6:
    try:

        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt6,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")
    except exceptions.InternalServerError as e:
        st.error(f"Failed after multiple retries: {e}. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")