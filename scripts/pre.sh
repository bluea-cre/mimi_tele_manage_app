#!/bin/bash

# Copy the functions to prepare the environment
mkdir -p build/run/
mkdir -p build/bin/without_terminal/
mkdir -p build/bin/with_terminal/

cp -rp archive/functions build/run/
cp -rp archive/functions build/bin/without_terminal/
cp -rp archive/functions build/bin/with_terminal/
