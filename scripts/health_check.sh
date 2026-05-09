#!/bin/bash
if systemctl is-active --quiet isc-bot; then
    echo "ISC Bot is running."
    exit 0
else
    echo "ISC Bot is NOT running."
    exit 1
fi
