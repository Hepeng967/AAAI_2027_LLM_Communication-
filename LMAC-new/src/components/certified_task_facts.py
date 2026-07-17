REQUIRED_TASK_FACTS = {
    "1o_10b_vs_1r": [
        {
            "fact": "enemy_position",
            "sender": 10,
            "fields": [6, 7],
            "receivers": list(range(10)),
            "feasibility": "Overseer observes enemy position while Banelings need it for target approach.",
            "necessity": "Banelings have limited local sight; the Overseer-to-Baneling edge resolves decentralized target localization.",
            "decision_relevance": "Enemy position changes movement and attack timing for Banelings.",
        },
        {
            "fact": "enemy_last_action",
            "sender": 10,
            "fields": list(range(85, 92)),
            "receivers": list(range(10)),
            "feasibility": "Overseer observation includes the enemy last-action slice.",
            "necessity": "Banelings cannot infer full enemy action history from their local observation alone.",
            "decision_relevance": "Enemy action intent affects whether Banelings should close distance or wait.",
        },
    ],
    "1o_2r_vs_4r": [
        {
            "fact": "ally_health",
            "sender": 0,
            "fields": [50],
            "receivers": [1, 2],
            "feasibility": "The reporting unit observes its own health field.",
            "necessity": "Other agents need team health to coordinate focus fire and avoid over-committing wounded allies.",
            "decision_relevance": "Ally health changes retreat, cover, and attack allocation decisions.",
        },
        {
            "fact": "enemy_position_health",
            "sender": 0,
            "fields": [6, 7, 8],
            "receivers": [1, 2],
            "feasibility": "The sender observes enemy relative position and health fields.",
            "necessity": "Receivers may not observe the same enemy state under partial observability.",
            "decision_relevance": "Enemy position and health determine target selection and movement.",
        },
    ],
    "5z_vs_1ul": [
        {
            "fact": "ultralisk_visibility_position",
            "sender": 0,
            "fields": [4, 5, 6],
            "receivers": [1, 2, 3, 4],
            "feasibility": "The sender observes Ultralisk visibility and relative position.",
            "necessity": "Other Zealots need shared target localization to maintain surround and avoid isolated attacks.",
            "decision_relevance": "Ultralisk position changes chase, surround, and retreat choices.",
        },
        {
            "fact": "health_and_attack_intent",
            "sender": 0,
            "fields": [34, 42],
            "receivers": [1, 2, 3, 4],
            "feasibility": "The sender observes the relevant health and attack-intent fields.",
            "necessity": "Receivers need team and intent context to coordinate focus and disengagement.",
            "decision_relevance": "Health and attack intent alter whether agents trade damage or reposition.",
        },
    ],
}


TASK_PROBES = {
    "1o_10b_vs_1r": [
        {
            "name": "overseer_enemy_position_to_banelings",
            "sender": 10,
            "fields": [6, 7],
            "receivers": list(range(10)),
            "fact": "enemy_position",
        },
        {
            "name": "overseer_last_action_to_banelings",
            "sender": 10,
            "fields": list(range(85, 92)),
            "receivers": list(range(10)),
            "fact": "enemy_last_action",
        },
    ],
    "1o_2r_vs_4r": [
        {
            "name": "ally_health_broadcast",
            "sender": 0,
            "fields": [50],
            "receivers": [1, 2],
            "fact": "ally_health",
        },
        {
            "name": "enemy_position_health_broadcast",
            "sender": 0,
            "fields": [6, 7, 8],
            "receivers": [1, 2],
            "fact": "enemy_position_health",
        },
    ],
    "5z_vs_1ul": [
        {
            "name": "ultralisk_position_broadcast",
            "sender": 0,
            "fields": [4, 5, 6],
            "receivers": [1, 2, 3, 4],
            "fact": "ultralisk_visibility_position",
        },
        {
            "name": "health_and_attack_intent_broadcast",
            "sender": 0,
            "fields": [34, 42],
            "receivers": [1, 2, 3, 4],
            "fact": "health_and_attack_intent",
        },
    ],
}


