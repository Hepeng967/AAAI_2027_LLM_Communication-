#!/bin/bash

export TZ="Asia/Shanghai"  # 设置时区为北京时间

# 自定义 config 和地图列表
CONFIG="gacg"
ENVS=(
  # "sc2_v2_terran"
  "sc2_v2_protoss"
  # "sc2_v2_zerg"
)


# 最大并行进程数
MAX_PROCESSES=5

# 创建日志目录
LOG_DIR="log"
mkdir -p $LOG_DIR

# 日志文件，用于监控实验进度
LOG_FILE="$LOG_DIR/$CONFIG/experiment_progress.log"
echo "实验开始时间: $(date +"%Y-%m-%d %H:%M:%S")" >> $LOG_FILE  # 使用北京时间

# 使用队列的方式循环每个地图，每个地图跑五遍
total_iterations=$((${#ENVS[@]} * 5))
current_iteration=0

# 记录已启动的进程
running_pids=()

while [ $current_iteration -lt $total_iterations ]; do
  # 启动新的实验进程直到达到最大并行进程数
  while [ ${#running_pids[@]} -lt $MAX_PROCESSES ] && [ $current_iteration -lt $total_iterations ]; do
    # 计算当前要跑的地图和迭代次数
    ENVS_index=$((current_iteration / 5))
    iteration=$((current_iteration % 5 + 1))
    ENVS_NAME=${ENVS[$ENVS_index]}

    # 启动新的实验进程
    echo "Running ENVS: $ENVS_NAME, iteration: $iteration" | tee -a $LOG_FILE
    start_time=$(date +"%Y%m%d_%H%M%S")
    CUDA_VISIBLE_DEVICES=1 nohup python3 src/main.py --config=$CONFIG --env-config=$ENVS_NAME > "$LOG_DIR/${CONFIG}/output_${ENVS_NAME}_iteration_${iteration}.log_${start_time}.log" 2>&1 &

    # 获取刚启动的进程的 PID，并加入正在运行的进程列表
    new_pid=$!
    running_pids+=($new_pid)

    # 更新当前运行的进程计数
    current_iteration=$((current_iteration + 1))
  done

  # 等待最先结束的进程
  wait -n  # 等待至少一个子进程结束

  # 移除已结束的进程 PID
  for pid in "${running_pids[@]}"; do
    if ! kill -0 $pid 2>/dev/null; then
      # 进程已经结束，从列表中移除
      running_pids=(${running_pids[@]/$pid})
      break
    fi
  done
done

# 等待所有进程结束
wait

# 记录实验结束时间
echo "所有实验运行完毕！" | tee -a $LOG_FILE
echo "实验结束时间: $(date +"%Y-%m-%d %H:%M:%S")" >> $LOG_FILE  # 使用北京时间
