"""
Main Streamlit Application
Person 2 - Visualization & Frontend Lead

This application orchestrates:
1. CSV upload and data preview
2. Problem statement input
3. LLM-based visualization proposals (from Person 1)
4. VLM enhancement using Grok API (Person 2 enhancement)
5. Interactive visualization display
6. Export functionality
"""

import streamlit as st
import pandas as pd
import os
from typing import List, Dict, Any, Optional
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from visualization.generator import VisualizationGenerator
from visualization.styler import Styler
from visualization.exporter import VisualizationExporter
from visualization.vlm_enhancer import GroqVLMEnhancer
from ui.components import UIComponents
from utils.logger import get_logger
from utils.exceptions import VisualizationError, VLMError

logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Intelligent Data Visualization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# Session state initialization
def init_session_state():
    """Initialize session state variables."""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'problem_statement' not in st.session_state:
        st.session_state.problem_statement = ""
    if 'visualizations' not in st.session_state:
        st.session_state.visualizations = []
    if 'selected_viz' not in st.session_state:
        st.session_state.selected_viz = -1
    if 'enhancement_report' not in st.session_state:
        st.session_state.enhancement_report = None
    if 'export_paths' not in st.session_state:
        st.session_state.export_paths = {}


@st.cache_resource
def get_components():
    """Get and cache visualization components."""
    styler = Styler(theme='light', palette='primary')
    generator = VisualizationGenerator(styler=styler)
    exporter = VisualizationExporter(output_dir="./exports")
    
    try:
        vlm_enhancer = GroqVLMEnhancer()
    except ValueError:
        logger.warning("Grok API key not configured, VLM enhancement will be disabled")
        vlm_enhancer = None
    
    return {
        'styler': styler,
        'generator': generator,
        'exporter': exporter,
        'vlm_enhancer': vlm_enhancer
    }


