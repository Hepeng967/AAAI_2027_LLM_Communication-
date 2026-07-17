
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
      "decision": "Roach selects an enemy reaper as target and moves to attack it.",
      "locally_missing_information": [
        "Existence and positions (relative x, y) of enemy reapers across the pit.",
        "Health of each visible reaper to prioritize low-health targets."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "overseer (agent type 'overseer')",
      "role_basis": "The overseer is a flying unit with unobstructed vision across the central pit, as per map description. Its observation includes enemy_*_available=1 for reapers on the other side."
    },
    {
      "group_id": "G2",
      "members": "both roaches (agent type 'roach')",
      "role_basis": "Roaches are ground units whose direct vision is blocked by the pit; their enemy_*_available features are 0 for enemies across the pit. They must rely on communication to locate enemies."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Positions (relative x, y) and health of enemy reapers located across the pit.",
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
          "name": "enemy_0_distance",
          "index": 5
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
          "name": "enemy_0_health",
          "index": 8
        },
        {
          "name": "enemy_1_available",
          "index": 11
        },
        {
          "name": "enemy_1_distance",
          "index": 12
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
          "name": "enemy_1_health",
          "index": 15
        },
        {
          "name": "enemy_2_available",
          "index": 18
        },
        {
          "name": "enemy_2_distance",
          "index": 19
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
          "name": "enemy_2_health",
          "index": 22
        },
        {
          "name": "enemy_3_available",
          "index": 25
        },
        {
          "name": "enemy_3_distance",
          "index": 26
        },
        {
          "name": "enemy_3_rel_x",
          "index": 27
        },
        {
          "name": "enemy_3_rel_y",
          "index": 28
        },
        {
          "name": "enemy_3_health",
          "index": 29
        }
      ],
      "receiver_need_hypothesis": "Roaches need to locate enemies to navigate around the pit and initiate attacks. Health information allows prioritizing wounded enemies to secure kills.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Whether all four reapers are simultaneously visible to the overseer; some may be out of sight range or behind cover.",
        "Enemy reapers may move after the overseer's observation, causing communicated positions to become outdated.",
        "Roaches must integrate enemy positions with their own movement constraints (pit navigation) to successfully engage."
      ]
    }
  ],
  "unsupported_assumptions": [
    "The overseer has uninterrupted line-of-sight to all reapers on the opposite side of the pit.",
    "Communicated coordinates are transmitted without delay or loss.",
    "Roaches can interpret relative coordinates directly into movement actions without additional path planning information beyond their local move_* indicators.",
    "Roaches do not require explicit coordination of target assignment (focus fire) beyond enemy position information."
  ]
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
