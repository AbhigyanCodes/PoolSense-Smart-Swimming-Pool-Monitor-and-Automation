#!/bin/bash
TS=$(date +%Y%m%d_%H%M%S)
DEST="exports/sensor_log_$TS.csv"
mkdir -p exports
cp logs/sensor_log.csv "$DEST"
echo "Exported to $DEST"
