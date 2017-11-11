#!/bin/bash

start=`date +%s`

# train and test
CUDA_VISIBLE_DEVICES=4 python holly_cifar.py \
--experiment_name=capsule_201_adam_N_2 \
--dataset=cifar10 \
--model_cifar=capsule \
--cap_model=v1 \
--cap_N=2 \
--epochs=300 \
--schedule_cifar 150 225 \
--optim=adam \
--lr=0.0001 \
--route_num=4 \
--multi_crop_test \
--deploy

end=`date +%s`
runtime=$((end-start))

echo "Completed in" $runtime "seconds"
