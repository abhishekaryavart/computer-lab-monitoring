from flask import render_template, session, redirect, url_for, flash
from db.mongo import labs_col, systems_col


def home():
    labs_cursor = labs_col.find({"department": "Computer Science"})
    labs_data = []

    for lab in labs_cursor:
        lab_id = lab["_id"]
        # Calculate stats
        total = systems_col.count_documents({"lab_id": lab_id})
        running = systems_col.count_documents({"lab_id": lab_id, "status": "ON"})
        dead = systems_col.count_documents({"lab_id": lab_id, "status": "DEAD"})
        available = total - running - dead # Simplified availability logic

        # Append stats to lab dict
        lab["total"] = total
        lab["running"] = running
        lab["dead"] = dead
        lab["available"] = available
        lab["lab_id"] = lab_id # Ensure lab_id key exists for template
        
        labs_data.append(lab)

    return render_template("home.html", labs=labs_data)


def lab_view(lab_id):
    if 'staff_id' not in session:
        flash("You must be logged in to view lab details.", "error")
        return redirect(url_for('auth.login'))

    lab = labs_col.find_one({"_id": lab_id})
    print("LAB ID:", lab_id)
    print("LAB DATA:", lab)

    if not lab:
        return f"Lab '{lab_id}' not found in database", 404

    # Fetch systems for this lab
    systems = list(systems_col.find({"lab_id": lab_id}))


    # ---- Build table structure ----
    # ---- Dynamic Layout Configuration ----
    def table_side(table_name, capacity):
        side_systems = [s for s in systems if s["table"] == table_name]
        return {
            "name": table_name,
            "capacity": capacity,
            "systems": side_systems
        }

    # Define variable layouts based on Lab ID
    tables = []
    
    if lab_id == "MCA_LAB":
        # Classic L1-L5 Layout
        tables = [
            {"type": "single", "sides": [table_side("L5", 10)]},
            {"type": "", "sides": [table_side("L3", 10), table_side("L4", 10)]},
            {"type": "short", "sides": [table_side("L1", 5), table_side("L2", 5)]}
        ]
        
    elif lab_id == "BCA_LAB":
        # 4 Large Rows (B1-B4)
        tables = [
             {"type": "", "sides": [table_side("B1", 10), table_side("B2", 10)]},
             {"type": "", "sides": [table_side("B3", 10), table_side("B4", 10)]}
        ]
        
    elif lab_id == "BIT_LAB":
        # High Density 6 Rows (T1-T6)
        tables = [
            {"type": "", "sides": [table_side("T1", 10), table_side("T2", 10)]},
            {"type": "", "sides": [table_side("T3", 10), table_side("T4", 10)]},
            {"type": "", "sides": [table_side("T5", 10), table_side("T6", 10)]}
        ]

    # Recalculate blank/dead for accurate stats
    lab_capacity = sum(len(side["systems"]) + (side["capacity"] - len(side["systems"])) for t in tables for side in t["sides"])
    # Note: simple capacity sum logic is complex, approximating or using DB totals
    # Better to rely on DB totals calculated in seeding for the header stats

    # ---- Stats ----
    total = len(systems)
    running = sum(1 for s in systems if s["status"] == "ON")
    dead = sum(1 for s in systems if s["status"] == "DEAD")
    blank = 30 - total   # example capacity

    stats = {
        "total": total,
        "running": running,
        "dead": dead,
        "blank": blank
    }

    return render_template(
        "lab.html",
        lab_name=lab["name"],
        tables=tables,
        stats=stats
    )
