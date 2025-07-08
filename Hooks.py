from agents import RunHooks, AgentHooks

class HealthRunHooks(RunHooks):
    def on_agent_start(self, agent, context):
        print(f"[RunHooks] Agent {agent.name} started.")
    def on_agent_end(self, agent, context):
        print(f"[RunHooks] Agent {agent.name} ended.")
    def on_tool_start(self, tool, context):
        print(f"[RunHooks] Tool {tool.name} started.")
    def on_tool_end(self, tool, context):
        print(f"[RunHooks] Tool {tool.name} ended.")
    def on_handoff(self, from_agent, to_agent, context):
        print(f"[RunHooks] Handoff from {from_agent.name} to {to_agent.name}.")

class HealthAgentHooks(AgentHooks):
    def on_start(self, agent, context):
        print(f"[AgentHooks] {agent.name} started.")
    def on_end(self, agent, context):
        print(f"[AgentHooks] {agent.name} ended.")
    def on_tool_start(self, tool, context):
        print(f"[AgentHooks] Tool {tool.name} started.")
    def on_tool_end(self, tool, context):
        print(f"[AgentHooks] Tool {tool.name} ended.")
    def on_handoff(self, from_agent, to_agent, context):
        print(f"[AgentHooks] Handoff from {from_agent.name} to {to_agent.name}.") 