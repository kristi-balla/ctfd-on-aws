import json

def build_prompt(
    question: str,
    answer: str,
    solution: str
) -> str:
    
    prompt = f"""

# Answer Quality Judge

You are a judge evaluating the quality of an answer.

A user was asked this question: {question}

They provided this answer: {answer}

Evaluate the correctness of the answer based on the solution: {solution}.
Bear in mind that the user could mix up lower and uppercase, use synonyms or provide only parts of the solution.
In addition, the answer could be in German, or a mix of German and English.

If those, or other cases that semantically make sense, match the answer of the question to the solution, then return `pass`.
Otherwise, return `fail`.
Only return `pass` or `fail` and no other output
"""

    return prompt

def request_verdict(client, question: str, answer: str, solution: str) -> bool:
    prompt = build_prompt(question, answer, solution)

    response = client.converse( 
        modelId="amazon.nova-lite-v1:0",
        messages=[{ 
            "role": "user", 
            "content": [{"text": f"{prompt}"}]
        }]  
    )  

    result = response["output"]["message"]["content"][0]["text"]
    return True if result == "pass" else False
