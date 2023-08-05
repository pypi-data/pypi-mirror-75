#!/bin/sh

# run benchmark for all tasks
for entry in config/task/*
do
  task="$(echo $entry | cut -d'/' -f3)" # cut: /config/task/example.yaml -> example.yaml
  task="$(echo $task | cut -d'.' -f1)"  # cut: example.yaml -> example
  echo "Benchmark:" $task
  python -B benchmark.py task=$task
done