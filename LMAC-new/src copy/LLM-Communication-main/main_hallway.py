from api.LLMCoder_hallway import LLMCoder
from api.LLMPlanner_hallway import LLMPlanner
import numpy as np
import os


def pipeline():
    # 与原 main 完全一致，避免任何副作用
    os.popen('rm -rf res-*')
    os.popen('rm -rf *.log')

    planner = LLMPlanner()
    coder = LLMCoder()

    print('---------------------Planning (Hallway)---------------------')
    com_tactics = planner.plan()

    print("\n===== LLM Communication Policy =====\n")
    print(com_tactics)

    print('\n---------------------Generating Communication Mask Function---------------------')
    mask_func = coder.generate_mask(
        com_tactics,
        mode='object_content'
    )

    if callable(mask_func):
        # 仍然使用 coder 内部定义的 n_agents / obs_dim
        n_agents = coder.n_agents
        obs_dim = coder.obs_dim
        bs = 2

        # 与原 main 保持一致，不引入任何 hallway 假设
        obs = np.random.rand(bs, n_agents, n_agents, obs_dim)

        mask = mask_func(obs, mode='object_content')

        print("\n===== Communication Mask =====\n")
        print(mask)
    else:
        print("[Error] LLM未能正确生成通信mask函数，原始输出如下：")
        print(mask_func)


if __name__ == '__main__':
    pipeline()
