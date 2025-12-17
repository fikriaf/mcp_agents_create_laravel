#!/usr/bin/env python3
"""
GenLaravel Monitoring Data Visualization
Generates charts and graphs from monitoring data
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from datetime import datetime
import numpy as np

# Paths
DATA_FILE = Path(__file__).parent.parent / "genlaravel_monitoring_2025-12-16 (3).json"
OUTPUT_DIR = Path(__file__).parent.parent / "frontend/docs/charts"

# Colors
COLORS = {
    'primary': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#9b59b6',
    'dark': '#2c3e50',
    'light': '#ecf0f1'
}

def load_data():
    """Load monitoring data from JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_output_dir():
    """Create output directory if not exists"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def plot_issue_severity(data):
    """Pie chart for issue severity distribution - COMPACT SIZE"""
    issues = data['issue_log']
    
    severity_count = {'High': 0, 'Medium': 0, 'Low': 0}
    for issue in issues:
        sev = issue.get('severity', 'Medium')
        severity_count[sev] = severity_count.get(sev, 0) + 1
    
    labels = [k for k, v in severity_count.items() if v > 0]
    sizes = [v for v in severity_count.values() if v > 0]
    colors = [COLORS['danger'], COLORS['warning'], COLORS['success']][:len(labels)]
    
    fig, ax = plt.subplots(figsize=(5, 4))  # Smaller size
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                       autopct='%1.1f%%', startangle=90,
                                       explode=[0.05]*len(labels))
    ax.set_title('Issue Severity Distribution', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'issue_severity.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("✅ Created: issue_severity.png")

def plot_issue_status(data):
    """Bar chart for issue status"""
    issues = data['issue_log']
    
    status_count = {'Resolved': 0, 'Open': 0, 'In Progress': 0}
    for issue in issues:
        status = issue.get('status', 'Open')
        status_count[status] = status_count.get(status, 0) + 1

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(status_count.keys(), status_count.values(), 
                  color=[COLORS['success'], COLORS['warning'], COLORS['primary']])
    
    ax.set_xlabel('Status')
    ax.set_ylabel('Count')
    ax.set_title('Issue Status Overview', fontsize=14, fontweight='bold')
    
    for bar, count in zip(bars, status_count.values()):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'issue_status.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: issue_status.png")

def plot_vendor_comparison(data):
    """Bar chart comparing vendor performance"""
    vendors = data['vendor_monitoring']
    
    llm_vendors = [v for v in vendors if v.get('total_calls')]
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    
    # Success Rate
    names = [v['vendor'] for v in llm_vendors]
    success_rates = [v['successful_calls']/v['total_calls']*100 for v in llm_vendors]
    colors = [COLORS['success'] if r >= 90 else COLORS['warning'] if r >= 70 else COLORS['danger'] for r in success_rates]
    
    axes[0].bar(names, success_rates, color=colors)
    axes[0].set_ylabel('Success Rate (%)')
    axes[0].set_title('Success Rate by Vendor', fontweight='bold')
    axes[0].set_ylim(0, 110)
    axes[0].axhline(y=99, color=COLORS['danger'], linestyle='--', label='SLA Target (99%)')
    axes[0].legend()
    
    for i, (name, rate) in enumerate(zip(names, success_rates)):
        axes[0].text(i, rate + 2, f'{rate:.1f}%', ha='center', fontweight='bold')
    
    # Response Time
    response_times = [v['avg_response_ms']/1000 for v in llm_vendors]
    sla_targets = [v['sla_target_ms']/1000 for v in llm_vendors]
    
    x = np.arange(len(names))
    width = 0.35
    
    bars1 = axes[1].bar(x - width/2, response_times, width, label='Actual', color=COLORS['primary'])
    bars2 = axes[1].bar(x + width/2, sla_targets, width, label='SLA Target', color=COLORS['light'], edgecolor=COLORS['dark'])
    
    axes[1].set_ylabel('Response Time (seconds)')
    axes[1].set_title('Response Time vs SLA Target', fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(names)
    axes[1].legend()
    
    # Total Calls
    total_calls = [v['total_calls'] for v in llm_vendors]
    successful = [v['successful_calls'] for v in llm_vendors]
    failed = [v['failed_calls'] for v in llm_vendors]
    
    axes[2].bar(names, successful, label='Successful', color=COLORS['success'])
    axes[2].bar(names, failed, bottom=successful, label='Failed', color=COLORS['danger'])
    axes[2].set_ylabel('Number of Calls')
    axes[2].set_title('API Calls Distribution', fontweight='bold')
    axes[2].legend()
    
    for i, (s, f) in enumerate(zip(successful, failed)):
        axes[2].text(i, s + f + 2, f'{s+f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'vendor_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: vendor_comparison.png")

def plot_task_progress(data):
    """Horizontal bar chart for task progress"""
    tasks = data['task_monitoring']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    task_names = [t['task'][:30] for t in tasks]
    progress = [t['progress'] for t in tasks]
    colors = [COLORS['success'] if p == 100 else COLORS['warning'] if p >= 50 else COLORS['danger'] for p in progress]
    
    y_pos = np.arange(len(task_names))
    bars = ax.barh(y_pos, progress, color=colors)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(task_names)
    ax.set_xlabel('Progress (%)')
    ax.set_title('Task Progress Overview', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 110)
    
    for i, (bar, p) in enumerate(zip(bars, progress)):
        ax.text(p + 1, i, f'{p}%', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'task_progress.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: task_progress.png")


def plot_generation_stats(data):
    """Pie chart for generation statistics"""
    stats = data['generation_stats']
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Success vs Failed
    labels1 = ['Successful', 'Failed']
    sizes1 = [stats['successful'], stats['failed']]
    colors1 = [COLORS['success'], COLORS['danger']]
    
    if stats['failed'] == 0:
        axes[0].pie([1], labels=['100% Success'], colors=[COLORS['success']], 
                    autopct='', startangle=90)
        axes[0].text(0, 0, f"{stats['successful']}\nGenerations", ha='center', va='center', 
                     fontsize=16, fontweight='bold')
    else:
        axes[0].pie(sizes1, labels=labels1, colors=colors1, autopct='%1.1f%%', startangle=90)
    
    axes[0].set_title('Generation Success Rate', fontweight='bold')
    
    # Single vs Multi Page
    labels2 = ['Single Page', 'Multi Page']
    sizes2 = [stats['single_page'], stats['multi_page']]
    colors2 = [COLORS['primary'], COLORS['info']]
    
    axes[1].pie(sizes2, labels=labels2, colors=colors2, autopct='%1.1f%%', startangle=90,
                explode=[0.02, 0.02])
    axes[1].set_title('Generation Type Distribution', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'generation_stats.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: generation_stats.png")

def plot_vendor_quality_scores(data):
    """Bar chart for vendor quality scores - COMPACT SIZE"""
    vendors = data['vendor_monitoring']
    
    fig, ax = plt.subplots(figsize=(6, 4))  # Smaller size
    
    names = [v['vendor'] for v in vendors]
    scores = [v.get('quality_score', 0) for v in vendors]
    sla_met = [v.get('sla_met', False) for v in vendors]
    
    colors = [COLORS['success'] if met else COLORS['danger'] for met in sla_met]
    
    bars = ax.bar(names, scores, color=colors, edgecolor=COLORS['dark'], linewidth=1.5)
    
    ax.set_ylabel('Quality Score', fontsize=9)
    ax.set_title('Vendor Quality Scores & SLA Status', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.axhline(y=90, color=COLORS['warning'], linestyle='--', label='Target (90%)')
    ax.tick_params(axis='x', labelsize=8)
    
    for bar, score, met in zip(bars, scores, sla_met):
        status = '✓' if met else '✗'
        ax.text(bar.get_x() + bar.get_width()/2, score + 2, 
                f'{score}%{status}', ha='center', fontsize=8, fontweight='bold')
    
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'vendor_quality.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("✅ Created: vendor_quality.png")

def plot_change_log_timeline(data):
    """Timeline visualization for change log"""
    changes = data['change_log']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    change_types = list(set(c['change_type'] for c in changes))
    type_colors = {
        'Feature Addition': COLORS['success'],
        'Architecture Change': COLORS['primary'],
        'Deployment Change': COLORS['info'],
        'Bug Fix': COLORS['warning']
    }
    
    dates = [c['date'] for c in changes]
    types = [c['change_type'] for c in changes]
    impacts = [c['impact'] for c in changes]
    
    y_positions = [change_types.index(t) for t in types]
    colors = [type_colors.get(t, COLORS['dark']) for t in types]
    sizes = [300 if i == 'Major' else 200 if i == 'Medium' else 100 for i in impacts]
    
    scatter = ax.scatter(range(len(dates)), y_positions, c=colors, s=sizes, alpha=0.7, edgecolors='black')
    
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, ha='right')
    ax.set_yticks(range(len(change_types)))
    ax.set_yticklabels(change_types)
    ax.set_xlabel('Date')
    ax.set_title('Change Log Timeline', fontsize=14, fontweight='bold')
    
    # Add descriptions
    for i, c in enumerate(changes):
        ax.annotate(c['description'][:25] + '...', (i, y_positions[i]), 
                    textcoords="offset points", xytext=(0, 10), ha='center', fontsize=7)
    
    # Legend for impact
    legend_elements = [
        plt.scatter([], [], s=300, c='gray', label='Major Impact'),
        plt.scatter([], [], s=200, c='gray', label='Medium Impact'),
        plt.scatter([], [], s=100, c='gray', label='Minor Impact')
    ]
    ax.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'change_timeline.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: change_timeline.png")

def plot_summary_dashboard(data):
    """Summary dashboard with key metrics"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('GenLaravel Monitoring Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Issue Summary
    issues = data['issue_log']
    resolved = sum(1 for i in issues if i['status'] == 'Resolved')
    open_issues = sum(1 for i in issues if i['status'] == 'Open')
    
    axes[0, 0].pie([resolved, open_issues], labels=['Resolved', 'Open'], 
                   colors=[COLORS['success'], COLORS['warning']], autopct='%1.0f%%')
    axes[0, 0].set_title(f'Issues ({len(issues)} total)')
    
    # 2. Task Completion
    tasks = data['task_monitoring']
    completed = sum(1 for t in tasks if t['progress'] == 100)
    
    axes[0, 1].bar(['Completed', 'In Progress'], [completed, len(tasks) - completed],
                   color=[COLORS['success'], COLORS['warning']])
    axes[0, 1].set_title(f'Tasks ({len(tasks)} total)')
    axes[0, 1].set_ylabel('Count')
    
    # 3. Generation Stats
    stats = data['generation_stats']
    axes[0, 2].bar(['Single', 'Multi'], [stats['single_page'], stats['multi_page']],
                   color=[COLORS['primary'], COLORS['info']])
    axes[0, 2].set_title(f"Generations ({stats['total_generations']} total)")
    axes[0, 2].set_ylabel('Count')
    
    # 4. Vendor Success Rates
    vendors = [v for v in data['vendor_monitoring'] if v.get('total_calls')]
    names = [v['vendor'] for v in vendors]
    rates = [v['successful_calls']/v['total_calls']*100 for v in vendors]
    colors = [COLORS['success'] if r >= 90 else COLORS['warning'] for r in rates]
    
    axes[1, 0].bar(names, rates, color=colors)
    axes[1, 0].axhline(y=99, color=COLORS['danger'], linestyle='--')
    axes[1, 0].set_title('Vendor Success Rates')
    axes[1, 0].set_ylabel('Success %')
    axes[1, 0].set_ylim(0, 110)
    
    # 5. API Calls
    total_calls = sum(v.get('total_calls', 0) for v in vendors)
    successful = sum(v.get('successful_calls', 0) for v in vendors)
    
    axes[1, 1].pie([successful, total_calls - successful], 
                   labels=['Success', 'Failed'],
                   colors=[COLORS['success'], COLORS['danger']], autopct='%1.1f%%')
    axes[1, 1].set_title(f'API Calls ({total_calls} total)')
    
    # 6. Key Metrics Text
    axes[1, 2].axis('off')
    metrics_text = f"""
    📊 KEY METRICS
    ─────────────────
    Total Issues: {len(issues)}
    Resolved: {resolved} ({resolved/len(issues)*100:.0f}%)
    
    Total Tasks: {len(tasks)}
    Completed: {completed} ({completed/len(tasks)*100:.0f}%)
    
    Total Generations: {stats['total_generations']}
    Success Rate: 100%
    
    Total API Calls: {total_calls}
    Success Rate: {successful/total_calls*100:.1f}%
    
    Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """
    axes[1, 2].text(0.1, 0.5, metrics_text, transform=axes[1, 2].transAxes,
                    fontsize=11, verticalalignment='center', fontfamily='monospace',
                    bbox=dict(boxstyle='round', facecolor=COLORS['light'], alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'dashboard_summary.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: dashboard_summary.png")

def main():
    """Main function to generate all visualizations"""
    print("🚀 GenLaravel Monitoring Visualization")
    print("=" * 50)
    
    # Load data
    print(f"📖 Loading data from: {DATA_FILE}")
    data = load_data()
    
    # Create output directory
    create_output_dir()
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print()
    
    # Generate all charts
    print("📊 Generating visualizations...")
    plot_issue_severity(data)
    plot_issue_status(data)
    plot_vendor_comparison(data)
    plot_task_progress(data)
    plot_generation_stats(data)
    plot_vendor_quality_scores(data)
    plot_change_log_timeline(data)
    plot_summary_dashboard(data)
    
    print()
    print("=" * 50)
    print("✅ All visualizations generated successfully!")
    print(f"📁 Charts saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
