
Task and aligned observation description:
The map is 1o_2r_vs_4r. There is a large pit in the center of the map, dividing the battlefield into two sides. At the beginning of each episode, the Overseer and 2 Roaches spawn on one side, while 4 Reapers spawn on the other. The pit blocks direct movement and vision, so Roaches must rely on communication from the Overseer to locate and attack the Reapers. This scenario tests communication and coordination under significant terrain constraints.Observation information for map '1o_2r_vs_4r':
- Each agent observes a vector of length 49.
- There are 3 agents. Their types are: overseer, roach, roach.
- Each row of the observation corresponds to agent_id: [0, 1, 2], and their types: ['overseer', 'roach', 'roach'].
- The observation vector is composed as follows (index: feature):
    - 0: move_north
    - 1: move_south
    - 2: move_east
    - 3: move_west
    - 4: enemy_0_available
    - 5: enemy_0_distance
    - 6: enemy_0_rel_x
    - 7: enemy_0_rel_y
    - 8: enemy_0_health
    - 9: enemy_0_type_0
    - 10: enemy_0_type_1
    - 11: enemy_1_available
    - 12: enemy_1_distance
    - 13: enemy_1_rel_x
    - 14: enemy_1_rel_y
    - 15: enemy_1_health
    - 16: enemy_1_type_0
    - 17: enemy_1_type_1
    - 18: enemy_2_available
    - 19: enemy_2_distance
    - 20: enemy_2_rel_x
    - 21: enemy_2_rel_y
    - 22: enemy_2_health
    - 23: enemy_2_type_0
    - 24: enemy_2_type_1
    - 25: enemy_3_available
    - 26: enemy_3_distance
    - 27: enemy_3_rel_x
    - 28: enemy_3_rel_y
    - 29: enemy_3_health
    - 30: enemy_3_type_0
    - 31: enemy_3_type_1
    - 32: ally_0_visible
    - 33: ally_0_distance
    - 34: ally_0_rel_x
    - 35: ally_0_rel_y
    - 36: ally_0_health
    - 37: ally_0_type_0
    - 38: ally_0_type_1
    - 39: ally_1_visible
    - 40: ally_1_distance
    - 41: ally_1_rel_x
    - 42: ally_1_rel_y
    - 43: ally_1_health
    - 44: ally_1_type_0
    - 45: ally_1_type_1
    - 46: own_health
    - 47: own_type_0
    - 48: own_type_1

