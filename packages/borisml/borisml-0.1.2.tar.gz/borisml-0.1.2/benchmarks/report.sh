#!/bin/sh

# check whether output directory exists
if [ -d "outputs" ]
then
    python -B plot.py
else
    echo 'There is currently no directory "benchmarks/outputs".'
    echo 'Try running benchmarks before creating the reports.'
fi