#!/bin/bash
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
bash $SCRIPT_DIR/can_activate.sh can_left 1000000 "3-1.1.3:1.0"
bash $SCRIPT_DIR/can_activate.sh can_right 1000000 "1-1.1.3:1.0"
