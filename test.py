from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama

model = ChatOllama(
    model='llama'
)

message = [
    SystemMessage(content=('Ты 10 летний python backend и javascript frontend разработчик'
                           'отвечай на все вопросы от пользователя как подобает твоему уровню')
    ),
    HumanMessage(content=('Как frontend и backend общаются между собой по сети?')
    ),
]

response = model.invoke(message)
print(type(response))
print(response)