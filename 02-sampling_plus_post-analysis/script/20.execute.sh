#!/bin/bash
rm -r 20-cluster
python3 20.holo_pocket_lig.py
mkdir 20-cluster
cp ./20.cluster.in ./20.gen-lig-parm.in 20-cluster
cd 20-cluster
tleap -s -f 20.gen-lig-parm.in
cpptraj -i 20.cluster.in