#!/bin/bash

sh 13-prep-parellel.sh
bsub < 13para-0-50.bsub
sleep 30
bsub < 13para-51-99.bsub
sleep 30
bsub < 13para-100-150.bsub
sleep 30
bsub < 13para-151-199.bsub
sleep 30
bsub < 13para-200-250.bsub
sleep 30
bsub < 13para-251-299.bsub
sleep 30
bsub < 13para-300-350.bsub
sleep 30
bsub < 13para-351-399.bsub
sleep 30
bsub < 13para-400-450.bsub
sleep 30
bsub < 13para-451-499.bsub