# fitbee_chat.py
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

prompt = PromptTemplate(
    template="""You are FitBee, an expert fitness coach. Respond helpfully and concisely.
    resolve the issues of users as required. 
    Question: {question}
    FitBee:
    
    """
)

chain = LLMChain(llm=llm, prompt=prompt)
# question = "generate a diet paln in tabular form my bmi is 26.2 and i want to gain muscle mass"
def get_fitbee_response(question):
    return chain.run(question)
# print(chain.run(question))
