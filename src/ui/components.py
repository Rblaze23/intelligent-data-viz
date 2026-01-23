"""
UI Components Module - Reusable Streamlit components
"""

import streamlit as st
from typing import Any, List, Dict, Optional, Callable
import plotly.graph_objects as go
from utils.logger import get_logger

logger = get_logger(__name__)


class UIComponents:
    """Collection of reusable UI components."""

    @staticmethod
    def data_preview(df, title: str = "Data Preview", max_rows: int = 5):
        """Display data preview."""
        with st.expander(title):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            
            st.dataframe(df.head(max_rows), use_container_width=True)
            
            with st.expander("Column Info"):
                for col in df.columns:
                    st.write(f"**{col}**: {df[col].dtype}")

    @staticmethod
    def problem_statement_input() -> str:
        """Input component for problem statement."""
        st.subheader("📋 Define Your Problem")
        problem = st.text_area(
            "What do you want to visualize?",
            placeholder="e.g., 'Show me the relationship between house prices and square meters'",
            height=100,
            help="Be specific about what insights you're looking for"
        )
        return problem

    @staticmethod
    def visualization_tabs(
        figures: List[go.Figure],
        titles: List[str],
        descriptions: List[str],
        justifications: List[str]
    ) -> int:
        """
        Display 3 visualization proposals in tabs.
        
        Returns:
            Index of selected visualization (0-2)
        """
        st.subheader("🎨 3 Visualization Proposals")
        
        tabs = st.tabs([f"Option {i+1}" for i in range(len(figures))])
        
        for i, (tab, fig, title, desc, justif) in enumerate(
            zip(tabs, figures, titles, descriptions, justifications)
        ):
            with tab:
                # Title and description
                st.markdown(f"### {title}")
                st.markdown(f"*{desc}*")
                
                # Visualization
                st.plotly_chart(fig, use_container_width=True)
                
                # Justification
                with st.expander("📖 Why This Visualization?"):
                    st.write(justif)
                
                # Select button
                if st.button(f"✅ Select Option {i+1}", key=f"select_{i}"):
                    st.session_state.selected_viz = i
                    st.success(f"Selected Option {i+1}!")
                    return i
        
        return st.session_state.get('selected_viz', -1)

    @staticmethod
    def loading_state(message: str = "Processing..."):
        """Display loading spinner."""
        with st.spinner(message):
            yield

    @staticmethod
    def error_message(message: str, title: str = "❌ Error"):
        """Display error message."""
        st.error(f"**{title}**\n{message}")

    @staticmethod
    def success_message(message: str, title: str = "✅ Success"):
        """Display success message."""
        st.success(f"**{title}**\n{message}")

    @staticmethod
    def info_message(message: str, title: str = "ℹ️ Info"):
        """Display info message."""
        st.info(f"**{title}**\n{message}")

    @staticmethod
    def visualization_stats(fig: go.Figure, data_points: int):
        """Display visualization statistics."""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Data Points", data_points)
        with col2:
            st.metric("Dimensions", len(fig.data))
        with col3:
            trace_types = set(trace.type for trace in fig.data)
            st.metric("Trace Types", len(trace_types))

    @staticmethod
    def export_options(png_path: Optional[str] = None, html_path: Optional[str] = None):
        """Display export buttons."""
        st.subheader("💾 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if png_path:
                with open(png_path, "rb") as f:
                    st.download_button(
                        label="📥 Download PNG",
                        data=f.read(),
                        file_name="visualization.png",
                        mime="image/png"
                    )
            else:
                st.button("📥 Download PNG", disabled=True)
        
        with col2:
            if html_path:
                with open(html_path, "rb") as f:
                    st.download_button(
                        label="📥 Download HTML",
                        data=f.read(),
                        file_name="visualization.html",
                        mime="text/html"
                    )
            else:
                st.button("📥 Download HTML", disabled=True)

    @staticmethod
    def enhancement_report(analysis: Dict[str, Any]):
        """Display VLM enhancement analysis."""
        st.subheader("✨ VLM Enhancement Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            clarity = analysis.get('clarity_score', 75)
            st.metric("Clarity Score", f"{clarity}/100", delta=clarity - 75)
        
        with col2:
            effectiveness = analysis.get('effectiveness_score', 75)
            st.metric("Effectiveness Score", f"{effectiveness}/100", delta=effectiveness - 75)
        
        # Insights
        with st.expander("🔍 VLM Insights"):
            insights = analysis.get('insights', [])
            if isinstance(insights, list):
                for insight in insights:
                    st.write(f"• {insight}")
            else:
                st.write(insights)
        
        # Improvements
        with st.expander("💡 Recommended Improvements"):
            improvements = analysis.get('improvements', [])
            if isinstance(improvements, list):
                for i, improvement in enumerate(improvements, 1):
                    st.write(f"{i}. {improvement}")
            else:
                st.write(improvements)
        
        # Enhancement recommendations
        with st.expander("🎯 Enhancement Recommendations"):
            recommendations = analysis.get('enhancement_recommendations', {})
            if recommendations:
                st.json(recommendations)
            else:
                st.write("No specific recommendations at this time")

    @staticmethod
    def sidebar_info():
        """Display sidebar information."""
        with st.sidebar:
            st.markdown("---")
            st.markdown("## ℹ️ About")
            st.markdown("""
This application uses:
- **LLM**: For analyzing data and recommending visualizations
- **VLM**: For enhancing visualizations to next level
- **Plotly**: For interactive visualizations
- **Grok API**: For vision-language model capabilities
""")
            
            st.markdown("---")
            st.markdown("## 📚 Tips")
            st.markdown("""
1. Be specific in your problem statement
2. Review all 3 visualization options
3. Check the VLM enhancement analysis
4. Export your final visualization
""")

    @staticmethod
    def footer():
        """Display footer."""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center'>
            <p>Made with ❤️ by Person 2 - Data Visualization Lead</p>
            <p>Powered by Streamlit, Plotly, and Grok Vision API</p>
        </div>
        """, unsafe_allow_html=True)
