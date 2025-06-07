from agent.agent import Agent

# # Direct tool usage
# print("Direct tool usage:")
# tools = Tools.get_tools()
# calculate = tools["calculate"]
# print("2 + 2 =", calculate.run("2 + 2"))
# print("4 * 7 / 3 =", calculate.run("4 * 7 / 3"))
# print("10 - 3**2 =", calculate.run("10 - 3**2"))
# print("1 / 0 =", calculate.run("1 / 0"))  # Should show error handling

# # Agent usage
agent = Agent()
# query = "What is 2 + 2?"
# result = agent(query)
# print(f"\nAgent usage:\nQuery: {query}\nResult: {result}")


# # Agent with Plotting Tool
# query_plot = "Plot the function y = x^2 for x in range(-10, 11)"
# result_plot = agent(query_plot)
# print(f"\nAgent usage with Plotting Tool:\nQuery: {query_plot}\nResult: {result_plot}")

# Difficult math problems for agent testing
print("\nDifficult math problems (agent):")

# 1. Multi-variable symbolic integration
difficult_query1 = "Integrate the function f(x, y) = x*y^2 with respect to x and y."
result1 = agent(difficult_query1)
print(f"\nQuery: {difficult_query1}\nResult: {result1}\n(Expected: (1/6)*x**2*y**3)")

# # 2. Multi-step symbolic differentiation
# difficult_query2 = "Differentiate f(x, y, z) = x^2*y + sin(z) with respect to x, then y, then z."
# result2 = agent(difficult_query2)
# print(f"\nQuery: {difficult_query2}\nResult: {result2}\n(Expected: 0)")

# # 3. Numeric evaluation with trigonometry
# difficult_query3 = "What is sin(pi/4) + cos(pi/4)?"
# result3 = agent(difficult_query3)
# print(f"\nQuery: {difficult_query3}\nResult: {result3}\n(Expected: sqrt(2) ≈ 1.4142)")

# 4. Numeric integration (approximate)
difficult_query4 = "Numerically evaluate the integral of exp(-x^2) from x = -2 to x = 2."
result4 = agent(difficult_query4)
print(f"\nQuery: {difficult_query4}\nResult: {result4}\n(Expected: ≈ 1.764)")

# 5. Plotting (visual check)
difficult_query5 = "Plot the function y = sin(x) * exp(-x/10) for x in range(-20, 20)."
result5 = agent(difficult_query5)
print(f"\nQuery: {difficult_query5}\nResult: {result5}\n(Expected: damped sine wave plot)")
