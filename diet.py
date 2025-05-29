
import os
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

def get_full_day_diet_plan_llm(bmi, diet_type,disease,Goal):
    prompt = PromptTemplate(
        input_variables=["bmi", "diet_type" , "disease", "Goal"],
        template="""
I am a {diet_type} person with a BMI of {bmi} and having disease: {disease}.
Suggest a healthy full-day diet plan for {Goal}.

Output the result in HTML only — no markdown.

Use this style:
<style>
table, th, td {{
  border: 1px solid black;
  border-collapse: collapse;
  padding: 6px;
}}
th {{
  background-color: #D3D0C9;
  color: black;
}}
</style>

Structure it in 4 sections:
1. <h3>Breakfast</h3>
2. <h3>Lunch</h3>
3. <h3>Snacks</h3>
4. <h3>Dinner</h3>

Each section must include a table with these columns:
- Food Item
- Quantity
- Calories (approx.)
- Timing of eating
- Notes

Make the meals practical, varied, nutrient-rich, and disease-conscious.
Guidelines:
- take care of disease as prior input that not effect the health.
- at last must include total protein , fibre , carbs , and other vitamins and minerals get from the diet.

"""
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )

    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain.run({"bmi": f"{bmi:.2f}", "diet_type": diet_type, "disease": disease, "Goal": Goal})
    return result
