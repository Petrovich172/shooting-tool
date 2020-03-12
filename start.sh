#!/bin/bash
#echo "Preparing dependencies"
#python main.py

echo "Starting tank"
cd ..
yandex-tank -c load.yaml
exit 0