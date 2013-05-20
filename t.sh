#!/bin/bash

for file in $(ls unittests)
do
  echo "Running $file..."
  python3 ./unittests/$file
  echo ''
done

