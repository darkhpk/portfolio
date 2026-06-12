# DevOps Automation Suite

A comprehensive collection of automation scripts for DevOps tasks including deployment automation, server monitoring, backup management, and CI/CD pipeline utilities.

## Features

- **Deployment Automation**: Automated deployment scripts for various platforms
- **Server Monitoring**: Real-time server health checks and alerts
- **Backup Management**: Automated backup and restoration utilities
- **Log Analysis**: Parse and analyze application logs
- **Docker Utilities**: Container management and orchestration helpers
- **Database Tools**: Database backup and migration automation
- **SSL Management**: Certificate renewal and management
- **Git Operations**: Automated git workflows and hooks

## Technologies Used

- Python 3.8+
- Bash scripting
- Docker & Docker Compose
- Git
- SSH/SCP
- Cron jobs

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` file:

```yaml
servers:
  - name: production
    host: example.com
    user: admin
    port: 22
    key_path: ~/.ssh/id_rsa

monitoring:
  check_interval: 300
  alert_email: admin@example.com

backup:
  destination: /backups
  retention_days: 30
```

## Scripts

### 1. Deployment Automation (`deploy.py`)

Automated deployment to multiple servers:

```bash
python deploy.py --environment production --branch main
```

Features:
- Git pull from repository
- Build and test
- Zero-downtime deployment
- Rollback capability
- Health checks

### 2. Server Monitor (`monitor.py`)

Real-time server monitoring:

```bash
python monitor.py --continuous
```

Monitors:
- CPU usage
- Memory usage
- Disk space
- Network traffic
- Process status
- Service health

### 3. Backup Manager (`backup.py`)

Automated backup solution:

```bash
python backup.py --type full --compress
```

Features:
- Database backups
- File system backups
- Incremental backups
- Compression
- Remote storage
- Automated cleanup

### 4. Log Analyzer (`log_analyzer.py`)

Parse and analyze logs:

```bash
python log_analyzer.py --file /var/log/app.log --errors-only
```

Features:
- Error detection
- Pattern matching
- Statistics generation
- Alert on anomalies

### 5. Docker Manager (`docker_manager.py`)

Docker container management:

```bash
python docker_manager.py --action restart --service webapp
```

Features:
- Container health checks
- Automatic restarts
- Resource monitoring
- Image cleanup
- Volume management

## Project Structure

```
devops-automation-suite/
├── scripts/
│   ├── deploy.py           # Deployment automation
│   ├── monitor.py          # Server monitoring
│   ├── backup.py           # Backup management
│   ├── log_analyzer.py     # Log analysis
│   └── docker_manager.py   # Docker utilities
├── utils/
│   ├── ssh_client.py       # SSH operations
│   ├── email_notifier.py   # Email notifications
│   ├── logger.py           # Logging utilities
│   └── config_loader.py    # Configuration management
├── config.yaml.example     # Example configuration
└── README.md
```

## Usage Examples

### Deploy to Production
```bash
# Deploy specific version
python scripts/deploy.py --env production --tag v1.2.3

# Deploy with rollback on failure
python scripts/deploy.py --env staging --rollback-on-error
```

### Monitor Servers
```bash
# One-time check
python scripts/monitor.py --check-once

# Continuous monitoring with alerts
python scripts/monitor.py --continuous --alert-threshold 80
```

### Backup Databases
```bash
# Full backup
python scripts/backup.py --type database --databases all

# Incremental backup
python scripts/backup.py --type incremental --since yesterday
```

### Analyze Logs
```bash
# Find errors in last hour
python scripts/log_analyzer.py --since "1 hour ago" --level ERROR

# Generate report
python scripts/log_analyzer.py --report --output report.html
```

## Scheduling with Cron

Add to crontab for automation:

```bash
# Backup every day at 2 AM
0 2 * * * /usr/bin/python3 /path/to/backup.py --type full

# Monitor every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/monitor.py --check-once

# Clean old logs weekly
0 0 * * 0 /usr/bin/python3 /path/to/log_analyzer.py --cleanup
```

## Security Considerations

- Store credentials in environment variables
- Use SSH keys instead of passwords
- Encrypt sensitive configuration
- Implement proper logging
- Regular security audits

## Future Enhancements

- Kubernetes support
- Cloud provider integration (AWS, Azure, GCP)
- Terraform automation
- Ansible playbook generation
- Slack/Discord notifications
- Web dashboard
- Multi-cloud support