def main():
    """Main application logic."""
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Intelligent Data Visualization System</h1>
        <p>Upload data → Define problem → Get AI-powered visualizations → Enhance with Vision AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    UIComponents.sidebar_info()
    
    # Main workflow
    with st.container():
        # Step 1: Data Upload
        st.header("Step 1️⃣ Upload Your Data")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with your data"
        )
        
        if uploaded_file is not None:
            try:
                st.session_state.data = pd.read_csv(uploaded_file)
                st.success("✅ Data loaded successfully!")
                
                # Data preview
                UIComponents.data_preview(st.session_state.data)
                
            except Exception as e:
                UIComponents.error_message(f"Failed to load data: {str(e)}")
                st.session_state.data = None
                return
        
        # Step 2: Problem Statement
        if st.session_state.data is not None:
            st.header("Step 2️⃣ Define Your Problem")
            st.session_state.problem_statement = UIComponents.problem_statement_input()
            
            # Step 3: Generate Visualizations (Mock - Would come from Person 1's LLM)
            if st.session_state.problem_statement:
                st.header("Step 3️⃣ Visualization Proposals")
                
                if st.button("🚀 Generate Visualizations", key="generate_btn"):
                    with st.spinner("Analyzing data and generating visualizations..."):
                        try:
                            components = get_components()
                            generator = components['generator']
                            
                            # Example visualizations (coordinated with Person 1's LLM output)
                            viz_specs = [
                                {
                                    'type': 'scatter',
                                    'x_col': st.session_state.data.select_dtypes(include=['number']).columns[0] if len(st.session_state.data.select_dtypes(include=['number']).columns) > 0 else st.session_state.data.columns[0],
                                    'y_col': st.session_state.data.select_dtypes(include=['number']).columns[1] if len(st.session_state.data.select_dtypes(include=['number']).columns) > 1 else st.session_state.data.columns[-1],
                                    'title': 'Scatter Plot Analysis',
                                    'description': 'Explores relationships between two variables'
                                },
                                {
                                    'type': 'bar',
                                    'x_col': st.session_state.data.columns[0],
                                    'y_col': st.session_state.data.select_dtypes(include=['number']).columns[0] if len(st.session_state.data.select_dtypes(include=['number']).columns) > 0 else st.session_state.data.columns[1],
                                    'title': 'Bar Chart Summary',
                                    'description': 'Shows distribution across categories'
                                },
                                {
                                    'type': 'heatmap',
                                    'title': 'Correlation Matrix',
                                    'description': 'Reveals relationships between all numeric variables'
                                }
                            ]
                            
                            # Generate figures
                            figures = []
                            justifications = []
                            
                            for spec in viz_specs:
                                try:
                                    fig = generator.create_from_llm_spec(st.session_state.data, spec)
                                    figures.append(fig)
                                    justifications.append(f"This {spec['type']} visualization is recommended because it directly addresses the problem: '{st.session_state.problem_statement}'")
                                except Exception as e:
                                    logger.warning(f"Could not generate {spec['type']}: {str(e)}")
                            
                            st.session_state.visualizations = figures
                            
                            if figures:
                                st.success(f"✅ Generated {len(figures)} visualization proposals!")
                            else:
                                UIComponents.error_message("Could not generate any visualizations")
                                return
                        
                        except Exception as e:
                            UIComponents.error_message(f"Error generating visualizations: {str(e)}")
                            return
                
                # Display visualizations
                if st.session_state.visualizations:
                    st.header("Step 4️⃣ Select & Enhance Visualization")
                    
                    selected_idx = UIComponents.visualization_tabs(
                        st.session_state.visualizations,
                        [f"Option {i+1}" for i in range(len(st.session_state.visualizations))],
                        ["Description 1", "Description 2", "Description 3"][:len(st.session_state.visualizations)],
                        ["Justification 1", "Justification 2", "Justification 3"][:len(st.session_state.visualizations)]
                    )
                    
                    # VLM Enhancement
                    if selected_idx >= 0:
                        st.subheader("✨ AI-Powered Enhancement")
                        
                        components = get_components()
                        vlm_enhancer = components['vlm_enhancer']
                        
                        if vlm_enhancer:
                            if st.button("🔮 Enhance with Grok VLM", key="enhance_btn"):
                                with st.spinner("Using Vision Language Model to enhance visualization..."):
                                    try:
                                        fig = st.session_state.visualizations[selected_idx]
                                        viz_spec = {
                                            'type': 'enhanced',
                                            'title': 'Enhanced Visualization',
                                            'description': 'VLM-enhanced version'
                                        }
                                        
                                        enhanced_fig, report = vlm_enhancer.end_to_end_enhancement(
                                            fig,
                                            st.session_state.data,
                                            st.session_state.problem_statement,
                                            viz_spec
                                        )
                                        
                                        st.session_state.visualizations[selected_idx] = enhanced_fig
                                        st.session_state.enhancement_report = report.get('vlm_analysis', {})
                                        
                                        st.success("✅ Visualization enhanced!")
                                        
                                        # Display enhancement report
                                        if st.session_state.enhancement_report:
                                            UIComponents.enhancement_report(st.session_state.enhancement_report)
                                    
                                    except Exception as e:
                                        UIComponents.error_message(f"VLM enhancement failed: {str(e)}")
                        else:
                            st.warning("⚠️ VLM enhancement not available - Grok API key not configured")
                        
                        # Step 5: Export
                        st.header("Step 5️⃣ Export Results")
                        
                        components = get_components()
                        exporter = components['exporter']
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("📥 Export PNG (High Quality)", key="export_png"):
                                try:
                                    png_path = exporter.export_png(
                                        st.session_state.visualizations[selected_idx],
                                        f"visualization_{selected_idx}",
                                        width=1200,
                                        height=800,
                                        scale=2.0
                                    )
                                    st.session_state.export_paths['png'] = png_path
                                    st.success(f"✅ Saved to {png_path}")
                                except Exception as e:
                                    UIComponents.error_message(f"Export failed: {str(e)}")
                        
                        with col2:
                            if st.button("📥 Export HTML (Interactive)", key="export_html"):
                                try:
                                    html_path = exporter.export_html(
                                        st.session_state.visualizations[selected_idx],
                                        f"visualization_{selected_idx}"
                                    )
                                    st.session_state.export_paths['html'] = html_path
                                    st.success(f"✅ Saved to {html_path}")
                                except Exception as e:
                                    UIComponents.error_message(f"Export failed: {str(e)}")
                        
                        # Display export buttons
                        if st.session_state.export_paths:
                            UIComponents.export_options(
                                st.session_state.export_paths.get('png'),
                                st.session_state.export_paths.get('html')
                            )
    
    # Footer
    UIComponents.footer()


if __name__ == "__main__":
    main()
