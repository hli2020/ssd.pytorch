#!/bin/bash

start=`date +%s`

# train and test
# '--test_batch=32' has to be small on cifar100
CUDA_VISIBLE_DEVICES=5 python holly_cifar.py \
--experiment_name=cifar_base_104_no_relu_multi_crop_fmnist \
--dataset=fmnist \
--model_cifar=capsule \
--epochs=300 \
--schedule_cifar 150 225 \
--lr=0.01 \
--route_num=4 \
--train_batch=128 \
--test_batch=128 \
--w_version=v2 \
--multi_crop_test \
--deploy

end=`date +%s`
runtime=$((end-start))

echo "Completed in" $runtime "seconds"
