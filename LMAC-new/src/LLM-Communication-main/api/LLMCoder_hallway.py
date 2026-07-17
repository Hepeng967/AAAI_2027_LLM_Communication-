from LLM.call_llm_api.call_llm import TextChatbot
import config
import numpy as np
import re
import os
import datetime
import torch
import traceback
import random

class LLMCoder:
    def __init__(self):
        self.coder_bot = TextChatbot("coder")
        env_info = config.process_obs_info(config.map_name)
        self.n_agents = env_info['n_agents']
        self.obs_dim = env_info['obs_shape']
        self.obs_feature_names = env_info['obs_feature_names']
        self.map_name = config.map_name
        self.seed = random.randint(1, 1000)
        
        self.system_content = f'''
You are an expert in multi-agent communication for coordination problems.
Your task is to read the following Communication Policy (in natural language) and translate it into a pure Python mask function for neural network training.
The function must support three modes (controlled by the mode parameter):

1. 'object' mode: Only select which agent communicates with which agent. The function should return a mask of shape (bs, n_agents, n_agents, 1), where mask[b, i, j, 0]=1 means agent i sends all its information to agent j in batch b, 0 means not sent.

2. 'content' mode: Select which content (obs dimension) is sent between each agent pair. The function should return a mask of shape (bs, n_agents, n_agents, obs_dim), where mask[b, i, j, k]=1 means agent i sends the k-th dimension of its observation to agent j in batch b, 0 means not sent. All agent pairs may communicate, but the content is selected.

3. 'object_content' mode: Jointly select both communication object and content. The function should return a mask of shape (bs, n_agents, n_agents, obs_dim), where mask[b, i, j, k]=1 means agent i sends the k-th dimension of its observation to agent j in batch b, 0 means not sent. If agent i does not communicate with agent j, all mask[b, i, j, :] should be 0.

The function signature must be:
def generate_mask(obs, mode='object'):
    ...
Where obs is a numpy array of shape (bs, n_agents, n_agents, obs_dim), and mode is one of the three above.
All policy logic must be encoded in the function body. Do not require policy as a runtime input. Use the obs_feature_names list to map content to obs indices.

HALLWAY ENVIRONMENT SPECIFICS:
- This is a complex ALL-agent coordination problem with {self.n_agents} agents
- Each agent has DIFFERENT maximum states:
  * Agent 0: states 0-4 (max state 4)
  * Agent 1: states 0-6 (max state 6)
  * Agent 2: states 0-8 (max state 8)  
  * Agent 3: states 0-10 (max state 10)
- Observation dimensions: {self.obs_dim} (2 features)
  Feature 0: 'current_state' - agent's current position (0 means goal)
  Feature 1: 'active_status' - whether agent is active (1.0=active, 0.0=inactive)
- Key challenge: Agents must synchronize despite different travel distances
- Communication must account for timing differences between agents
- Typical triggers based on relative progress, not just absolute positions

GENERATING MASK FUNCTION FOR THIS COMPLEX HALLWAY:
1. Consider each agent's maximum state when determining triggers
2. Communication should help faster agents know when to wait
3. Slower agents should signal their progress to others
4. Focus on synchronization for simultaneous arrival

IMPLEMENTATION GUIDANCE FOR HETEROGENEOUS COORDINATION:
1. Consider each agent's maximum state when determining communication triggers
2. Agent 3 (max state 10) should send progress updates when reaching key milestones (e.g., state 5, state 2)
3. Agent 0 (max state 4) should wait at state 1 until receiving signals from slower agents
4. Communication should enable staggered waiting based on travel distance

IMPORTANT CODING REQUIREMENTS:
- All torch tensor operations MUST ensure that shapes are EXACTLY matched.
- Do NOT rely on broadcasting; manually align shapes.
- No for loops; use torch's batch operations only.
- Before expanding a tensor, always use view or unsqueeze to adjust shape.
- All parentheses must be properly closed and matched.
- Test with: obs = torch.randn(2, {self.n_agents}, {self.n_agents}, {self.obs_dim}); mask = generate_mask(obs, mode='object_content')
'''

    def generate_mask(self, policy, mode='object', promotion='', max_retry=10):
        attempt = 0
        last_error = ''
        
        while attempt < max_retry:
            prompt = f"""
The Communication Policy is as follows:
{policy}

HALLWAY ENVIRONMENT DETAILS - 4 AGENTS WITH DIFFERENT STATE RANGES:
- Number of agents: {self.n_agents} (4 agents)
- Each agent has a DIFFERENT maximum state:
  * Agent 0: states 0-4 (max state 4)
  * Agent 1: states 0-6 (max state 6)
  * Agent 2: states 0-8 (max state 8)
  * Agent 3: states 0-10 (max state 10)
- Observation dimensions: {self.obs_dim}
  obs_feature_names = {self.obs_feature_names}
  [0] current_state: agent's current position (0 means goal)
  [1] active_status: whether agent is active (1.0=active, 0.0=inactive)

CRITICAL COORDINATION CONSTRAINTS:
1. All 4 agents must reach state 0 SIMULTANEOUSLY
2. Agents have different travel distances: 4, 6, 8, 10 steps
3. The fastest agent (Agent 0) must wait for the slowest (Agent 3)
4. Communication must account for these timing differences

{promotion}

IMPLEMENTATION REQUIREMENTS FOR THIS COMPLEX HALLWAY:
1. The obs input has shape (bs, n_agents, n_agents, 2)
2. obs[:, i, j, 0] gives current_state of agent i from perspective of agent j
3. obs[:, i, j, 1] gives active_status of agent i from perspective of agent j
4. Communication triggers should consider:
   - Each agent's progress relative to its maximum state
   - Faster agents waiting for slower agents
   - Synchronization signals when agents reach critical waypoints
5. For object mode: create mask of shape (bs, n_agents, n_agents, 1)
6. For content/object_content modes: create mask of shape (bs, n_agents, n_agents, 2)

ADVANCED IMPLEMENTATION NOTES:
1. Since each agent has different max state, you may need to:
   - Store each agent's max state as a tensor: [4, 6, 8, 10]
   - Calculate progress percentage: current_state / max_state
   - Use different triggers for different agents
2. Consider implementing a leader-follower pattern:
   - Agent 3 (slowest) sends progress updates
   - Agents 0-2 send acknowledgments when they reach waiting positions
3. The mask function must handle 4 agents, not just 2

CRITICAL CODING REQUIREMENTS:
1. Use torch operations only, no numpy.
2. No for loops - use vectorized operations.
3. Ensure tensor shapes match exactly before operations.
4. Implement the policy triggers based on state values and agent indices.
5. Support all three modes (object, content, object_content).
6. Consider using agent indices to differentiate behaviors.

Example structure for complex triggering:
# Each agent's max state (hardcoded based on agent index)
max_states = torch.tensor([4, 6, 8, 10], device=obs.device).view(1, 4, 1, 1)
# Calculate progress percentage
progress = obs[:, :, :, 0] / max_states
# Create triggers based on progress thresholds

Generate the complete generate_mask function that implements the communication policy for this complex hallway environment.
"""
            response = self.coder_bot.query(self.system_content, prompt, maintain_history=True)
            code = self.extract_code(response)
            print(f"[LLMCoder][Attempt {attempt+1}]")
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'matrix_code', self.map_name, f'{self.seed}')
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f'{timestamp}_try{attempt+1}.py')
            
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(code if code else response)
            
            if code is None or 'def generate_mask' not in code:
                print(f"[LLMCoder][ERROR] LLM did not generate a valid function. Raw output:\n{response}")
                promotion += f"\n[BUG] LLM did not generate a valid function. Please fix."
                attempt += 1
                continue
            
            local_vars = {}
            try:
                exec(code, {'np': np, 'torch': torch}, local_vars)
                gen_func = local_vars.get('generate_mask', None)
                
                if gen_func is None:
                    print(f"[LLMCoder][ERROR] No generate_mask function found in code.")
                    tb = traceback.format_exc()
                    promotion += f"\n[BUG] No generate_mask function found. Traceback:\n{tb}\nPlease fix."
                    attempt += 1
                    continue
                
                test_modes = ['object', 'content', 'object_content']
                all_pass = True
                
                for test_mode in test_modes:
                    try:
                        test_obs = torch.randn(1, self.n_agents, self.n_agents, self.obs_dim)
                        mask = gen_func(test_obs, test_mode)
                        
                        if test_mode == 'object':
                            expected_shape = (1, self.n_agents, self.n_agents, 1)
                        else:
                            expected_shape = (1, self.n_agents, self.n_agents, self.obs_dim)
                        
                        if mask.shape != expected_shape:
                            raise ValueError(f"Shape mismatch. Got {mask.shape}, expected {expected_shape}")
                            
                    except Exception as run_e:
                        tb = traceback.format_exc()
                        print(f"[LLMCoder][ERROR] Runtime error in mode={test_mode}: {run_e}\nTraceback:\n{tb}")
                        promotion += f"\n[BUG] Runtime error in mode={test_mode}: {run_e}\nTraceback:\n{tb}\nPlease fix the code."
                        all_pass = False
                        break
                
                if all_pass:
                    print(f"[LLMCoder][SUCCESS] generate_mask function successfully generated and passed all mode tests. Saved at: {save_path}")
                    return gen_func
                else:
                    attempt += 1
                    continue
                    
            except Exception as e:
                tb = traceback.format_exc()
                print(f"[LLMCoder][ERROR] Code execution error: {e}\nTraceback:\n{tb}")
                promotion += f"\n[BUG] Exec error: {e}\nTraceback:\n{tb}\nPlease fix the code."
                attempt += 1
                continue
        
        print(f"[LLMCoder][FATAL] Failed to generate usable code after {max_retry} attempts. Last error: {promotion}")
        return None

    @staticmethod
    def extract_code(response):
        code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
        if not code_match:
            code_match = re.search(r'```(.*?)```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        return response.strip() if 'def generate_mask' in response else None