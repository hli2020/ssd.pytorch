#!/bin/bash

start=`date +%s`

# train and test
# from 'cifar_base_104_no_relu.sh'
CUDA_VISIBLE_DEVICES=0 python holly_cifar.py \
--experiment_name=cifar_base_104_KL \
--dataset=cifar \
--model_cifar=capsule \
--epochs=300 \
--use_KL \
--KL_manner=1 \
--KL_factor=.1 \
--schedule_cifar 150 225 \
--lr=0.01 \
--deploy

end=`date +%s`
runtime=$((end-start))

echo "Completed in" $runtime "seconds"
