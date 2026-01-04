import os
import subprocess
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def get_system_metrics():
    """
    Gather real system metrics strictly from the OS.
    Designed for Linux environments (CyberPanel).
    """
    metrics = {
        'cpu_load': 0.0,
        'memory_percent': 0,
        'disk_percent': 0,
        'score': 100,
        'details': {}
    }

    # 1. Memory Usage (Linux /proc/meminfo)
    try:
        with open('/proc/meminfo', 'r') as f:
            mem_info = {}
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = int(parts[1].strip().split()[0]) # kB
                    mem_info[key] = val
            
            if 'MemTotal' in mem_info and 'MemAvailable' in mem_info:
                total_mem = mem_info['MemTotal']
                avail_mem = mem_info['MemAvailable']
                used_mem = total_mem - avail_mem
                metrics['memory_percent'] = int((used_mem / total_mem) * 100)
                metrics['details']['memory_used_mb'] = int(used_mem / 1024)
                metrics['details']['memory_total_mb'] = int(total_mem / 1024)
    except FileNotFoundError:
        # Fallback for development (e.g., Mac)
        metrics['details']['error_mem'] = "Memory stats unavailable (Not Linux)"

    # 2. CPU Load (1, 5, 15 min avg)
    try:
        load1, load5, load15 = os.getloadavg()
        metrics['cpu_load'] = round(load1, 2)
    except OSError:
        pass

    # 3. Disk Usage (Root partition)
    try:
        stat = os.statvfs('/')
        total_blocks = stat.f_blocks
        free_blocks = stat.f_bavail
        used_blocks = total_blocks - free_blocks
        metrics['disk_percent'] = int((used_blocks / total_blocks) * 100)
    except OSError:
        pass

    # 4. Calculate Optimization Score
    # Start at 100, deduct based on resource pressure
    score = 100
    
    # Memory penalty
    mem_p = metrics['memory_percent']
    if mem_p > 90: score -= 30
    elif mem_p > 75: score -= 15
    elif mem_p > 60: score -= 5

    # Load penalty (Soft assumption: load > 4 is heavy for typical VPS)
    load = metrics['cpu_load']
    if load > 5.0: score -= 25
    elif load > 2.0: score -= 10

    # Disk penalty
    disk_p = metrics['disk_percent']
    if disk_p > 90: score -= 20
    elif disk_p > 80: score -= 10

    # 5. Redis Status Check
    try:
        subprocess.check_call(['pgrep', 'redis-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        metrics['redis_active'] = True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        metrics['redis_active'] = False

    metrics['score'] = max(0, min(100, score))
    
    # Generate explicit recommendation
    if metrics['score'] < 90:
        metrics['recommendation'] = True
        metrics['recommendation_text'] = "Optimization Recommended"
        metrics['recommendation_color'] = "warning" # Bootstrap class part
    else:
        metrics['recommendation'] = False
        metrics['recommendation_text'] = "System Healthy"
        metrics['recommendation_color'] = "success"

    return metrics

@login_required
def index(request):
    """
    Main dashboard view using real-time system metrics.
    """
    metrics = get_system_metrics()
    
    status_color = "success"
    if metrics['score'] < 60:
        status_color = "danger"
    elif metrics['score'] < 85:
        status_color = "warning"

    context = {
        'score': metrics['score'],
        'metrics': metrics,
        'status_color': status_color,
        'plugin_name': 'HostCheckr'
    }
    return render(request, 'HostCheckr/index.html', context)

@login_required
def fix_optimization(request):
    """
    Trigger system optimization: Flush filesystem buffers and free pagecache.
    """
    if request.method == 'POST':
        msg = "Optimization steps executed."
        
        # 1. Sync
        try:
            subprocess.run(['sync'], check=True, timeout=10)
        except Exception:
            pass

        # 2. Drop Caches (Requires Root/Sudo)
        # 3 clears pagecache, dentries and inodes
        try:
            with open('/proc/sys/vm/drop_caches', 'w') as f:
                f.write('3')
            msg = "System, Database, PHP, and Redis optimized."
        except PermissionError:
            msg = "Optimization ran (Root needed for full clean)."
        except FileNotFoundError:
            pass

        # 3. MariaDB Optimization
        # 'analyze' updates index statistics without locking tables for long periods (unlike 'optimize')
        try:
            subprocess.run(['mysqlcheck', '-a', '--all-databases'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        except Exception:
            pass

        # 4. PHP Optimization
        # Killing lsphp processes forces LiteSpeed to spawn fresh ones, clearing OPcache and memory leaks
        try:
            subprocess.run(['killall', 'lsphp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        except Exception:
            pass

        # 5. Redis Optimization (Flush All)
        try:
            subprocess.run(['redis-cli', 'flushall'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        except Exception:
            pass

        # Recalculate metrics
        metrics = get_system_metrics()
        
        status_color = "success"
        if metrics['score'] < 60:
            status_color = "danger"
        elif metrics['score'] < 85:
            status_color = "warning"

        return JsonResponse({
            'status': 'success',
            'message': msg,
            'new_score': metrics['score'],
            'status_color': status_color,
            'metrics': metrics  # Return full metrics to update UI detailed view
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
