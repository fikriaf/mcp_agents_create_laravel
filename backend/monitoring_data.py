"""
GenLaravel Project Monitoring Data
Auto-records Issue Log, Change Log, Task Monitoring, and Vendor Monitoring
from REAL system activity - NO SIMULATION DATA
"""

import json
import os
from datetime import datetime
from pathlib import Path
import time

# Data file path
DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "monitoring_data.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Empty default data structure - NO SIMULATION
DEFAULT_DATA = {
    "issue_log": [],
    "change_log": [],
    "task_monitoring": [],
    "vendor_monitoring": [],
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


# ============================================
# 🐛 ISSUE LOG - Auto-recorded from errors
# ============================================

def log_issue(issue: str, severity: str = "Medium", source: str = "System", resolution: str = ""):
    """Auto-log issue when error occurs in system"""
    data = load_data()
    new_issue = {
        "id": len(data['issue_log']) + 1,
        "date": datetime.now().strftime('%Y-%m-%d'),
        "time": datetime.now().strftime('%H:%M:%S'),
        "issue": issue,
        "severity": severity,
        "status": "Open",
        "resolution": resolution,
        "pic": source
    }
    data['issue_log'].append(new_issue)
    save_data(data)
    print(f"📋 Issue logged: {issue}")
    return new_issue


def resolve_issue(issue_id: int, resolution: str):
    """Mark issue as resolved"""
    data = load_data()
    for issue in data['issue_log']:
        if issue['id'] == issue_id:
            issue['status'] = "Resolved"
            issue['resolution'] = resolution
            issue['resolved_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            break
    save_data(data)
    return data['issue_log']


# ============================================
# 📝 CHANGE LOG - Auto-recorded from system changes
# ============================================

def log_change(change_type: str, description: str, reason: str, impact: str = "Medium", source: str = "System"):
    """Auto-log change when system configuration changes"""
    data = load_data()
    new_change = {
        "id": len(data['change_log']) + 1,
        "date": datetime.now().strftime('%Y-%m-%d'),
        "time": datetime.now().strftime('%H:%M:%S'),
        "change_type": change_type,
        "description": description,
        "reason": reason,
        "impact": impact,
        "approved_by": source
    }
    data['change_log'].append(new_change)
    save_data(data)
    print(f"📝 Change logged: {description}")
    return new_change


# ============================================
# 📊 TASK MONITORING - Auto-updated from agent pipeline
# ============================================

def update_task_status(task_name: str, status: str, progress: int, pic: str = "System"):
    """Auto-update task status from agent pipeline"""
    data = load_data()
    
    # Find existing task or create new
    task_found = False
    for task in data['task_monitoring']:
        if task['task'] == task_name:
            task['status'] = status
            task['progress'] = progress
            task['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task_found = True
            break
    
    if not task_found:
        new_task = {
            "id": len(data['task_monitoring']) + 1,
            "task": task_name,
            "status": status,
            "pic": pic,
            "progress": progress,
            "created": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['task_monitoring'].append(new_task)
    
    save_data(data)
    return data['task_monitoring']


def reset_all_tasks():
    """Reset all tasks to pending (called at start of generation)"""
    data = load_data()
    for task in data['task_monitoring']:
        task['status'] = "Pending"
        task['progress'] = 0
    save_data(data)


# ============================================
# 🏢 VENDOR MONITORING - Auto-recorded from API calls
# ============================================

def log_vendor_call(vendor: str, service: str, response_time_ms: float, success: bool, error_msg: str = ""):
    """Auto-log vendor API call performance"""
    data = load_data()
    
    # Find existing vendor or create new
    vendor_found = False
    for v in data['vendor_monitoring']:
        if v['vendor'] == vendor and v['service'] == service:
            # Update stats
            v['total_calls'] = v.get('total_calls', 0) + 1
            v['successful_calls'] = v.get('successful_calls', 0) + (1 if success else 0)
            v['failed_calls'] = v.get('failed_calls', 0) + (0 if success else 1)
            
            # Update average response time
            old_avg = v.get('avg_response_ms', 0)
            total = v['total_calls']
            v['avg_response_ms'] = ((old_avg * (total - 1)) + response_time_ms) / total
            
            # Update last call info
            v['last_call'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            v['last_response_ms'] = response_time_ms
            v['last_success'] = success
            if not success:
                v['last_error'] = error_msg
            
            # Calculate SLA met (assuming SLA is < 5000ms)
            v['sla_met'] = v['avg_response_ms'] < 5000
            v['quality_score'] = int((v['successful_calls'] / v['total_calls']) * 100) if v['total_calls'] > 0 else 0
            
            vendor_found = True
            break
    
    if not vendor_found:
        new_vendor = {
            "id": len(data['vendor_monitoring']) + 1,
            "vendor": vendor,
            "service": service,
            "total_calls": 1,
            "successful_calls": 1 if success else 0,
            "failed_calls": 0 if success else 1,
            "avg_response_ms": response_time_ms,
            "last_call": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "last_response_ms": response_time_ms,
            "last_success": success,
            "sla_target_ms": 5000,
            "sla_met": response_time_ms < 5000,
            "quality_score": 100 if success else 0
        }
        if not success:
            new_vendor['last_error'] = error_msg
        data['vendor_monitoring'].append(new_vendor)
    
    save_data(data)
    return data['vendor_monitoring']


# ============================================
# 📈 GENERATION STATS - Auto-recorded
# ============================================

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
    if stats['total_generations'] > 0:
        total = stats['total_generations']
        old_avg = stats['avg_duration_seconds']
        stats['avg_duration_seconds'] = ((old_avg * (total - 1)) + duration) / total
    
    stats['last_generation'] = datetime.now().isoformat()
    
    save_data(data)
    return stats


# ============================================
# 🔧 UTILITY FUNCTIONS
# ============================================

def clear_all_data():
    """Clear all monitoring data (for testing)"""
    save_data(DEFAULT_DATA.copy())
    print("🗑️ All monitoring data cleared")


def get_summary():
    """Get summary of all monitoring data"""
    data = load_data()
    return {
        "total_issues": len(data['issue_log']),
        "open_issues": len([i for i in data['issue_log'] if i['status'] == 'Open']),
        "total_changes": len(data['change_log']),
        "total_tasks": len(data['task_monitoring']),
        "completed_tasks": len([t for t in data['task_monitoring'] if t['status'] == 'Completed']),
        "total_vendors": len(data['vendor_monitoring']),
        "generation_stats": data['generation_stats']
    }


# Initialize empty data file if not exists
if not DATA_FILE.exists():
    save_data(DEFAULT_DATA)
