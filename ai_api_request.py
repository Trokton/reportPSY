import google.generativeai as genai
import os

# Fetch the API key from an environment variable
api_key = os.environ.get("AI_API_KEY")
if not api_key:
    raise EnvironmentError("The environment variable 'AI_API_KEY' is not set. Please set it to your API key.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "Summarize the differences between the thesis statements for these documents."

response = model.generate_content([prompt, sample_file, sample_file_2, sample_file_3])
print(response)