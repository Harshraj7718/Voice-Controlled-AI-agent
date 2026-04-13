import os
import ollama

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


#  CREATE FILE
def create_file(filename):
    try:
        if not filename:
            filename = "output.txt"

        path = os.path.join(OUTPUT_DIR, filename)

        with open(path, "w") as f:
            f.write("")

        print(f"[DEBUG] File created at {path}")
        return f"File created: {path}"

    except Exception as e:
        print("[ERROR create_file]:", e)
        return f"File Error: {str(e)}"



#WRITE CODE
def write_code(filename, code):
    try:
        if not filename.endswith(".py"):
            filename = filename.replace(".txt", ".py")

        path = os.path.join(OUTPUT_DIR, filename)

        with open(path, "w") as f:
            f.write(code)

        print(f"[DEBUG] Code written to {path}")
        return f"Code written to {path}"

    except Exception as e:
        print("[ERROR write_code]:", e)
        return f"Code Write Error: {str(e)}"



#  GENERATE CODE
def generate_code(prompt):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Write clean Python code for:

{prompt}

IMPORTANT:
- Only return code
- No explanation
- No markdown
"""
                }
            ],
            options={"temperature": 0}
        )

        code = response['message']['content'].strip()

        print("[DEBUG] RAW CODE:", code)

        
        if "```" in code:
            parts = code.split("```")
            if len(parts) >= 3:
                code = parts[1]
            else:
                code = parts[-1]

            
            if code.strip().startswith("python"):
                code = code.replace("python", "", 1).strip()

        return code.strip()

    except Exception as e:
        print("[ERROR generate_code]:", e)

        return """# Fallback code
def example():
    print("Code generation failed")
"""



#  SUMMARIZE

def summarize(text):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this text clearly:\n{text}"
                }
            ]
        )

        return response['message']['content']

    except Exception as e:
        print("[ERROR summarize]:", e)
        return f"Summarization Error: {str(e)}"


# CHAT

def chat_response(text):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": text}
            ]
        )

        return response['message']['content']

    except Exception as e:
        print("[ERROR chat]:", e)
        return f"Chat Error: {str(e)}"
    
   
    #Hello, my name is Harsh.
#In this project, I built a Voice-Controlled AI Agent that takes audio input,
#  converts it into text, understands user intent using a local Large Language Model, 
# and executes real tasks like creating files, generating code, and summarizing content.