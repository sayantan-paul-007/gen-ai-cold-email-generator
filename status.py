
from langchain_groq import ChatGroq
# api_key = "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"
# headers = {
#     "Authorization": f"Bearer {api_key}"
# }
# response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
# print(response.status_code)
# print(response.text)

llm =ChatGroq (
temperature=0,
groq_api_key="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",
model_name="llama-3.3-70b-versatile"
)
response = llm.invoke("The first person to land on moon was")
print(response.content)
