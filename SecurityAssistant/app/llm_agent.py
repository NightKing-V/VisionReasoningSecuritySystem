from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = Ollama(model="mistral", base_url="http://ollama:11434")

prompt = PromptTemplate(
    input_variables=["object_list"],
    template="""
You are an AI security assistant.

The following objects were detected in a surveillance image: {object_list}.

1. Describe the scene.
2. Is the scene suspicious? Answer 'Yes' or 'No' and explain your reasoning.
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def analyze_scene(labels):
    object_str = ", ".join(labels)
    return chain.run(object_list=object_str)
