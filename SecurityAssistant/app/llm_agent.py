from datetime import datetime
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = Ollama(model="mistral", base_url="http://ollama:11434")

prompt = PromptTemplate(
    input_variables=["object_list", "timestamp"],
    template="""
You are an AI security assistant.

The following objects were detected in a surveillance frame at {timestamp}: {object_list}.

1. Describe the scene briefly and clearly.
2. Determine if the scene is suspicious (Yes/No) no need explanation.
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def analyze_scene(labels):
    object_str = ", ".join(labels)
    ts_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return chain.run(object_list=object_str, timestamp=ts_str)
