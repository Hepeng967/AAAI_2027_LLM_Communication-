import json
import os
import glob
import pickle
from configs.map_config import MapConfig
from env_adapters import get_adapter, normalize_environment

comm_info_base_dir = 'knowledge_data/communication_info/'
unit_info_base_dir = 'knowledge_data/firecrawl_test/sc2_unit_info/'
def process_info(unit_name):
    if unit_name == 'overseer':
        unit_name = 'observer'
    with open(f'{unit_info_base_dir}{unit_name}.json', 'r') as reader:
        info_json = json.load(reader)
    info_needed = {}
    info_needed['Unit'] = unit_name
    #info_needed['Type'] = info_json['Type']
    #info_needed['Description'] = info_json['Description']
    info_needed['Attack'] = info_json['Attack']
    info_needed['Unit stats'] = info_json['Unit stats']
    #info_needed['Strong against'] = info_json['Strong against']
    #info_needed['Weak against'] = info_json['Weak against']
    #info_needed["Competitive Usage"] = info_json["Competitive Usage"]

    return str(info_needed)

def process_obs_info(map_name):
    environment = normalize_environment(os.environ.get("LLM_COMM_ENV", "smac"))
    if environment != "smac":
        return get_adapter(environment).documented_obs_info(map_name)
    if map_name in ["hallway", "4rooms", "hallway_4rooms"]:
        # hallway环境固定配置
        obs_info = {
            'map_name': map_name,
            'obs_shape': 2,  # 固定为2维
            'n_agents': 2,   # 默认2个智能体，与论文一致
            'obs_feature_names': [
                'current_state',    # 当前位置/状态 (0 = goal)
                'active_status'     # 是否活跃 (1.0=active, 0.0=inactive)
            ],
            'feature_index': {
                'current_state': [0, 1],
                'active_status': [1, 2]
            },
            'obs_agent_id_map': ['agent_0', 'agent_1'],
            'obs_agent_type_map': ['standard_agent', 'standard_agent']
        }
        return obs_info
    else:
        # 原有的SMAC配置逻辑
        with open(f'{comm_info_base_dir}{map_name}.json', 'r') as reader:
            info_json = json.load(reader)
        obs_info = {
            'map_name': map_name,
            'obs_shape': info_json['obs_shape'],
            'n_agents': info_json['n_agents'],
            'obs_feature_names': info_json['obs_feature_names'],
            'feature_index': info_json['feature_index'],
            'obs_agent_id_map': info_json['obs_agent_id_map'],
            'obs_agent_type_map': info_json['obs_agent_type_map'],
        }
        return obs_info

def obs_info_to_prompt(obs_info):
    # 为hallway环境优化提示词
    if obs_info['map_name'] in ["hallway", "4rooms", "hallway_4rooms"]:
        prompt = f"Hallway Environment - Group Coordination Problem\n"
        prompt += f"- Map: {obs_info['map_name']}\n"
        prompt += f"- Number of agents: {obs_info['n_agents']}\n"
        prompt += f"- Observation vector length: {obs_info['obs_shape']}\n"
        prompt += f"- Observation features:\n"
        prompt += f"  - current_state (index 0): Agent's current position state (0 means goal position)\n"
        prompt += f"  - active_status (index 1): Whether agent is active (1.0=active, 0.0=inactive)\n"
        prompt += f"- Task: Agents must coordinate to reach state 0 simultaneously within their group\n"
        prompt += f"- Communication: Agents can send messages to coordinate arrival timing\n"
        return prompt
    else:
        # 原有的SMAC提示词
        prompt = f"Observation information for map '{obs_info['map_name']}':\n"
        prompt += f"- Each agent observes a vector of length {obs_info['obs_shape']}.\n"
        prompt += f"- There are {obs_info['n_agents']} agents. Their types are: {', '.join(obs_info['obs_agent_type_map'])}.\n"
        prompt += f"- Each row of the observation corresponds to agent_id: {obs_info['obs_agent_id_map']}, and their types: {obs_info['obs_agent_type_map']}.\n"
        prompt += f"- The observation vector is composed as follows (index: feature):\n"
        for i, feat in enumerate(obs_info['obs_feature_names']):
            idx_range = obs_info['feature_index'].get(feat, None)
            if idx_range and isinstance(idx_range, list) and len(idx_range) == 2:
                if idx_range[0] == idx_range[1] - 1:
                    prompt += f"    - {idx_range[0]}: {feat}\n"
                else:
                    prompt += f"    - {idx_range[0]}~{idx_range[1]-1}: {feat}\n"
            else:
                prompt += f"    - ?: {feat}\n"
        return prompt

