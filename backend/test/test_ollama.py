from langchain_ollama import ChatOllama
import time

model = ChatOllama(
    model="qwen3.5:4b-q4_K_M",
    reasoning=False
)

start_time = time.time()
response = model.invoke(
    "introduce yourself"
)
end_time = time.time()

spent_time = end_time - start_time

print(f"Time cost for this prompt: {spent_time:.2f}s")
print(type(response))
print(response.content)