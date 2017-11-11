#!/bin/bash

start=`date +%s`

# train and test
CUDA_VISIBLE_DEVICES=2 python holly_cifar.py \
--experiment_name=cifar_base_104_no_relu_spead_rmsprop \
--dataset=cifar10 \
--model_cifar=capsule \
--epochs=300 \
--optim=rmsprop \
--schedule_cifar 150 225 \
--lr=0.0001 \
--use_spread_loss \
--deploy

end=`date +%s`
runtime=$((end-start))

echo "Completed in" $runtime "seconds"