def process_lmac_rollout_obs_info(map_name):
    obs_info = process_obs_info(map_name)
    environment = normalize_environment(os.environ.get("LLM_COMM_ENV", "smac"))
    rollout_root = os.environ.get(
        "LMAC_ROLLOUT_ROOT",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data")),
    )
    rollout_map_root = os.path.join(rollout_root, map_name) if environment == "smac" else os.path.join(rollout_root, environment, map_name)
    files = sorted(glob.glob(os.path.join(rollout_map_root, "train_traj_*.pkl")))
    aligned = dict(obs_info)
    aligned["documented_obs_shape"] = obs_info["obs_shape"]
    aligned["rollout_root"] = rollout_root
    aligned["rollout_files"] = files[:4]
    aligned["rollout_available"] = False
    if environment != "smac":
        # LMAC's lmac.yaml appends previous-action one-hot and agent ID before
        # a rollout exists. Environment adapters provide the static action
        # count so the initial teacher is generated against the exact tensor
        # shape later consumed by the controller.
        static_spec = get_adapter(environment).static_map_spec(map_name)
        aligned["raw_obs_shape"] = int(obs_info["obs_shape"])
        aligned["action_dim"] = int(
            static_spec.get(
                "n_actions",
                6 + int(obs_info.get("n_enemies", obs_info["n_agents"])),
            )
        )
        aligned["obs_shape"] = (
            aligned["raw_obs_shape"] + aligned["action_dim"] + int(obs_info["n_agents"])
        )
    if files:
        try:
            with open(files[0], "rb") as reader:
                data = pickle.load(reader)
            obs = data.get("obs")
            if obs is not None and len(obs.shape) == 4:
                aligned["rollout_available"] = True
                raw_obs_dim = int(obs.shape[-1])
                aligned["n_agents"] = int(obs.shape[-2])
                action = data.get("actions_onehot")
                aligned["action_dim"] = int(action.shape[-1]) if action is not None else None
                aligned["raw_obs_shape"] = raw_obs_dim
                aligned["obs_shape"] = raw_obs_dim + int(aligned["action_dim"] or 0) + aligned["n_agents"]
                if environment == "smacv2" and raw_obs_dim != int(obs_info["obs_shape"]):
                    aligned["schema_mismatch"] = (
                        f"Documented raw obs_dim={obs_info['obs_shape']} but rollout raw obs_dim={raw_obs_dim}. "
                        "Runtime dimension remains authoritative; unknown positions are not assigned invented semantics."
                    )
        except Exception as exc:
            aligned["rollout_error"] = f"{type(exc).__name__}: {exc}"

    feature_index = dict(obs_info.get("feature_index", {}))
    documented_dim = int(obs_info["obs_shape"])
    actual_dim = int(aligned["obs_shape"])
    # smac_plus allocates one additional enemy-health slot per enemy when both
    # obs_all_health and obs_enemy_health are enabled, but writes health only
    # once. For 1o_2r_vs_4r this creates four constant-zero padding slots and
    # shifts all later features relative to the legacy 49-D JSON description.
    if map_name == "1o_2r_vs_4r" and int(aligned.get("raw_obs_shape", 0)) == 53:
        names = ["move_north", "move_south", "move_east", "move_west"]
        runtime_index = {name: [idx, idx + 1] for idx, name in enumerate(names)}
        cursor = 4
        for enemy_id in range(4):
            fields = (
                "available", "distance", "rel_x", "rel_y", "health",
                "type_0", "type_1", "unused_health_padding",
            )
            for field in fields:
                runtime_index[f"enemy_{enemy_id}_{field}"] = [cursor, cursor + 1]
                cursor += 1
        for ally_id in range(2):
            fields = "visible", "distance", "rel_x", "rel_y", "health", "type_0", "type_1"
            for field in fields:
                runtime_index[f"ally_{ally_id}_{field}"] = [cursor, cursor + 1]
                cursor += 1
        for field in ("health", "type_0", "type_1"):
            runtime_index[f"own_{field}"] = [cursor, cursor + 1]
            cursor += 1
        feature_index = runtime_index
        aligned["non_information_raw_indices"] = [11, 19, 27, 35]
        aligned["semantic_raw_obs_dim"] = 49
    described_until = int(aligned.get("raw_obs_shape", documented_dim)) if map_name == "1o_2r_vs_4r" else documented_dim
    for idx in range(described_until, actual_dim):
        raw_dim = int(aligned.get("raw_obs_shape", documented_dim))
        action_dim = int(aligned.get("action_dim") or 0)
        if idx < raw_dim:
            name = f"env_extra_{idx}"
        elif idx < raw_dim + action_dim:
            name = f"previous_action_{idx - raw_dim}"
        else:
            name = f"agent_id_{idx - raw_dim - action_dim}"
        feature_index[name] = [idx, idx + 1]
    aligned["feature_index"] = feature_index
    aligned["obs_feature_names"] = list(obs_info.get("obs_feature_names", [])) + [
        f"lmac_extra_{idx}" for idx in range(documented_dim, actual_dim)
    ]
    aligned["alignment_note"] = (
        "The LMAC policy consumes raw environment observation followed by previous-action "
        "one-hot and agent-id one-hot. For this rollout: environment observation indices "
        f"are [0,{int(aligned.get('raw_obs_shape', documented_dim)) - 1}], previous action "
        f"indices are [{int(aligned.get('raw_obs_shape', documented_dim))},"
        f"{int(aligned.get('raw_obs_shape', documented_dim)) + int(aligned.get('action_dim') or 0) - 1}], "
        f"and agent ID indices are [{int(aligned.get('raw_obs_shape', documented_dim)) + int(aligned.get('action_dim') or 0)},"
        f"{actual_dim - 1}]. WHAT should prioritize environment observations; previous action "
        "or agent ID may only be selected with an explicit coordination justification. "
        "Undocumented env_extra dimensions must not be assigned invented semantics."
    )
    return aligned

