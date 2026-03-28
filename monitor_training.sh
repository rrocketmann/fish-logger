#!/bin/bash
# Monitor training progress in real-time

echo "🔍 Monitoring Fish AI Training..."
echo "Press Ctrl+C to stop monitoring (training will continue)"
echo "========================================================"
echo ""

# Check if training is running
if ! ps aux | grep "python train.py" | grep -v grep > /dev/null; then
    echo "⚠️  No training process found"
    echo "Start training with: python train.py --epochs 20"
    exit 1
fi

# Show live training log
tail -f training.log
