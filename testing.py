from tools.tools import Tools
from agent.agent import Agent

# Direct tool usage
print("Direct tool usage:")
tools = Tools.get_tools()
calculate = tools["calculate"]
print("2 + 2 =", calculate.run("2 + 2"))
print("4 * 7 / 3 =", calculate.run("4 * 7 / 3"))
print("10 - 3**2 =", calculate.run("10 - 3**2"))
print("1 / 0 =", calculate.run("1 / 0"))  # Should show error handling

# Agent usage
agent = Agent()
query = "What is 2 + 2?"
result = agent(query)
print(f"\nAgent usage:\nQuery: {query}\nResult: {result}")
