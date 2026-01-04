import os
import subprocess
import sys
import traceback
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

# --- DEBUG LOGGER ---
def log_debug(msg):
    try:
        with open("/tmp/hostcheckr_debug.log", "a") as f:
            f.write(f"{msg}\n")
    except:
        pass

log_debug("HostCheckr: views.py loaded")

def get_system_metrics():
    log_debug("Getting system metrics...")
    metrics = {
        'cpu_load': 0.0,
        'memory_percent': 0,
        'disk_percent': 0,
        'score': 100,
        'redis_active': False
    }
    
    try:
        # Memory
        if os.path.exists('/proc/meminfo'):
            with open('/proc/meminfo', 'r') as f:
                mem_info = {}
                for line in f:
                    parts = line.split(':')
                    if len(parts) == 2:
                        mem_info[parts[0].strip()] = int(parts[1].strip().split()[0])
                if 'MemTotal' in mem_info:
                    used = mem_info['MemTotal'] - mem_info.get('MemAvailable', 0)
                    metrics['memory_percent'] = int((used / mem_info['MemTotal']) * 100)
        
        # CPU
        metrics['cpu_load'] = round(os.getloadavg()[0], 2)
        
        # Disk
        st = os.statvfs('/')
        metrics['disk_percent'] = int(((st.f_blocks - st.f_bavail) / st.f_blocks) * 100)

        # Redis logic check
        try:
            subprocess.check_call(['pgrep', 'redis-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            metrics['redis_active'] = True
        except:
            metrics['redis_active'] = False

    except Exception as e:
        log_debug(f"Error in metrics: {e}")

    # Simplified Score Logic
    score = 100
    if metrics['memory_percent'] > 90: score -= 30
    elif metrics['memory_percent'] > 70: score -= 10
    if metrics['cpu_load'] > 4.0: score -= 20
    
    metrics['score'] = max(0, min(100, score))
    
    # Recommendation
    if score < 90:
        metrics['recommendation_text'] = "Optimization Recommended"
        metrics['recommendation_color'] = "warning"
        metrics['recommendation'] = True
    else:
        metrics['recommendation_text'] = "System Healthy"
        metrics['recommendation_color'] = "success"
        metrics['recommendation'] = False
        
    return metrics

def index(request):
    log_debug("Index view execution started")
    try:
        metrics = get_system_metrics()
        context = {
            'score': metrics['score'],
            'metrics': metrics,
            'status_color': 'danger' if metrics['score'] < 60 else ('warning' if metrics['score'] < 85 else 'success'),
            'plugin_name': 'HostCheckr'
        }
        log_debug("Rendering template...")
        return render(request, 'HostCheckr/index.html', context)
    except Exception as e:
        log_debug(f"Index Exception: {e}")
        # Return fallback HTML if template fails
        return HttpResponse(f"""
            <div style="font-family:sans-serif; padding:50px; text-align:center;">
                <h1 style="color:red;">HostCheckr Error</h1>
                <p>Could not render dashboard.</p>
                <textarea style="width:100%; height:200px;">{traceback.format_exc()}</textarea>
            </div>
        """)

def fix_optimization(request):
    try:
        # Quick sync
        subprocess.run(['sync'], timeout=5)
        
        # Simple cache drop
        if os.path.exists('/proc/sys/vm/drop_caches'):
            with open('/proc/sys/vm/drop_caches', 'w') as f:
                f.write('3')
                
        metrics = get_system_metrics()
        return JsonResponse({
            'status': 'success',
            'new_score': metrics['score'],
            'status_color': 'success',
            'message': 'Optimized.',
            'metrics': metrics
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