def lmac_obs_info_to_prompt(obs_info):
    prompt = obs_info_to_prompt(obs_info)
    if "documented_obs_shape" in obs_info:
        prompt += "\nLMAC rollout observation alignment:\n"
        prompt += f"- Runtime LMAC observation vector length: {obs_info['obs_shape']}.\n"
        prompt += f"- Documented SMAC observation vector length: {obs_info['documented_obs_shape']}.\n"
        prompt += f"- Rollout available: {obs_info.get('rollout_available')} from {obs_info.get('rollout_root')}.\n"
        prompt += "- Use runtime obs_shape for generated code and tests.\n"
        prompt += "- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.\n"
        # The documented feature map was already printed above. Only show
        # dimensions that are genuinely appended at runtime.
        documented_dim = int(obs_info["documented_obs_shape"])
        extra = {
            feat: span for feat, span in obs_info.get("feature_index", {}).items()
            if isinstance(span, list) and len(span) == 2 and int(span[0]) >= documented_dim
        }
        if extra:
            prompt += "- Additional runtime dimensions:\n"
            for feat, idx_range in extra.items():
                prompt += f"    - {idx_range[0]}~{idx_range[1]-1}: {feat}\n"
    return prompt

map_name = os.environ.get("LLM_SMAC_MAP_NAME", "1o_2r_vs_4r")
environment = normalize_environment(os.environ.get("LLM_COMM_ENV", "smac"))

# 根据环境类型构建task_config
if environment != "smac":
    obs_info = process_lmac_rollout_obs_info(map_name)
    task_config = get_adapter(environment).task_prompt(map_name, obs_info)
elif map_name in ["hallway", "4rooms", "hallway_4rooms"]:
    # hallway环境专用配置
    obs_info = process_lmac_rollout_obs_info(map_name)
    task_config = f'''
Hallway Coordination Environment
{lmac_obs_info_to_prompt(obs_info)}
'''
else:
    # 原有的SMAC配置逻辑
    mc = MapConfig().get_map_config(map_name)
    map_config = mc['map_info']
    units = mc['units_info']

    units_info = ''
    for a in set(units):
        units_info += process_info(a) + '\n'

    obs_info = process_lmac_rollout_obs_info(map_name)
    obs_config = lmac_obs_info_to_prompt(obs_info)

    # unit_config = f'''
    # The information of the units are:
    # {units_info}All the units has no abilities such as blinking or equipments.
    # '''

    # task_config = map_config + unit_config + obs_config

    task_config = map_config + obs_config


prefix_code = '''
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race, Difficulty
from sc2.ids.ability_id import AbilityId
from sc2.ids.effect_id import EffectId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units
import math
import random

class MarineBot(BotAI):
'''

post_code = '''
if __name__ == '__main__':
    bot = MarineBot()
    result = run_game(maps.get('{}'), [Bot(Race.Random, bot), Computer(Race.Random, Difficulty.VeryHard)], realtime=False)
    print(result)
    print(bot.state.score.score)
    print(bot.state.score.total_damage_dealt_life)
    print(bot.state.score.total_damage_taken_life)
    print(bot.state.score.total_damage_taken_shields)
    print(len(bot.units))
    print(len(bot.enemy_units)+ len(bot.enemy_structures))
'''.format(map_name)

    
