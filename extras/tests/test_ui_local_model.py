"""
Test script for UI components related to local model integration
"""

import streamlit as st
import sys

def test_ui():
    """
    Simple Streamlit app to test the UI components related to local models
    """
    st.title("DeFacture Local Model Test")
    
    st.write("## Testing Local Model UI Integration")
    
    # Check if local models are available
    has_local_models = False
    try:
        import torch
        import importlib.util
        transformers_spec = importlib.util.find_spec("transformers")
        has_local_models = transformers_spec is not None
        
        if has_local_models:
            st.success("✅ Local model dependencies detected (PyTorch and Transformers)")
        else:
            st.error("❌ Local model dependencies missing")
    except ImportError:
        st.error("❌ Could not import required packages")
        has_local_models = False
    
    # Define model options and their descriptions
    model_options = [
        {"id": "phi-2-local", 
         "name": f"Phi-2 (Local){' ✓' if has_local_models else ' ⚠️'}", 
         "desc": "Uses locally cached Phi-2 model (fastest, best quality)" if has_local_models else "Local model requires PyTorch and Transformers (not detected)"},
        {"id": "phi-2", 
         "name": "Phi-2 (API)", 
         "desc": "Uses Hugging Face API with Phi-2 (good quality, uses API quota)"},
        {"id": "bart", 
         "name": "BART (API)", 
         "desc": "Uses Hugging Face API with BART (simpler analysis)"},
        {"id": "mock", 
         "name": "Mock Data", 
         "desc": "Uses mock data (no model, for testing only)"}
    ]
    
    # Create radio buttons with descriptions
    st.write("### Model Selection UI")
    selected_option = st.radio(
        "Context Analysis Model",
        options=[opt["id"] for opt in model_options],
        format_func=lambda x: next((opt["name"] for opt in model_options if opt["id"] == x), x),
        index=0
    )
    
    # Show description for selected model
    selected_desc = next((opt["desc"] for opt in model_options if opt["id"] == selected_option), "")
    st.caption(selected_desc)
    
    # Show the model source with icon and styling
    st.write("### Model Source Indicator")
    if selected_option == "phi-2-local":
        model_source = "Local"
        model_icon = "💻"
        color = "green"
    elif selected_option == "mock":
        model_source = "Mock"
        model_icon = "🔄"
        color = "gray"
    else:
        model_source = "API"
        model_icon = "🌐"
        color = "blue"
    
    model_name = selected_option.split('-')[0].upper()
    st.markdown(f"<div style='color: {color}; font-size: 0.9em;'>{model_icon} Analysis performed using: <b>{model_name}</b> ({model_source})</div>", unsafe_allow_html=True)
    
    # Test result
    st.write("### Test Result")
    st.success("✅ UI components rendered successfully")

if __name__ == "__main__":
    test_ui()