from agents.tool import function_tool

def test_tool(x: int) -> dict:
    return {"y": x}

test_tool = function_tool(test_tool)