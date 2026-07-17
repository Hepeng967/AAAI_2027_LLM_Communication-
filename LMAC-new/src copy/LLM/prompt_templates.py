class PromptTemplates:

    @staticmethod
    def get_step1_info():
        return {
            'step_num': 1,
            'step_name': 'Task-Decision Coverage',
            'step_goal': 'Ensure each receiver obtains task-critical facts needed for decentralized decisions',
            'step_instruction': 'Improve communication by covering missing decision-relevant information',
            'specific_instruction': """Considering the provided feedback, refine the communication approach to cover task-critical facts that affect movement, attack, retreat, target selection, or coordination. Prediction errors are diagnostic signals only; do not optimize for full state reconstruction.""",
            'enhancement_goals': [
                'Ensure receivers obtain facts they cannot reliably observe locally',
                'Prioritize facts that can change action choices or team return',
                'Address agent-specific information bottlenecks without reconstructing the full state'
            ],
            'analysis_logic': """
**Analysis Method (Phase 1 Focus - Task-Decision Coverage)**:
- **Use predictability as a probe, not the objective**: Compare 'with_communication' vs 'without_communication' to identify information bottlenecks.
- **Identify missing decision facts**: Focus on facts that receivers lack locally and that can change actions such as moving, attacking, retreating, or focusing fire.
- **Isolate sender/receiver roles**: Identify which sender observes the fact and which receiver needs it for decentralized decision-making.
"""
        }

    @staticmethod
    def get_step2_info():
        return {
            'step_num': 2,
            'step_name': 'Certified Edge Refinement',
            'step_goal': 'Make communication edges necessary, compact, and task-decision complete',
            'step_instruction': 'Refine when/who communication to remove redundancy and preserve certified task-fact edges',
            'specific_instruction': """Improve the current communication approach by emphasizing necessary sender-to-receiver facts. You must preserve facts that are feasible for the sender, needed by the receiver, and relevant to task decisions; remove redundant communication that does not support those criteria.""",
            'enhancement_goals': [
                'Keep communication focused on necessary sender-receiver pairs',
                'Reduce redundant edges while preserving task-decision completeness',
                'Focus on variables whose absence changes coordination decisions'
            ],
            'analysis_logic': """
**Analysis Method (Step 2 Focus - Certified Edge Refinement)**:
- **Analyze asymmetry**: High variance can indicate that some agents observe task-critical facts while others need them.
- **Identify certified sources**: Prefer sender-receiver edges where the sender can observe the fact and the receiver needs it for action selection.
- **Check compactness**: Avoid all-to-all communication unless the task truly requires every receiver to use the sender's fact.
"""
        }


    @staticmethod
    def _get_description_I_T(task_description, obs_shape, obs_dim_desc, detail_content, important_dims=None, task_additional_description=""):
        """
        [Component 1] Task Description (I_T)
        Specifies cooperative goal, environment characteristics, and information structure.
        Includes Important State Dimensions (Task Information Structure).
        """
        state_description = ""
        if important_dims:
            state_description = f"""
**Reasoning Tokens - Important State Dimensions**:
Based on previous analysis, the following state dimensions were identified as critical:
{important_dims}
{task_additional_description}
These dimensions are diagnostic candidates for communication. The protocol should only transmit the subset that is feasible for the sender, necessary for the receiver, and relevant to task decisions.
"""

        return f"""
**Task Description and Environment Characteristics**:

**Task Description**:
{task_description}

**State Information**:
{state_description}

**Observation Information**:
- Observation tensor shape: {obs_shape}
- {obs_dim_desc}
- Each dimension meaning: {detail_content}

"""

    @staticmethod
    def _get_instruction_I_P(obs_shape, indexing_example, additional_msg_prompt):
        """
        [Component 2] Protocol Instruction (I_P)
        Specifies required input-output format and design objectives.
        """
        return f"""
**Protocol Design Instructions**:

**Communication Design Key Principles**:
1. **Task-Decision Completeness & Knowledge Gap Bridging:**
- **Analyze Semantic Relationship**: Before designing, identify which local observations correspond to task-critical facts that other agents lack.
- **Target Partial Observability**: In POMDPs, global states are hidden. Do not access them directly. Share only local features that help receivers choose better actions.
- **Do not optimize for full state reconstruction**: State predictability is only a diagnostic signal. The protocol should cover decision bottleneck variables, not every recoverable state dimension.

2. **Uniqueness, Sufficiency & Compactness**:
- Share only essential information not already known or easily inferred by others.
- Ensure sufficiency for coordination while strictly minimizing redundancy.
- A message is sufficient only if it covers the required task facts that can affect action choice, Q-values, or team return.

3. **Contextual and Interaction-Aware**:
- Prioritize self-perceived behavioral data (e.g., movement possibilities, recent actions) to compensate for partial visibility.

4. **Explicitness and Clarity**:
- Avoid abstraction; critical task information must be explicit and interpretable.

5. **Structured Output**:
- Output shape: ({obs_shape.split(',')[0].strip('(')}, {obs_shape.split(',')[1].strip()}, {obs_shape.split(',')[2].strip().rstrip(')')} + message_dim).

6. **Communication Protocol**:
- Messages must be transmitted to other agents, ensuring they receive the information.
- The received message is then appended to the recipient's observation vector.
- Do NOT include the message in the sender's own observation.

7. **Computational Efficiency**:
- No trainable components; minimize loops for batch efficiency.

**Observation Access Pattern**:
For example: {indexing_example}

**Protocol Requirements**: 
{additional_msg_prompt}

**Task**: Design a protocol using the identified critical dimensions to improve coordination and task decisions. The protocol should be suitable for a static certificate: sender feasibility, receiver necessity, task-decision relevance, and sensitivity to task-critical perturbations.

**Required Python Functions**:

1. `message_design_instruction()`:
- Returns a string explaining sender feasibility, receiver necessity, task-decision relevance, and why the message is compact.

2. `communication(o)`:
- Input: Observation `o`.
- Output: Enhanced observation with messages that provide task-critical facts to the intended receivers.
- Logic: Extract key information from `o` and format it for others' consumption.

3. `communication_matrix(o)`:
- Input: The same observation tensor `o`.
- Output: A float/binary communication matrix with shape `(batch_size, n_agents, n_agents)`.
- Matrix convention: `matrix[:, receiver, sender] = 1` means the receiver should use the sender's message at the current step.
- Self-communication must be zero on the diagonal.
- This matrix is used as a teacher for a learnable communication selector during RL training, so it should encode the protocol's when/who decisions.

**Constraints**:
- Executable, integration-ready Python code.
- **Vectorized operations only** (minimize for-loops) for efficiency.
- **Semantic Inference**: Analyze the semantic relationship between the required information and the available features in 'o'. You must exclusively utilize the existing features in 'o' to infer or approximate the target information, strictly prohibiting the assumption of any particular features that are not explicitly listed in the 'Observation Information'.

Let's think step by step. Below is an illustrative example of the expected output:

```python
import torch as th
def message_design_instruction():
    # Explain feasibility, necessity, task-decision relevance, and compactness.
    return message_description

def communication(o):
    # Implement protocol logic using vectorized operations.
    # Input o: {obs_shape}, Output: {obs_shape} + message_dim
    # Ensure device consistency.
    return messages_o

def communication_matrix(o):
    # Return teacher when/who matrix: [batch, receiver_agent, sender_agent].
    return matrix
```
"""

    @staticmethod
    def get_reasoning_prompt_z0(detail_content_state, task_description):
        """
        [Step 0-1] Important State Reasoning Prompt (Generates z^(0))
        LLM acts as a 'Reasoning Agent' to select important states.
        Matches original: get_llm_d_prompt
        """
        return f"""
You are a reasoning agent designing an importance extractor function for multi-agent reinforcement learning.
=========================================================
The agents' task description is:
{task_description}
=========================================================
Important notes:
- The explanation of each state dimension is provided here:
{detail_content_state}
=========================================================
Your task:
Write a Python function named `select_important_state()` that:

**Task-driven Hypothesis (Initial Reasoning)**:  
- Based on the task description and the meaning of each state dimension, form an initial hypothesis about which dimensions are likely important for task success.  
- In this partially observable multi-agent environment, each agent only perceives a limited view of the global state. Therefore, dimensions that are hard to perceive individually but critical when inferred through inter-agent communication should be prioritized. These dimensions are assumed to contribute significantly to coordinated decision-making and ultimately to task success.

Let's think step by step. Below is an illustrative example of the expected output:

```python
import numpy
def select_important_state():
    # Your implementation here
    # A brief explanation as an in-code comment about why you selected these dimensions
    return important_dims  # e.g., [idx,...]
```
"""

    @staticmethod
    def get_input_prompt_x(important_dims, task_description, task_additional_description, detail_content, 
                           obs_shape, obs_dim_desc, indexing_example, additional_msg_prompt=""):
        """
        [Step 0-2] Input Prompt x (Combines I_T and I_P only)
        Strictly x = I_T + I_P as per paper.
        """
        I_T = PromptTemplates._get_description_I_T(
            task_description, obs_shape, obs_dim_desc, detail_content, 
            important_dims, task_additional_description
        )
        
        I_P = PromptTemplates._get_instruction_I_P(
            obs_shape, indexing_example, additional_msg_prompt
        )
        return f"""
You are a communication design agent for Multi-Agent Reinforcement Learning (MARL).
Your goal is to design a task-specific communication protocol that maximizes decentralized decision quality and coordination efficiency, without relying on full state reconstruction as the objective.

=========================================================
[PART 1] Task Description (I_T)
=========================================================

{I_T}

=========================================================
[PART 2] Protocol Design Instruction (I_P)
=========================================================

{I_P}
"""

    @staticmethod
    def get_feedback_instruction_x_tilde(analysis_data, task_description, detail_content, obs_shape, 
                          obs_tensor_desc, obs_example, predictability_calc, 
                          timewise_additional_prompt, next_k_input_data, 
                          task_additional_description, previous_comm_protocol, json_data,
                          phase_info=None):
        """
        [Step k] Feedback Instruction x_tilde
        Guides the Analysis Agent to generate feedback c^(k).
        """
        I_T = PromptTemplates._get_description_I_T(task_description, obs_shape, obs_tensor_desc, detail_content)
        
        extras = []
        if timewise_additional_prompt and timewise_additional_prompt.strip():
            extras.append(timewise_additional_prompt.strip())
        if next_k_input_data and next_k_input_data.strip():
            extras.append(next_k_input_data.strip())
        if task_additional_description and task_additional_description.strip():
            extras.append(task_additional_description.strip())
        extras_block = "\n".join(extras)
    
        if phase_info is None:
            phase_info = PromptTemplates.get_phase1_info()

        goals = "\n".join(f"- {g}" for g in phase_info.get("enhancement_goals", []))
        
        phase_instruction_block = (
            f"**CURRENT PHASE CONTEXT**:\n"
            f"- Step: {phase_info['step_num']} ({phase_info['step_name']})\n"
            f"- Goal: {phase_info['step_goal']}\n"
            f"- Objective: {phase_info['step_instruction']}\n"
            f"- Specific Instruction: {phase_info['specific_instruction']}\n"
            f"- Focus Areas:\n{goals}\n{extras_block}"
        )

        criterion = (
            "**Important State Dimensions Performance**:\n"
            f"{json_data}\n\n"
            "**Evaluation Method**:\n"
            f"{predictability_calc}"
        )
        
        step_wise_analysis_part = f"""
You are an analysis agent tasked with improving communication strategies in a multi-agent reinforcement learning (MARL) system.
**Context**:
{I_T}

### STEP-WISE ANALYSIS INSTRUCTION

1. **Step Information & Guidelines**:
Conduct your analysis based on the objectives below.
{phase_instruction_block}
{phase_info['analysis_logic']}

2. **Previous Protocol Under Analysis**:
{previous_comm_protocol}

3. Performance Data Analysis**:
Analyze the discriminator results below based on the 'Guidelines' provided.
=========================================================
**Criterion**:
{criterion}
"""

        feedback_generation_part = f"""
### FEEDBACK GENERATION INSTRUCTION

Based on your analysis, generate structured feedback. Treat discriminator or predictability results as evidence for possible information bottlenecks, not as a command to reconstruct the full state.

**Expected Output Format (JSON)**:
Strictly output a single JSON object. Do not include markdown formatting (```json ... ```) outside the object if possible, or ensure it is clean.
{{
  "Evaluation": "Synthesize your analysis results. Explicitly mention task-decision bottlenecks and any diagnostic predictability gaps using the Step {phase_info['step_num']} analysis method.",
  "Missing_Information_Hypothesis": "Hypothesis about what feasible sender-observed facts are missing for which receivers, and why those facts affect action selection or team return.",
  "Improvement_Suggestions": "Specific, actionable suggestions to modify message content and communication_matrix when/who edges. Each suggestion should satisfy sender feasibility, receiver necessity, task-decision relevance, and compactness."
}}
"""
        return step_wise_analysis_part + feedback_generation_part

    @staticmethod 
    def get_protocol_update_prompt(task_description, detail_content, obs_shape, obs_dim_desc, 
                                   indexing_example, message_concat_axis, timestep_additional_prompt, 
                                   task_additional_prompt, additional_msg_prompt, feedback):

        I_T = PromptTemplates._get_description_I_T(task_description, obs_shape, obs_dim_desc, detail_content)
        I_P = PromptTemplates._get_instruction_I_P(obs_shape, indexing_example, additional_msg_prompt)
        
        return f"""
You are a communication design agent for Multi-Agent Reinforcement Learning (MARL).
Your goal is to design a task-specific communication protocol that allows agents to share only essential and non-redundant information to enhance decentralized coordination and decision-making.
Based on the task description and observation dimensions, identify feasible sender-observed facts that receivers need for action selection. Do not optimize for full state reconstruction.

=========================================================
[PART 1] Task Description (I_T)
=========================================================

{I_T}

=========================================================
[PART 2] Protocol Design Instruction (I_P)
=========================================================

{I_P}

=========================================================
[PART 3] Feedback & Protocol Update Instruction
=========================================================
Here is the feedback from the previous communication protocol evaluation:
{feedback}

**Protocol Update Strategy**:
1. **Reflect Feedback**: Analyze the performance gaps identified above.
2. **Complement, Do Not Repeat**: The new message will be **concatenated** with the previous one.
   - **Constraint**: Do NOT include information that is already shared by the previous protocol.
   - **Action**: Design new message fields that provide **missing** or **refined** decision facts (e.g., if 'Location' is already shared, add 'Velocity' or 'Intent' only when it changes receiver decisions).
3. **Design New Message**: Create a protocol that strictly extracts these complementary features from the local observation.
4. **Update When/Who**: Ensure `communication_matrix(o)` marks only sender-receiver edges that are necessary for the certified task facts.

{timestep_additional_prompt}
{task_additional_prompt}

Let's think step by step. Below is an illustrative example of the expected output:

```python
import torch as th

def message_design_instruction():
    # Your message design instruction goes here
    return message_description

def communication(o):
    # input : {obs_shape}
    # Your communication implementation goes here
    # use same device as input to avoid CUDA/CPU mismatch
    # {message_concat_axis}
    # Strict Rule : Only concatenate new, non-overlapping fields into each agent’s observation; exclude any information already included in the previous protocol.
    return messages_o 

def communication_matrix(o):
    # Return teacher when/who matrix: [batch, receiver_agent, sender_agent].
    return matrix
```
"""
    
    @staticmethod
    def get_error_augmentation_prompt(base_prompt, attempt, stage, exc, short_tb):
        return (
            f"{base_prompt}\n\n"
            f"---\n"
            f"[Retry context] Previous attempt #{attempt} FAILED\n"
            f"Stage: {stage}\n"
            f"Exception: {type(exc).__name__}\n"
            f"Details (last lines):\n```\n{short_tb}\n```\n"
            "Please fix the issue above. Output ONLY a single Python fenced block:\n"
            "```python\n# your fixed code\n```\n"
            "Requirements: provide functions `communication(o)`, `communication_matrix(o)`, and `message_design_instruction()`; "
            "no trainable params; respect the required tensor shapes; avoid for-loops over batch/time dims."
        )
