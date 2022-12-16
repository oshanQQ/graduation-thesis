#!/bin/sh

for i in `seq 1 $1`
do
  python train.py
done