BASE_MAP_SPECS = {
    "1o_10b_vs_1r": {
        "n_agents": 11,
        "obs_dim": 103,
        "time_seq": 10,
        "expected_sender_rate": 10 / (11 * 10),
        "critical_receivers": list(range(10)),
        "critical_senders": [10],
    },
    "1o_2r_vs_4r": {
        "n_agents": 3,
        "obs_dim": 66,
        "time_seq": 10,
    },
    "5z_vs_1ul": {
        "n_agents": 5,
        "obs_dim": 48,
        "time_seq": 10,
    },
    "protoss_10_vs_10": {
        "environment": "smacv2", "n_agents": 10, "n_enemies": 10,
        "obs_dim": 208, "documented_raw_obs_dim": 182, "time_seq": 10,
        "dynamic_agent_roles": True,
        "possible_unit_types": ["stalker", "zealot", "colossus"],
        "agent_id_role_warning": "Agent ID does not identify a fixed unit type across episodes.",
    },
    "terran_10_vs_10": {
        "environment": "smacv2", "n_agents": 10, "n_enemies": 10,
        "obs_dim": 188, "documented_raw_obs_dim": 162, "time_seq": 10,
        "dynamic_agent_roles": True,
        "possible_unit_types": ["marine", "marauder", "medivac"],
        "agent_id_role_warning": "Agent ID does not identify a fixed unit type across episodes.",
    },
    "zerg_10_vs_10": {
        "environment": "smacv2", "n_agents": 10, "n_enemies": 10,
        "obs_dim": 188, "documented_raw_obs_dim": 162, "time_seq": 10,
        "dynamic_agent_roles": True,
        "possible_unit_types": ["zergling", "hydralisk", "baneling"],
        "agent_id_role_warning": "Agent ID does not identify a fixed unit type across episodes.",
    },
    "hallway": {
        "environment": "hallway", "n_agents": 4, "n_actions": 3,
        "obs_dim": 8, "documented_raw_obs_dim": 1, "time_seq": 10,
        "state_numbers": [4, 6, 8, 10],
        "objective": "All four agents must reach position 0 on the same timestep.",
        "failure_condition": "The episode fails if only a subset reaches position 0.",
        "actions": {0: "stay", 1: "toward_zero", 2: "away_from_zero"},
        "raw_features": {"current_position": [0, 1]},
    },
    "hallway_group": {
        "environment": "hallway_group", "n_agents": 7, "n_actions": 3,
        "obs_dim": 12, "documented_raw_obs_dim": 2, "time_seq": 10,
        "n_groups": 2, "group_ids": [0, 0, 0, 1, 1, 1, 1],
        "state_numbers": [3, 5, 7, 4, 6, 8, 10],
        "objective": "Each group must reach position 0 synchronously, and different groups must finish in separate rounds.",
        "failure_condition": "Partial group arrival fails that group; simultaneous completion by multiple groups is rolled back and penalized.",
        "actions": {0: "stay", 1: "toward_zero", 2: "away_from_zero"},
        "raw_features": {"current_position": [0, 1], "active_status": [1, 2]},
    },
    "academy_3_vs_1_with_keeper": {
        "environment": "grf", "n_agents": 3, "n_enemies": 2, "n_actions": 19,
        "obs_dim": 48, "documented_raw_obs_dim": 26, "time_seq": 10,
        "objective": "Three attackers coordinate positioning and passes to score against one field defender and a goalkeeper.",
        "raw_feature_semantics": "ego position/direction, teammate relative positions/directions, opponent relative positions/directions, and ball relative position/direction",
    },
    "academy_run_pass_and_shoot_with_keeper": {
        "environment": "grf", "n_agents": 2, "n_enemies": 2, "n_actions": 19,
        "obs_dim": 43, "documented_raw_obs_dim": 22, "time_seq": 10,
        "objective": "Two attackers coordinate a run-pass-and-shoot sequence against one field defender and a goalkeeper.",
        "raw_feature_semantics": "ego position/direction, teammate relative position/direction, opponent relative positions/directions, and ball relative position/direction",
    },
}


def certified_task_fact_edges(map_name):
    edges = []
    seen = set()
    for fact in REQUIRED_TASK_FACTS.get(map_name, []):
        sender = fact["sender"]
        for receiver in fact["receivers"]:
            edge = (receiver, sender)
            if edge not in seen:
                edges.append(edge)
                seen.add(edge)
    return edges


CERTIFIED_TASK_FACT_EDGES = {
    map_name: certified_task_fact_edges(map_name)
    for map_name in REQUIRED_TASK_FACTS
}


def map_specs():
    specs = {}
    for map_name, base in BASE_MAP_SPECS.items():
        spec = dict(base)
        spec["task_probes"] = TASK_PROBES.get(map_name, [])
        spec["required_task_facts"] = REQUIRED_TASK_FACTS.get(map_name, [])
        specs[map_name] = spec
    return specs
