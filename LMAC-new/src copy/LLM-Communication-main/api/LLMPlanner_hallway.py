from LLM.call_llm_api.call_llm import TextChatbot
import config

class LLMPlanner:
    def __init__(self):
        self.planner_bot = TextChatbot("planner")
        
        env_info = config.process_obs_info(config.map_name)
        n_agents = env_info['n_agents']
        reward_win = 10  # 从hallway环境代码中获取
        
        self.system_content = '''
You are an expert in multi-agent systems and communication strategies. 
I will describe the map, the units, and the task scenario. 
Your job is to design a communication policy for the agents in this scenario.

Please output the communication policy in the following format for each agent:
### Agent X Communication Policy
**Trigger Condition:**
(When should this agent initiate communication? E.g., "When agent X reaches a specific state", "When agent X is approaching the goal", etc.)
**Communication Target(s):**
(Which agent(s) should X communicate with? Specify by agent ID or group membership)
**Message Content:**
(What information should be sent? E.g., "current state", "ready to move to goal", "wait for others", etc.)

If there are multiple communication rules for an agent, please enumerate them clearly.

The policy should be concise, readable, and actionable for code generation.
'''

        self.task_content = f'''
Hallway Environment - All-Agent Coordination Problem:

Environment Details:
- Agents: 4 agents with DIFFERENT state ranges:
  * Agent 0: states 0-4 (must travel 4 steps to reach goal)
  * Agent 1: states 0-6 (must travel 6 steps to reach goal)  
  * Agent 2: states 0-8 (must travel 8 steps to reach goal)
  * Agent 3: states 0-10 (must travel 10 steps to reach goal)
- Observations per agent: [current_state, active_status]
  - current_state: integer representing current position (0 = goal)
  - active_status: float (1.0 if active, 0.0 if inactive)
- Actions: 0=stay, 1=move left (decrease state), 2=move right (increase state)
- Goal: ALL 4 agents must reach state 0 SIMULTANEOUSLY
- Reward: +1 only if ALL 4 agents reach state 0 at the same time
- Time limit: max(state_range) + 10 = 20 steps

CRITICAL COORDINATION CHALLENGE:
1. Each agent has a different distance to travel (4, 6, 8, 10 steps)
2. The fastest agent (Agent 0) must wait for the slowest agent (Agent 3)
3. If ANY agent reaches 0 before others, the entire team FAILS
4. Agents cannot see each other's positions - communication is essential
5. This is a SINGLE group coordination problem (all 4 agents must coordinate together)

NEEDED COMMUNICATION STRATEGY:
Given the different travel distances, communication should focus on:
1. The slowest agent (Agent 3) should signal when it's approaching the goal
2. Faster agents should wait at safe positions until receiving signals
3. Synchronization should be based on the slowest agent's progress
4. Communication should be minimal - only when necessary for coordination

Paper Strategy (adapted for 4 agents with different distances):
1. Fastest agents move quickly to their border positions (state 1)
2. Slowest agent (Agent 3) moves toward goal at its own pace
3. When slowest agent reaches critical positions, it signals to others
4. All agents wait for synchronization signals
5. All move together for the final steps to reach state 0 simultaneously

Design Communication Policy:
Create a communication policy that enables this multi-agent synchronization.
Focus on:
1. Communication triggered by reaching critical positions (e.g., state 1, state 2)
2. Signals from slower agents to faster agents
3. Acknowledgments from faster agents to slower agents
4. Ensuring ALL agents are synchronized before the final move

Generate the communication policy following the specified format.
'''

    def plan(self, message=None):
        response = self.planner_bot.query(self.system_content, self.task_content, maintain_history=True)
        return response