#!/bin/bash
cd /usr/src/app && /usr/local/bin/python /usr/src/app/scripts/VickyTopiaReportCLI.py --tenableReport >> /var/log/tenable_sync.log 2>&1
