import json
import os

KB_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "knowledge_base.json")

def load_knowledge_base():
    """Load and validate the JSON knowledge base."""
    if not os.path.exists(KB_PATH):
        raise FileNotFoundError(f"Knowledge base not found at {KB_PATH}")
    
    with open(KB_PATH, "r", encoding="utf-8") as f:
        kb_data = json.load(f)
        
    if "stages" not in kb_data:
        raise ValueError("Invalid knowledge base structure: missing 'stages' key.")
    return kb_data

def evaluate_stage_data(stage_key, user_inputs):
    """
    Evaluates and retrieves relevant knowledge base items based on the stage
    and user inputs (subsurface layer, water behavior, local advice, weather).
    """
    kb = load_knowledge_base()
    stages = kb.get("stages", {})
    
    # Map any stage representation to the exact knowledge_base.json keys
    mapping = {
        "stage_1": "stage_1_input_echo",
        "stage_1_input_echo": "stage_1_input_echo",
        "stage_2": "stage_2_missing_analysis",
        "stage_2_missing_analysis": "stage_2_missing_analysis",
        "stage_3": "stage_3_fix_protocol",
        "stage_3_fix_protocol": "stage_3_fix_protocol",
        "stage_4": "stage_4_readiness_gate",
        "stage_4_readiness_gate": "stage_4_readiness_gate",
        "stage_5": "stage_5_crop_suggestions",
        "stage_5_crop_suggestions": "stage_5_crop_suggestions",
        "stage_6": "stage_6_timeframe",
        "stage_6_timeframe": "stage_6_timeframe",
        "stage_7": "stage_7_planting_method",
        "stage_7_planting_method": "stage_7_planting_method",
        "stage_8": "stage_8_ongoing_care",
        "stage_8_ongoing_care": "stage_8_ongoing_care",
        "stage_9": "stage_9_harvest_regeneration",
        "stage_9_harvest_regeneration": "stage_9_harvest_regeneration"
    }
    
    normalized_key = mapping.get(stage_key, stage_key)
    stage_node = stages.get(normalized_key, {})
    items = stage_node.get("items", [])
    
    # Extract & lowercase user inputs
    subsurface = str(user_inputs.get("subsurface_layer", "")).lower()
    water = str(user_inputs.get("water_behavior", "")).lower()
    advice = str(user_inputs.get("local_advice", "")).lower()
    weather = str(user_inputs.get("weather", "")).lower()
    
    # --- STAGE 2 LOGIC ---
    if "stage_2" in normalized_key:
        inferences = [
            "Shallow iron/aluminum oxide layer restricts root depth and expansion.",
            "High surface runoff potential during intense seasonal rains."
        ]
        if "hardpan" in subsurface or "rock" in subsurface:
            inferences.append("Continuous rock/hardpan prevents natural water infiltration below 15 cm.")
        return {"inferences": inferences, "items": items}
        
    # --- STAGE 3 LOGIC ---
    elif "stage_3" in normalized_key:
        filtered_actions = []
        for item in items:
            cond = item.get("condition", "")
            if "continuous_hardpan" in cond and ("hardpan" in subsurface or "rock" in subsurface):
                filtered_actions.append(item.get("action"))
            elif "loose_gravel" in cond and "gravel" in subsurface:
                filtered_actions.append(item.get("action"))
            elif "sloping_terrain" in cond and ("runoff" in water or "slope" in str(user_inputs.get("description", "")).lower()):
                filtered_actions.append(item.get("action"))
            elif "flat_land" in cond and "pooling" in water:
                filtered_actions.append(item.get("action"))
        if not filtered_actions:
            filtered_actions = [item.get("action") for item in items if "action" in item]
        return {"actions": filtered_actions, "items": items}
        
    # --- STAGE 5 LOGIC (CROP SUGGESTIONS) ---
    elif "stage_5" in normalized_key:
        relevant_crops = []
        
        for item in items:
            crop_name = item.get("crop")
            if crop_name:
                suitability = item.get("suitability", "")
                
                # Dynamic matching indicators based on user inputs
                if "pooling" in water and "Sweet Potato" in crop_name:
                    suitability = "⭐ PRIMARY DRAINAGE MATCH: " + suitability
                elif "runoff" in water and "Finger Millet" in crop_name:
                    suitability = "⭐ RUNOFF-ADAPTED MATCH: " + suitability
                elif ("hardpan" in subsurface or "rock" in subsurface) and "Pigeon Pea" in crop_name:
                    suitability = "⭐ HARDPAN PENETRATION MATCH: " + suitability
                elif ("late" in weather or "dry" in weather) and "Sorghum" in crop_name:
                    suitability = "⭐ DROUGHT & LATE-RAIN MATCH: " + suitability
                
                relevant_crops.append({
                    "crop": crop_name,
                    "suitability": suitability,
                    "trade_offs": item.get("trade_offs", "Requires organic soil amendments."),
                    "source": item.get("source_reference", "Knowledge Base")
                })
                
        # Guaranteed Fallback if items was empty
        if not relevant_crops:
            relevant_crops = [
                {
                    "crop": "Finger Millet (Ragi)",
                    "suitability": "⭐ HIGH RESILIENCE: Excellent tolerance for acidic, gravelly soils and short rainy bursts.",
                    "trade_offs": "Requires organic compost pockets in planting holes.",
                    "source": "Arid Plateau Crop Matrix"
                },
                {
                    "crop": "Pigeon Pea (Toor Dal)",
                    "suitability": "⭐ DEEP TAPROOT: Deep taproot helps break sub-surface layers over time and fixes nitrogen.",
                    "trade_offs": "Slower early establishment phase.",
                    "source": "Legume Resilience Study"
                },
                {
                    "crop": "Sweet Potato",
                    "suitability": "⭐ WATERLOGGING CONTROL: Thrives on mounded ridge systems that prevent water pooling.",
                    "trade_offs": "Requires well-constructed raised beds.",
                    "source": "Drainage Farming Guide"
                },
                {
                    "crop": "Sorghum (Jowar)",
                    "suitability": "⭐ WEATHER ADAPTIVE: Resilient against unexpected dry spells and late rainy season starts.",
                    "trade_offs": "Sensitive to extreme waterlogging if drainage fails.",
                    "source": "Semi-Arid Agronomy Notes"
                }
            ]
            
        return {"crops": relevant_crops}
        
    return {"stage_info": stage_node, "items": items}

def evaluate_readiness_gate(user_inputs, tool_penetrated=False, water_retained=False):
    """Evaluates whether the readiness gate passes based on explicit observable checks."""
    if not tool_penetrated or not water_retained:
        return {
            "status": "failed",
            "explanation": "Readiness check failed: Hand tool must penetrate to hand's depth (~15 cm) and water bucket test must show retention."
        }
    return {
        "status": "passed",
        "explanation": "Readiness gate cleared successfully. Observable soil preparation checks verified."
    }