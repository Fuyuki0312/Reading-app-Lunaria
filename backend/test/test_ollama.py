from langchain_ollama import ChatOllama

model = ChatOllama(
    model="qwen3.5:4b-q4_K_M",
    reasoning=False
)

response = model.invoke(
    "introduce yourself"
)

print(type(response))
print(response.content)