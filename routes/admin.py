from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.mongo import systems_col, labs_col, staff_col

admin_bp = Blueprint('admin', __name__)

# Dashboard View
@admin_bp.route('/dashboard')
def dashboard():
    if 'staff_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Fetch Data for Dashboard
    labs = list(labs_col.find())
    total_systems = systems_col.count_documents({})
    active_users = systems_col.count_documents({"status": "ON"})
    maintenance_issues = systems_col.count_documents({"status": "DEAD"})
    
    return render_template('dashboard.html', 
                           labs=labs, 
                           total=total_systems, 
                           active=active_users, 
                           issues=maintenance_issues,
                           staff_name=session.get('staff_name', 'Staff'))

# Add System Logic
@admin_bp.route('/add_system', methods=['POST'])
def add_system():
    if 'staff_id' not in session:
        return redirect(url_for('auth.login'))
        
    lab_id = request.form.get('lab_id')
    table = request.form.get('table')
    pc_name = request.form.get('pc_name')
    config = request.form.get('config')
    
    # Simple validation
    if not lab_id or not pc_name:
        flash("Lab ID and PC Name are required!", "error")
        return redirect(url_for('admin.dashboard'))
        
    # Check if exists
    if systems_col.find_one({"lab_id": lab_id, "pc_name": pc_name}):
        flash(f"System {pc_name} already exists in {lab_id}", "error")
        return redirect(url_for('admin.dashboard'))

    # Determine position automatically? 
    # For now, just append to end or find max position?
    # Or just let it be 0 and rely on layout order if flexible?
    # The current layout logic relies on 'position' for ordering in the loop.
    # We should find the max position for this table.
    
    last_sys = systems_col.find_one(
        {"lab_id": lab_id, "table": table},
        sort=[("position", -1)]
    )
    new_pos = (last_sys["position"] + 1) if last_sys else 1
    
    new_system = {
        "_id": f"{lab_id}_{pc_name}",
        "lab_id": lab_id,
        "table": table,
        "pc_name": pc_name,
        "position": new_pos,
        "config": config,
        "user": "Available",
        "status": "OFF", # Default state
        "purpose": None
    }
    
    systems_col.insert_one(new_system)
    
    # Update Lab Details (lazy update or recalc?)
    # We should update the lab stats
    update_lab_stats(lab_id)
    
    flash(f"System {pc_name} added successfully!", "success")
    return redirect(url_for('admin.dashboard'))

# Allocate System Logic
@admin_bp.route('/allocate_system', methods=['POST'])
def allocate_system():
    if 'staff_id' not in session:
        return redirect(url_for('auth.login'))
        
    lab_id = request.form.get('lab_id')
    pc_name = request.form.get('pc_name')
    user_name = request.form.get('user_name')
    activity = request.form.get('activity')
    
    result = systems_col.update_one(
        {"lab_id": lab_id, "pc_name": pc_name},
        {"$set": {
            "status": "ON",
            "user": user_name,
            "purpose": activity
        }}
    )
    
    if result.matched_count > 0:
        update_lab_stats(lab_id)
        flash(f"Allocated {pc_name} to {user_name}", "success")
    else:
        flash(f"System {pc_name} not found!", "error")
        
    return redirect(url_for('admin.dashboard'))

# Remove System Logic
@admin_bp.route('/remove_system', methods=['POST'])
def remove_system():
    if 'staff_id' not in session:
        return redirect(url_for('auth.login'))
        
    lab_id = request.form.get('lab_id')
    pc_name = request.form.get('pc_name')
    
    result = systems_col.delete_one({"lab_id": lab_id, "pc_name": pc_name})
    
    if result.deleted_count > 0:
        update_lab_stats(lab_id)
        flash(f"System {pc_name} removed permanently.", "error") # Red toast
    else:
        flash(f"System {pc_name} not found!", "error")
        
    return redirect(url_for('admin.dashboard'))

# Helper to recalc stats
def update_lab_stats(lab_id):
    total = systems_col.count_documents({"lab_id": lab_id})
    running = systems_col.count_documents({"lab_id": lab_id, "status": "ON"})
    dead = systems_col.count_documents({"lab_id": lab_id, "status": "DEAD"})
    available = systems_col.count_documents({"lab_id": lab_id, "status": "OFF"})
    
    labs_col.update_one(
        {"_id": lab_id},
        {"$set": {"total": total, "running": running, "dead": dead, "available": available}}
    )
