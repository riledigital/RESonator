#!/bin/bash

set -e
docker run  -t -d -p 8085:8085 -v "$(pwd)":/app resonator