LMAC rollout observation alignment:
- Runtime LMAC observation vector length: 49.
- Documented SMAC observation vector length: 49.
- Rollout available: False from /data/hp/LLM_Communication/LMAC-new/data.
- Use runtime obs_shape for generated code and tests.
- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.


Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Roach selects a movement direction to approach and attack a Reaper.",
      "locally_missing_information": [
        "Availability of enemy Reapers (which are alive)",
        "Relative position of each enemy Reaper to the deciding Roach",
        "Health of each enemy Reaper to allow low-health targeting"
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach selects which enemy to attack when multiple are reachable.",
      "locally_missing_information": [
        "Which enemies are already being focused by the other Roach",
        "Current health of each enemy to estimate time-to-kill and avoid overkill"
      ]
    },
    {
      "decision_id": "D3",
      "decision": "Overseer decides which enemy-related information to prioritize in communication (e.g., closest enemy, all enemies, a target command).",
      "locally_missing_information": [
        "Exact positions of both Roaches to frame relative directions",
        "Whether Roaches need absolute or own-frame-relative coordinates for navigation"
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "agent_0 (overseer)",
      "role_basis": "Only agent with vision across the central pit; enemy features are observable (enemy_*_available = 1 for Reapers). Task description explicitly states Roaches must rely on Overseer communication."
    },
    {
      "group_id": "G2",
      "members": "agent_1 (roach), agent_2 (roach)",
      "role_basis": "Ground attackers that cannot see enemies across the pit (enemy_*_available = 0). Need externally sourced enemy information to move and attack. They can observe each other and the Overseer if within ally-observation range."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Positions of alive enemy Reapers relative to the receiving Roach.",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "enemy_0_available",
          "index": 4
        },
        {
          "name": "enemy_0_rel_x",
          "index": 6
        },
        {
          "name": "enemy_0_rel_y",
          "index": 7
        },
        {
          "name": "enemy_1_available",
          "index": 11
        },
        {
          "name": "enemy_1_rel_x",
          "index": 13
        },
        {
          "name": "enemy_1_rel_y",
          "index": 14
        },
        {
          "name": "enemy_2_available",
          "index": 18
        },
        {
          "name": "enemy_2_rel_x",
          "index": 20
        },
        {
          "name": "enemy_2_rel_y",
          "index": 21
        },
        {
          "name": "enemy_3_available",
          "index": 25
        },
        {
          "name": "enemy_3_rel_x",
          "index": 27
        },
        {
          "name": "enemy_3_rel_y",
          "index": 28
        }
      ],
      "receiver_need_hypothesis": "Without enemy positions Roaches cannot move toward any enemy. They require these coordinates updated every timestep to react to enemy movement. The relative nature (to Overseer) can be transformed if the Roach also knows the Overseer's relative position via ally observations.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Coordinate transformation may be non-trivial when both agents are moving.",
        "No unique enemy ID exists; the order of enemies in observation may change between steps, breaking simple index-based communication.",
        "Bandwidth may force partial information, risking omission of some enemies."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Health of each alive enemy Reaper to allow focus-fire decisions.",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "enemy_0_health",
          "index": 8
        },
        {
          "name": "enemy_1_health",
          "index": 15
        },
        {
          "name": "enemy_2_health",
          "index": 22
        },
        {
          "name": "enemy_3_health",
          "index": 29
        }
      ],
      "receiver_need_hypothesis": "Roaches can avoid wasteful overkill and choose the weakest target if health information is shared. This improves team damage efficiency.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Health alone may be insufficient if enemy identities cannot be tracked across messages.",
        "Delay in communication may render health stale if enemies are damaged by Roach attacks in the meantime."
      ]
    },
    {
      "requirement_id": "IR3",
      "fact": "Which enemy each Roach is currently targeting or moving toward.",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "ally_0_visible",
          "index": 32
        },
        {
          "name": "ally_0_rel_x",
          "index": 34
        },
        {
          "name": "ally_0_rel_y",
          "index": 35
        },
        {
          "name": "ally_1_visible",
          "index": 39
        },
        {
          "name": "ally_1_rel_x",
          "index": 41
        },
        {
          "name": "ally_1_rel_y",
          "index": 42
        }
      ],
      "receiver_need_hypothesis": "If each Roach knows the other's intended target, they can split targets efficiently. Direct observation of ally positions is possible, but intention is not directly observed, so communication of target index or vector is needed.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Roaches might infer ally actions from movement without explicit messages, reducing need for this IR.",
        "If only one enemy is alive or reachable, this IR becomes irrelevant."
      ]
    }
  ],
  "unsupported_assumptions": []
}

Return this policy schema:
{
  "policy_hypothesis":"...",
  "agent_groups":[...],
  "rules":[
    {"rule_id":"R1","requirement_ids":["IR1"],
      "who":{"sender_group":"G1","receiver_selector":"...","observable_basis":[]},
      "when":{"feature_names":["..."],"feature_indices":[0],"operator":"...",
        "threshold":0.0,"threshold_basis":{"type":"binary_semantics|documented_semantics|rollout_distribution|relative_comparison|llm_hypothesis","evidence":"..."}},
      "what":{"feature_names":["..."],"feature_indices":[0]},
      "sender_feasibility":"...","receiver_necessity":"...",
      "expected_rollout_behavior":"...","uncertainties":[]}
  ],
  "default_behavior":"no communication",
  "design_tradeoffs":"..."
}
Feature indices must match the supplied aligned schema. Do not invent runtime
fields. A threshold without a documented or observed basis must be explicitly
labelled llm_hypothesis. Prefer no communication only as a default, not as a
hard-coded claim that sparse communication is always superior.
