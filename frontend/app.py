import streamlit as st
import os
import sys

# Ensure project root is in path for engine imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Attempt to connect to reasoning engine
engine_connected = False
engine_module = None
try:
    from engine import reasoning
    engine_module = reasoning
    engine_connected = True
except ImportError:
    engine_connected = False

# Configure Streamlit Page
st.set_page_config(
    page_title="TERRAFORM: Lateritic Hardpan Plateau Survival System",
    page_icon="🌱",
    layout="centered"
)

# Define the Nine Stages in Order
STAGES = [
    "1. Input Echo",
    "2. Missing Analysis",
    "3. Fix Protocol",
    "4. Next Action / Readiness Gate",
    "5. Crop Suggestions",
    "6. Timeframe",
    "7. Planting Method",
    "8. Ongoing Care",
    "9. Harvest & Regeneration"
]

# Initialize Session State
if "current_stage_idx" not in st.session_state:
    st.session_state.current_stage_idx = 0

if "soil_inputs" not in st.session_state:
    st.session_state.soil_inputs = {
        "description": "",
        "image": None,
        "soil_color": "Reddish",
        "surface_texture": "Gravelly",
        "subsurface_layer": "Continuous hardpan / rock",
        "water_behavior": "Fast runoff",
        "visible_vegetation": "Sparse dry grass",
        "local_advice": "No local advice available",
        "available_resources": "Hand tools, organic compost",
        "checks_performed": "Hand depth test (~10 cm)"
    }

if "readiness_status" not in st.session_state:
    st.session_state.readiness_status = "unverified"  # options: unverified, failed, passed

# --- Sidebar: Navigation & Status ---
st.sidebar.title("🌱 TERRAFORM")
st.sidebar.markdown("**Case Study:** Lateritic Hardpan Plateau")
st.sidebar.markdown("---")

# Engine Connection Indicator
if engine_connected:
    st.sidebar.success("🔗 Reasoning Engine: Connected")
else:
    st.sidebar.warning("⚠️ Reasoning Engine: Standalone UI Mode")

st.sidebar.markdown("### Mission Stages")
for idx, stage_name in enumerate(STAGES):
    if idx == st.session_state.current_stage_idx:
        st.sidebar.markdown(f"👉 **{stage_name}**")
    elif idx < st.session_state.current_stage_idx:
        st.sidebar.markdown(f"✅ ~~{stage_name}~~")
    else:
        st.sidebar.markdown(f"🔒 {stage_name}")

progress_val = (st.session_state.current_stage_idx + 1) / len(STAGES)
st.sidebar.progress(progress_val)

# --- Main Interface Header ---
st.title("🌱 TERRAFORM Survival System")
st.subheader(f"Stage {st.session_state.current_stage_idx + 1}: {STAGES[st.session_state.current_stage_idx]}")
st.markdown("---")

current_idx = st.session_state.current_stage_idx

# Helper function to get structured engine results if available, else fallback structures
def fetch_engine_results(stage_name_key):
    if engine_connected and hasattr(engine_module, "evaluate_stage_data"):
        try:
            return engine_module.evaluate_stage_data(stage_name_key, st.session_state.soil_inputs)
        except Exception:
            return None
    return None

