import json
import base64

# Define the structured chart data following Helena Rasiowa's 5-level decision tree depth metrics
chart_data = {
    "metadata": {
        "chart_type": "bar",
        "chart_title": "Multi-Resolution Neuro-Symbolic Model Tree Depths",
        "orientation": "vertical",
        "stacking": "none",
        "x_axis_title": "Tree Processing Tier",
        "y_axis_title": "Maximum Tree Depth (Steps)"
    },
    "labels": [
        "Level 1 Vocab", 
        "Level 2 Unit", 
        "Level 3 Story", 
        "Level 4 Analogy", 
        "Level 5 Plan Synthesis"
    ],
    "datasets": [
        {
            "label": "Tree Depth Trackers",
            "axis": "primary",
            "data": [
                {"value_raw": 2.0, "tooltip_text": "Level 1 Vocabulary: Depth = 2 Steps (Capitalization and Suffix Splits)"},
                {"value_raw": 2.0, "tooltip_text": "Level 2 Unit Containment: Depth = 2 Steps (Part-Whole Component Contractions)"},
                {"value_raw": 1.0, "tooltip_text": "Level 3 Story Context: Depth = 1 Step (Macro Domain Segregations)"},
                {"value_raw": 1.0, "tooltip_text": "Level 4 Homomorphism Analogy: Depth = 1 Step (Cross-Domain Isomorphism Mappings)"},
                {"value_raw": 3.0, "tooltip_text": "Level 5 Plan Synthesis: Depth = 3 Steps (Dynamic Graph Minor Reroute Estimators)"}
            ]
        }
    ]
}

# Serialize and encode to base64 format for safe, raw pipeline materialization
spec_str = json.dumps(chart_data).encode('utf-8')
print(f'chartjs_spec: "{base64.b64encode(spec_str).decode("utf-8")}"')
