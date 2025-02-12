from typing import List, TypedDict
# from langchain_community.document_loaders import WebBaseLoader
from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
# from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
# from langsmith import Client
from langchain import hub


class InputState(TypedDict):
  question: str

class OutputState(TypedDict):
  agent_output_value: str

class OverallState(TypedDict):
    question: str
    agent_output_value: str

# class ModelOutputFormat(BaseModel):
#     value_a: str = Field(description="Explain what needs to be in this field")
#     value_b: List[str] = Field(description="Explain what needs to be in this field")

def initial_step(state: InputState) -> OverallState:
  overall_state: OverallState = {}
  
  # do some work

  overall_state["temp_value_a"] = 'foobar'
  overall_state["temp_value_b"] = ['foo', 'bar']
  return overall_state


def model_call(state: OverallState) -> OverallState:
  updated_state: OverallState = {}
  updated_state.update(state)

  model = ChatOpenAI(model="gpt-4o", temperature=0.7)
  # output_parser = PydanticOutputParser(pydantic_object=ModelOutputFormat)
  # langsmith_client = Client()
  # prompt = langsmith_client.pull_prompt("test_prompt")
  prompt = hub.pull("test_prompt")

  print("***** hub called")

  prompt.input_variables = ["question"]
  # prompt.partial_variables = {"format_instructions": output_parser.get_format_instructions()}

  chain = prompt | model    # .with_structured_output(ModelOutputFormat)
  response = chain.invoke({
      "question": state["question"],
  })

  updated_state["agent_output_value"] = response['result']
  return updated_state


def final_step(state: OverallState) -> OutputState:
  output_state: OutputState = {}
  output_state['agent_output_value'] = state['agent_output_value']
  # do some work
  return output_state

builder = StateGraph(OverallState,input=InputState,output=OutputState)
builder.add_node("initial_step", initial_step)
builder.add_node("model_call", model_call)
builder.add_node("final_step", final_step)
builder.add_edge(START, "initial_step")
builder.add_edge("initial_step", "model_call")
builder.add_edge("model_call", "final_step")
builder.add_edge("final_step", END)

graph = builder.compile()
