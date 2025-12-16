"""
GenLaravel Project Monitoring Data
Stores Issue Log, Change Log, Task Monitoring, and Vendor Monitoring
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Data file path
DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "monitoring_data.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Default data structure
DEFAULT_DATA = {
    "issue_log": [
        {
            "id": 1,
            "date": "2024-12-10",
            "issue": "Cerebras API rate limit exceeded during peak usage",
            "severity": "High",
            "status": "Resolved",
            "resolution": "Implemented Mistral fallback and request queuing",
            "pic": "Backend Team"
        },
        {
            "id": 2,
            "date": "2024-12-12",
            "issue": "WebSocket connection drops on Railway deployment",
            "severity": "High",
            "status": "In Progress",
            "resolution": "Investigating proxy buffering settings",
            "pic": "DevOps Team"
        },
        {
            "id": 3,
            "date": "2024-12-13",
            "issue": "Draft HTML validation fails for complex layouts",
            "severity": "Medium",
            "status": "Resolved",
            "resolution": "Enhanced validator agent with auto-fix capability",
            "pic": "AI Team"
        },
        {
            "id": 4,
            "date": "2024-12-14",
            "issue": "Frontend hardcoded localhost URLs breaking production",
            "severity": "High",
            "status": "Resolved",
            "resolution": "Implemented CONFIG.getApiUrl() for dynamic URLs",
            "pic": "Frontend Team"
        },
        {
            "id": 5,
            "date": "2024-12-15",
            "issue": "Multi-page generation timeout for 5+ pages",
            "severity": "Medium",
            "status": "Open",
            "resolution": "Pending - Need to optimize agent pipeline",
            "pic": "AI Team"
        }
    ],
    "change_log": [
        {
            "id": 1,
            "date": "2024-12-08",
            "change_type": "Feature Addition",
            "description": "Added multi-page generation support",
            "reason": "User requirement for generating complete applications",
            "impact": "Major - New agent pipeline required",
            "approved_by": "Project Manager"
        },
        {
            "id": 2,
            "date": "2024-12-11",
            "change_type": "Architecture Change",
            "description": "Unified WebSocket endpoint for single/multi mode",
            "reason": "Simplify backend and enable queue system",
            "impact": "Medium - Frontend needs update",
            "approved_by": "Tech Lead"
        },
        {
            "id": 3,
            "date": "2024-12-14",
            "change_type": "Deployment Change",
            "description": "Migrated from local to Railway + Vercel",
            "reason": "Enable public access and demo capability",
            "impact": "Major - Configuration overhaul needed",
            "approved_by": "Project Manager"
        }
    ],
    "task_monitoring": [
        {
            "id": 1,
            "task": "Prompt Expander Agent",
            "status": "Completed",
            "pic": "Fikri",
            "progress": 100
        },
        {
            "id": 2,
            "task": "Draft Agent (HTML Generator)",
            "status": "Completed",
            "pic": "Fikri",
            "progress": 100
        },
        {
            "id": 3,
            "task": "Prompt Planner Agent",
            "status": "Completed",
            "pic": "Fikri",
            "progress": 100
        },
        {
            "id": 4,
            "task": "Page Architect Agent",
            "status": "Completed",
            "pic": "Fikri",
            "progress": 100
        },
        {
            "id": 5,
            "task": "UI Generator Agent",
            "status": "Completed",
            "pic": "Fikri",
            "progress": 100
        },
        {
            "id": 6,
            "task": "Route Generator Agent",
            "status": "Completed",
            "pic": "Fikri",
            "progress": 100
        },
        {
            "id": 7,
            "task": "Validator Agent",
            "status": "Completed",
            "pic": "Fikri",
            "progress": 100
        },
        {
            "id": 8,
            "task": "Frontend UI Development",
            "status": "Completed",
            "pic": "Frontend Team",
            "progress": 100
        },
        {
            "id": 9,
            "task": "WebSocket Streaming",
            "status": "In Progress",
            "pic": "Backend Team",
            "progress": 85
        },
        {
            "id": 10,
            "task": "Production Deployment",
            "status": "In Progress",
            "pic": "DevOps Team",
            "progress": 70
        }
    ],
    "vendor_monitoring": [
        {
            "id": 1,
            "vendor": "Cerebras AI",
            "service": "LLM API (Qwen 32B)",
            "sla_response": "< 2 seconds",
            "actual_response": "1.5 seconds avg",
            "sla_met": True,
            "repair_time": "N/A",
            "quality_score": 95,
            "notes": "Excellent speed, occasional rate limits"
        },
        {
            "id": 2,
            "vendor": "Mistral AI",
            "service": "LLM API (Fallback)",
            "sla_response": "< 5 seconds",
            "actual_response": "3.2 seconds avg",
            "sla_met": True,
            "repair_time": "N/A",
            "quality_score": 88,
            "notes": "Reliable fallback, slightly slower"
        },
        {
            "id": 3,
            "vendor": "Railway",
            "service": "Backend Hosting",
            "sla_response": "99.9% uptime",
            "actual_response": "99.5% uptime",
            "sla_met": False,
            "repair_time": "< 1 hour",
            "quality_score": 85,
            "notes": "WebSocket proxy issues being resolved"
        },
        {
            "id": 4,
            "vendor": "Vercel",
            "service": "Frontend Hosting",
            "sla_response": "99.99% uptime",
            "actual_response": "99.99% uptime",
            "sla_met": True,
            "repair_time": "N/A",
            "quality_score": 98,
            "notes": "Excellent performance and CDN"
        }
    ],
    "generation_stats": {
        "total_generations": 0,
        "successful": 0,
        "failed": 0,
        "single_page": 0,
        "multi_page": 0,
        "avg_duration_seconds": 0,
        "last_generation": None
    }
}


def load_data():
    """Load monitoring data from file"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()


def save_data(data):
    """Save monitoring data to file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_all_data():
    """Get all monitoring data"""
    return load_data()


def add_issue(issue: dict):
    """Add new issue to log"""
    data = load_data()
    issue['id'] = len(data['issue_log']) + 1
    issue['date'] = datetime.now().strftime('%Y-%m-%d')
    data['issue_log'].append(issue)
    save_data(data)
    return issue


def add_change(change: dict):
    """Add new change to log"""
    data = load_data()
    change['id'] = len(data['change_log']) + 1
    change['date'] = datetime.now().strftime('%Y-%m-%d')
    data['change_log'].append(change)
    save_data(data)
    return change


def update_task(task_id: int, updates: dict):
    """Update task progress"""
    data = load_data()
    for task in data['task_monitoring']:
        if task['id'] == task_id:
            task.update(updates)
            break
    save_data(data)
    return data['task_monitoring']


def record_generation(mode: str, success: bool, duration: float):
    """Record generation statistics"""
    data = load_data()
    stats = data['generation_stats']
    
    stats['total_generations'] += 1
    if success:
        stats['successful'] += 1
    else:
        stats['failed'] += 1
    
    if mode == 'single':
        stats['single_page'] += 1
    else:
        stats['multi_page'] += 1
    
    # Update average duration
    total = stats['total_generations']
    old_avg = stats['avg_duration_seconds']
    stats['avg_duration_seconds'] = ((old_avg * (total - 1)) + duration) / total
    stats['last_generation'] = datetime.now().isoformat()
    
    save_data(data)
    return stats


# Initialize data file if not exists
if not DATA_FILE.exists():
    save_data(DEFAULT_DATA)
