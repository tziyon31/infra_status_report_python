# infra_status_report_script_python

A lightweight Python tool for checking service availability (via ping or HTTP) and generating a simple HTML status report.

## Features

- Supports both network-level (`ping`) and application-level (`HTTP GET`) checks
- Generates a self-contained HTML report
- Easily configurable list of targets

## Technologies Used

- Python 3
- `requests`, `subprocess`, `os`

## Motivation

In small-scale environments or lab setups, it's often useful to have a quick tool to monitor service status without setting up full observability stacks.  
This project shows practical scripting and basic diagnostic automation with minimal overhead.

## How to Run

```bash
python status_check.py
