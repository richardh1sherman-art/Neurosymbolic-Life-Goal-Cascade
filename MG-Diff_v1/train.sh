model=$1
dataset=$2
attr=$3
t_len=$4
pretrain=$5
config=$6
batch=$7
gpu_ids=$8
seed=$9

for ((i=0; i<=0; i++))
do
# 🚨 FIXED: Explicitly calling the absolute virtual environment path instead of the raw keyword
/home/rsherman/projects/SMT-ILP/smt-ilp-env/bin/python3.12 train.py --model ${model}\
  --dataset_mode ${dataset}\
  --pred_attr ${attr}\
  --enable_val\
  --gpu_ids ${gpu_ids}\
  --config ${config}\
  --pretrain ${pretrain}\
  --save_best\
  --t_len ${t_len}\
  --seed $((${seed}+${i}))\
  --eval_epoch_freq 5\
  --num_train_target 3\
  --num_threads 4\
  --batch_size ${batch}
done
