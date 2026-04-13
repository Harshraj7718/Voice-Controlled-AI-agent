import ollama
import json

def detect_intent(text):
    try:
        prompt = f"""
You are an intent classification system.

STRICT RULES:
- ONLY return valid JSON
- NO explanation
- NO extra text

Return format:
[
  {{"intent":"create_file","filename":"test.txt"}}
]

Available intents:
create_file, write_code, summarize, chat

Examples:

Input: Create a file test.txt
Output:
[{{"intent":"create_file","filename":"test.txt"}}]

Input: Write python code for factorial
Output:
[{{"intent":"write_code","filename":"code.py"}}]

Input: Summarize this text
Output:
[{{"intent":"summarize","filename":null}}]

Input: Hello
Output:
[{{"intent":"chat","filename":null}}]

Now classify:

Input: {text}
Output:
"""

        # CALL OLLAMA
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        # DEBUG PRINT 
        print("RAW OLLAMA RESPONSE:", response)

        output = response['message']['content'].strip()

        
        output = output.replace("```json", "").replace("```", "").strip()

        print("CLEANED OUTPUT:", output)

        try:
            intents = json.loads(output)

            if isinstance(intents, dict):
                intents = [intents]

            return intents

        except Exception as parse_error:
            print("JSON PARSE ERROR:", parse_error)

           
            return [{"intent": "chat", "filename": "output.txt"}]

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return [{"intent": "error", "filename": None, "error": str(e)}]