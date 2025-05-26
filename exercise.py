from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()



def get_exercise_plan_llm(goal, body_type, injury, height, weight, age):
    prompt = PromptTemplate(
        input_variables=["goal", "body_type", "injury", "height", "weight", "age"],
        template="""
You are a certified fitness coach. Create a **personalized weekly exercise plan** with the following details:

- Age: {age}
- Goal: {goal}
- Body Type: {body_type}
- Height: {height} cm
- Weight: {weight} kg
- Past Injuries: {injury}

Output Instructions:
- Use **pure HTML with inline CSS styles**.
- Every day's plan should be a separate table titled with `<h3>Day X</h3>`.
- Include a `<style>` section for borders:
  <style>
  table, th, td {{
    border: 1px solid black;
    border-collapse: collapse;
    padding: 6px;
  }}
  th {{
    background-color: #f2f2f2;
    color: black;
  }}
  </style>

Each day's table must have the following columns:
- Exercise
- Sets/Reps or Duration
- Notes

Guidelines:
- Tailor intensity based on age and fitness goal.
- Avoid exercises that could worsen the injuries.
- End with a paragraph of **rest/recovery advice**.
"""
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )

    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain.run({
        "goal": goal,
        "body_type": body_type,
        "injury": injury.strip() if injury else "None",
        "height": str(height),
        "weight": str(weight),
        "age": str(age)
    })

    return result