# ==========================================
# STAGE 1: Input Echo
# ==========================================
if current_idx == 0:
    st.markdown("### Stage 1: Input Echo")
    st.info("Record field observations supplied directly by the survivor. Use everyday measures (hand's depth, bucketful, pace). Mark items as unknown or unchecked if data is missing.")
    
    with st.form("input_echo_form"):
        desc = st.text_area(
            "Survivor's description of the land:",
            value=st.session_state.soil_inputs["description"],
            placeholder="e.g., Shallow, reddish, gravelly soil with a hard layer close to the surface."
        )
        
        uploaded_file = st.file_uploader(
            "Optional site image upload (organizer provided):", 
            type=["png", "jpg", "jpeg"]
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            color = st.text_input(
                "Observed soil color:",
                value=st.session_state.soil_inputs["soil_color"],
                placeholder="e.g., Reddish brown"
            )
            texture = st.text_input(
                "Surface texture:",
                value=st.session_state.soil_inputs["surface_texture"],
                placeholder="e.g., Gravelly, coarse"
            )
            subsurface = st.selectbox(
                "Subsurface layer observed:",
                ["Not checked / Unknown", "Loose gravel", "Continuous hardpan / rock", "Both loose gravel and hardpan"],
                index=["Not checked / Unknown", "Loose gravel", "Continuous hardpan / rock", "Both loose gravel and hardpan"].index(st.session_state.soil_inputs["subsurface_layer"])
            )
        with col_b:
            water = st.selectbox(
                "Water behavior during rain:",
                ["Not checked / Unknown", "Fast runoff", "Pooling", "Both runoff and pooling"],
                index=["Not checked / Unknown", "Fast runoff", "Pooling", "Both runoff and pooling"].index(st.session_state.soil_inputs["water_behavior"])
            )
            advice = st.selectbox(
                "Local farming advice status:",
                ["Unknown / Not checked", "Reliable local advice available", "No local advice available"],
                index=["Unknown / Not checked", "Reliable local advice available", "No local advice available"].index(st.session_state.soil_inputs["local_advice"])
            )
        
        vegetation = st.text_input(
            "Visible vegetation / weeds:",
            value=st.session_state.soil_inputs["visible_vegetation"],
            placeholder="e.g., Sparse dry grass, stunted shrubs"
        )
        resources = st.text_input(
            "Materials and resources available:",
            value=st.session_state.soil_inputs["available_resources"],
            placeholder="e.g., Hand tools (trowel, pickaxe), organic compost, buckets"
        )
        checks = st.text_input(
            "Observations or checks already performed:",
            value=st.session_state.soil_inputs["checks_performed"],
            placeholder="e.g., Hand depth test (~10 cm), bucketful water test"
        )
        
        submitted = st.form_submit_button("Confirm & Save Input Echo")
        if submitted:
            st.session_state.soil_inputs["description"] = desc
            st.session_state.soil_inputs["soil_color"] = color
            st.session_state.soil_inputs["surface_texture"] = texture
            st.session_state.soil_inputs["subsurface_layer"] = subsurface
            st.session_state.soil_inputs["water_behavior"] = water
            st.session_state.soil_inputs["visible_vegetation"] = vegetation
            st.session_state.soil_inputs["local_advice"] = advice
            st.session_state.soil_inputs["available_resources"] = resources
            st.session_state.soil_inputs["checks_performed"] = checks
            if uploaded_file is not None:
                st.session_state.soil_inputs["image"] = uploaded_file
            st.success("Input Echo saved successfully! Click 'Next Stage ➡️' below.")
    
    if st.session_state.soil_inputs["image"] is not None:
        st.markdown("---")
        st.markdown("#### Uploaded Site Image Inspection")
        st.image(st.session_state.soil_inputs["image"], caption="Survivor Site Photo (Visual inspection only)", use_container_width=True)

# ==========================================
# STAGE 2: Missing Analysis
# ==========================================
elif current_idx == 1:
    st.markdown("### Stage 2: Missing Analysis")
    st.write("Strictly separating direct observations from inferences and unknowns based on survivor inputs.")
    
    engine_data = fetch_engine_results("stage_2")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**👁️ Observations**")
        st.write(f"- Description: {st.session_state.soil_inputs['description'] or 'None provided'}")
        st.write(f"- Color/Texture: {st.session_state.soil_inputs['soil_color']} / {st.session_state.soil_inputs['surface_texture']}")
        st.write(f"- Subsurface: {st.session_state.soil_inputs['subsurface_layer']}")
        st.write(f"- Water Flow: {st.session_state.soil_inputs['water_behavior']}")
    with col2:
        st.markdown("**🧠 Inferences**")
        st.write("- Shallow iron/aluminum oxide layer limits root expansion.")
        st.write("- High runoff risk during short intense rainfall periods.")
        if engine_data and "inferences" in engine_data:
            for inf in engine_data["inferences"]:
                st.write(f"- {inf}")
    with col3:
        st.markdown("**❓ Unknowns & Missing Checks**")
        st.write(f"- Local Advice: {st.session_state.soil_inputs['local_advice']}")
        st.write("- Exact soil chemical pH value (untested without instruments).")
        st.write(f"- Unchecked Items: {st.session_state.soil_inputs['subsurface_layer'] if 'Not checked' in st.session_state.soil_inputs['subsurface_layer'] else 'None marked unknown'}")

# ==========================================
# STAGE 3: Fix Protocol
# ==========================================
elif current_idx == 2:
    st.markdown("### Stage 3: Fix Protocol")
    st.write("Condition-dependent soil preparation, organic fertility improvement, and runoff management:")
    
    sub_layer = st.session_state.soil_inputs["subsurface_layer"]
    water_beh = st.session_state.soil_inputs["water_behavior"]
    
    if "Continuous hardpan" in sub_layer:
        st.warning("⚠️ **Hardpan Remediation Protocol:** Do not attempt deep plowing. Target hardpan breaking at grid points spaced 2 paces apart using heavy hand tools. Apply 1 bucketful of organic compost or decomposed leaf litter per planting pit.")
    elif "Loose gravel" in sub_layer:
        st.info("ℹ️ **Gravel Layer Protocol:** Incorporate organic matter (2 bucketfuls per square pace) and establish stone contour bunds.")
    else:
        st.info("ℹ️ **Subsurface Unchecked:** Perform hand tool test to determine if hardpan or loose gravel exists before applying soil amendments.")
        
    if "runoff" in water_beh.lower():
        st.write("- **Runoff Management:** Dig shallow contour trenches (one hand's depth deep) across the slope every 3 paces to capture and infiltrate heavy rainfall.")
    elif "pooling" in water_beh.lower():
        st.write("- **Water Pooling Management:** Construct raised planting beds or ridges (hand's depth high) to prevent waterlogging around plant root zones.")
    else:
        st.write("- **Drainage Management:** Monitor water movement during initial rain to decide between contour trenches and raised ridges.")

# ==========================================
# STAGE 4: Next Action / Readiness Gate
# ==========================================
elif current_idx == 3:
    st.markdown("### Stage 4: Next Action / Readiness Gate")
    st.write("Before unlocking crop suggestions and planting recommendations, verify soil readiness using everyday observable checks:")
    
    st.markdown("""
    * **Check 1 (Tool Penetration):** Sturdy hand tool penetrates easily to hand's depth (~15 cm) after organic amendment and crust fracturing.
    * **Check 2 (Moisture Retention):** Bucketful water test shows water is absorbed within the planting pocket rather than instantly washing away across the surface.
    """)
    
    status = st.session_state.readiness_status
    if status == "unverified":
        st.warning("⚠️ Status: **Unverified**. Perform physical checks in your field before declaring readiness.")
    elif status == "failed":
        st.error("❌ Status: **Readiness Failed**. Soil still resists tool penetration or water runs off instantly. Re-apply Fix Protocol (Stage 3).")
    else:
        st.success("✅ Status: **Readiness Passed!** Soil preparation verified successfully. Crop suggestions and planting methods are now unlocked.")
        
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Mark Readiness PASSED"):
            st.session_state.readiness_status = "passed"
            st.rerun()
    with col_b:
        if st.button("Mark Readiness FAILED"):
            st.session_state.readiness_status = "failed"
            st.rerun()

# ==========================================
# STAGES 5 - 9 (Locked behind Readiness Gate)
# ==========================================
else:
    if st.session_state.readiness_status != "passed":
        st.error("🔒 **Readiness Gate Locked:** Crop suggestions and planting protocols are locked until soil preparation passes in Stage 4.")
        st.info("Please navigate back to Stage 4 (Next Action / Readiness Gate) to verify and pass your soil readiness checks.")
    else:
        st.success("🔓 **Readiness Gate Cleared:** Active recommendations fully unlocked.")
        
        # Stage 5: Crop Suggestions
        # Stage 5: Crop Suggestions
        if current_idx == 4:
            st.markdown("### Stage 5: Crop Suggestions")
            st.write("Adaptive crop options dynamically selected by reasoning engine based on your site conditions:")
            
            crop_results = fetch_engine_results("stage_5_crop_suggestions")
            
            crops_list = []
            if crop_results and "crops" in crop_results and crop_results["crops"]:
                crops_list = crop_results["crops"]
            else:
                # Direct fallback if reasoning engine function is offline
                crops_list = [
                    {
                        "crop": "Finger Millet (Ragi)",
                        "suitability": "⭐ HIGH RESILIENCE: Excellent tolerance for acidic, gravelly soils.",
                        "trade_offs": "Requires organic compost pockets in planting holes.",
                        "source": "Arid Plateau Crop Matrix"
                    },
                    {
                        "crop": "Pigeon Pea (Toor Dal)",
                        "suitability": "⭐ DEEP TAPROOT: Deep taproot helps break sub-surface layers over time.",
                        "trade_offs": "Slower early establishment phase.",
                        "source": "Legume Resilience Study"
                    },
                    {
                        "crop": "Sweet Potato",
                        "suitability": "⭐ WATERLOGGING CONTROL: Thrives on mounded ridge systems.",
                        "trade_offs": "Requires well-constructed raised beds.",
                        "source": "Drainage Farming Guide"
                    },
                    {
                        "crop": "Sorghum (Jowar)",
                        "suitability": "⭐ WEATHER ADAPTIVE: Resilient against unexpected dry spells.",
                        "trade_offs": "Sensitive to waterlogging if drainage fails.",
                        "source": "Semi-Arid Agronomy Notes"
                    }
                ]

            for crop_info in crops_list:
                st.markdown(f"#### 🌾 {crop_info['crop']}")
                st.write(f"- **Suitability:** {crop_info['suitability']}")
                st.write(f"- **Trade-offs / Requirements:** {crop_info['trade_offs']}")
                st.caption(f"Source: {crop_info.get('source', 'Knowledge Base')}")
                st.markdown("---")

        # Stage 6: Timeframe
        elif current_idx == 5:
            st.markdown("### Stage 6: Timeframe")
            st.write("Remediation, establishment, maturity ranges, and seasonal buffer information:")
            st.markdown("""
            * **Remediation & Soil Preparation Phase:** 3 to 7 days (organic composting and crust fracturing).
            * **Crop Establishment Phase:** First 15 to 30 days post-germination.
            * **Realistic Maturity Ranges:**
              * *Finger Millet:* 90 to 120 days
              * *Pigeon Pea:* 150 to 180 days
              * *Sweet Potato:* 90 to 120 days
              * *Sorghum:* 100 to 130 days
            * **Seasonal Buffer:** Adjust sowing schedule if late rains or unexpected dry spells occur during the early establishment window.
            """)

        # Stage 7: Planting Method
        elif current_idx == 6:
            st.markdown("### Stage 7: Planting Method")
            st.write("Applicable bed or pit preparation, planting guidance, and water conservation:")
            st.markdown("""
            * **Sloping Terrain:** Plant in zai pits or half-moon micro-catchments spaced 2 paces apart along contour lines to trap scarce rainfall.
            * **Flat Terrain / Pooling:** Plant on raised ridges constructed to a hand's depth height to prevent root rot.
            * **Sowing Depth:** Place seeds at a shallow depth (approx. one finger-joint) to allow easy emergence through amended topsoil pockets.
            """)

        # Stage 8: Ongoing Care
        elif current_idx == 7:
            st.markdown("### Stage 8: Ongoing Care")
            st.write("Growth-stage care, organic fertility, dry-spell measures, and pest monitoring:")
            st.markdown("""
            * **Moisture Conservation:** Apply organic mulch (dry leaf litter or grass) two hand-spans wide around plant bases to reduce evaporation during unexpected dry spells.
            * **Weed Management:** Perform manual weeding early in the rainy season to eliminate competition for scarce moisture and nutrients.
            * **Pest Monitoring:** Inspect leaf undersides weekly for common dryland pests; apply organic deterrents (e.g., neem-based sprays) if infestation occurs.
            """)

        # Stage 9: Harvest & Regeneration
        elif current_idx == 8:
            st.markdown("### Stage 9: Harvest & Regeneration")
            st.write("Visible harvest signs, harvesting guidance, storage advice, and post-harvest regeneration:")
            st.markdown("""
            * **Visible Harvest Signs:** Grain hardening for millets, pod drying for pigeon peas, or tuber skin firming for sweet potatoes.
            * **Harvesting Guidance:** Harvest mature crops without deep tilling to preserve soil aggregates. Cut stalks cleanly at ground level.
            * **Post-Harvest Regeneration:** Retain crop stubble and incorporate organic green matter post-harvest to regenerate acidity-stressed soil structure for the next season.
            """)

st.markdown("---")
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("⬅️ Previous Stage", disabled=(current_idx == 0)):
        st.session_state.current_stage_idx -= 1
        st.rerun()
with col_next:
    if st.button("Next Stage ➡️", disabled=(current_idx == len(STAGES) - 1)):
        # Enforce strict lock on moving past stage 4 if readiness not passed
        if current_idx == 3 and st.session_state.readiness_status != "passed":
            st.warning("Cannot proceed past Readiness Gate until soil preparation status is PASSED.")
        else:
            st.session_state.current_stage_idx += 1
            st.rerun()