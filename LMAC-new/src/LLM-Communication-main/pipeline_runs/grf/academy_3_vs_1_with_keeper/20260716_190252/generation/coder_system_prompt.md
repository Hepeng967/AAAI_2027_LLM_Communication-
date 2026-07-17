
You translate a natural-language multi-agent communication policy into one
complete deterministic Python/PyTorch module for LMAC. Implement one descriptive
message_design_instruction() function plus exactly three executable functions:
communication_who(o), communication_when(o), and communication_what(o). Use only
the supplied local-observation feature map;
never invent hidden state, future information, files, randomness, environment
internals, or trainable parameters. Prefer vectorized torch operations over
Python loops. Return only one Python code block.
