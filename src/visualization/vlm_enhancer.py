"""
VLM Enhancer Module - Uses Groq API via LangChain to enhance visualizations
This is the next-level enhancement layer that improves LLM-generated visualizations
using Vision Language Model capabilities.
"""

from typing import Dict, Any, Optional, Tuple
import os
import json
import base64
import io
import plotly.graph_objects as go
from langchain_core.messages import HumanMessage
import pandas as pd
from utils.logger import get_logger
from utils.exceptions import VisualizationError

logger = get_logger(__name__)


class GroqVLMEnhancer:
    """
    Enhances visualizations using Groq API via LangChain.
    Analyzes existing visualizations and suggests improvements.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "mixtral-8x7b-32768"):
        """
        Initialize Groq VLM Enhancer.
        
        Args:
            api_key: Groq API key (defaults to GROK_API_KEY env var)
            model: Model to use (mixtral-8x7b-32768 for fast inference)
        """
        self.api_key = api_key or os.getenv("GROK_API_KEY", "").strip('"')
        self.model_name = model
        
        if not self.api_key:
            logger.debug(f"Available env vars: {list(os.environ.keys())}")
            raise ValueError("GROK_API_KEY environment variable not set")
        
        # Initialize LangChain Groq client
        try:
            from langchain_groq import ChatGroq
            self.llm = ChatGroq(
                model=model,
                api_key=self.api_key,
                temperature=0.3
            )
            logger.info(f"Initialized Groq VLM with model: {model}")
        except ImportError:
            logger.error("langchain-groq not installed. Install with: uv pip install langchain-groq")
            raise

    def encode_figure_to_base64(self, fig: go.Figure) -> str:
        """
        Encode Plotly figure as base64 image for LangChain transmission.
        
        Args:
            fig: Plotly Figure object
            
        Returns:
            Base64 encoded image string
        """
        try:
            # Convert figure to image bytes
            img_bytes = fig.to_image(format="png", width=800, height=600)
            
            # Encode to base64
            b64_string = base64.b64encode(img_bytes).decode('utf-8')
            logger.info("Encoded figure to base64")
            return b64_string
        except Exception as e:
            logger.error(f"Error encoding figure: {str(e)}")
            raise VisualizationError(f"Failed to encode visualization: {str(e)}")

    def analyze_visualization(
        self,
        fig: go.Figure,
        data: pd.DataFrame,
        problem_statement: str,
        viz_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze visualization using Groq VLM.
        
        Args:
            fig: Plotly Figure to analyze
            data: Original DataFrame
            problem_statement: User's problem statement
            viz_spec: Visualization specification from LLM
            
        Returns:
            Dictionary with analysis results:
            {
                'clarity_score': float (0-100),
                'effectiveness_score': float (0-100),
                'insights': str,
                'improvements': List[str],
                'enhancement_recommendations': Dict
            }
        """
        try:
            # Encode figure
            fig_b64 = self.encode_figure_to_base64(fig)
            
            # Create analysis prompt
            analysis_prompt = f"""
Analyze this data visualization as an expert in information design and data storytelling.

CONTEXT:
- Problem Statement: {problem_statement}
- Data Shape: {data.shape[0]} rows × {data.shape[1]} columns
- Visualization Type: {viz_spec.get('type', 'unknown')}
- Chart Title: {viz_spec.get('title', 'Untitled')}
- Visualization Description: {viz_spec.get('description', 'No description')}

ANALYSIS REQUIREMENTS:
1. Assess clarity (how easily viewers understand the visualization)
2. Assess effectiveness (how well it addresses the problem statement)
3. Identify key insights visible in the visualization
4. Suggest specific, actionable improvements
5. Recommend enhancements that would take this visualization to the next level

Provide structured JSON response with keys:
- clarity_score (0-100)
- effectiveness_score (0-100)
- insights (List of 2-3 key findings)
- improvements (List of 3-5 specific improvements)
- enhancement_recommendations (Dict with specific visual enhancements)

Focus on practical, implementable suggestions.
"""
            
            # Create message with image for VLM
            message = HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{fig_b64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": analysis_prompt
                    }
                ]
            )
            
            # Get response from Groq
            response = self.llm.invoke([message])
            response_text = response.content
            
            # Parse JSON response
            try:
                # Extract JSON from response (may be wrapped in markdown code blocks)
                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    json_str = response_text.split("```")[1].split("```")[0]
                else:
                    json_str = response_text
                
                analysis_result = json.loads(json_str)
                logger.info(f"VLM analysis complete: clarity={analysis_result.get('clarity_score')}, effectiveness={analysis_result.get('effectiveness_score')}")
                return analysis_result
            
            except json.JSONDecodeError:
                logger.warning("Could not parse VLM response as JSON, returning raw text")
                return {
                    "clarity_score": 75,
                    "effectiveness_score": 75,
                    "insights": response_text,
                    "improvements": [],
                    "enhancement_recommendations": {}
                }
        
        except Exception as e:
            logger.error(f"Error analyzing visualization: {str(e)}")
            raise VisualizationError(f"Failed to analyze visualization with VLM: {str(e)}")

    def generate_enhanced_specification(
        self,
        original_spec: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate enhanced visualization specification based on VLM analysis.
        
        Args:
            original_spec: Original LLM visualization spec
            analysis: VLM analysis results
            
        Returns:
            Enhanced specification with improvements
        """
        try:
            enhanced_spec = original_spec.copy()
            
            # Add enhancement metadata
            enhanced_spec['enhancements'] = {
                'clarity_score': analysis.get('clarity_score', 75),
                'effectiveness_score': analysis.get('effectiveness_score', 75),
                'vlm_insights': analysis.get('insights', []),
                'recommended_improvements': analysis.get('improvements', []),
                'visual_enhancements': analysis.get('enhancement_recommendations', {})
            }
            
            # Apply specific enhancements based on scores
            recommendations = analysis.get('enhancement_recommendations', {})
            
            # Title enhancement
            if recommendations.get('title_enhancement'):
                enhanced_spec['title'] = f"{original_spec.get('title', '')} - {recommendations['title_enhancement']}"
            
            # Color enhancement
            if recommendations.get('color_scheme'):
                enhanced_spec['color_scheme'] = recommendations['color_scheme']
            
            # Annotation suggestions
            if recommendations.get('annotations'):
                enhanced_spec['suggested_annotations'] = recommendations['annotations']
            
            logger.info(f"Generated enhanced specification with {len(enhanced_spec.get('enhancements', {}))} enhancements")
            return enhanced_spec
        
        except Exception as e:
            logger.error(f"Error generating enhanced spec: {str(e)}")
            return original_spec

    def enhance_figure_with_annotations(
        self,
        fig: go.Figure,
        enhancements: Dict[str, Any]
    ) -> go.Figure:
        """
        Apply VLM-suggested enhancements to figure.
        
        Args:
            fig: Original Plotly Figure
            enhancements: Enhancement recommendations from VLM
            
        Returns:
            Enhanced Plotly Figure
        """
        try:
            enhanced_fig = fig
            
            # Add annotations if suggested
            annotations = enhancements.get('suggested_annotations', [])
            for annotation in annotations:
                enhanced_fig.add_annotation(
                    text=annotation.get('text', ''),
                    xref=annotation.get('xref', 'paper'),
                    yref=annotation.get('yref', 'paper'),
                    x=annotation.get('x', 0.5),
                    y=annotation.get('y', 0.5),
                    showarrow=annotation.get('showarrow', True),
                    arrowhead=2,
                    font=dict(size=10, color='darkblue')
                )
            
            # Apply title enhancement if present
            if 'title' in enhancements:
                enhanced_fig.update_layout(title_text=enhancements['title'])
            
            # Apply color scheme if suggested
            color_scheme = enhancements.get('color_scheme', {})
            if color_scheme:
                enhanced_fig.update_traces(
                    marker_color=color_scheme.get('marker_color'),
                    line_color=color_scheme.get('line_color')
                )
            
            logger.info("Applied annotations and enhancements to figure")
            return enhanced_fig
        
        except Exception as e:
            logger.error(f"Error enhancing figure: {str(e)}")
            return fig

    def end_to_end_enhancement(
        self,
        fig: go.Figure,
        data: pd.DataFrame,
        problem_statement: str,
        viz_spec: Dict[str, Any]
    ) -> Tuple[go.Figure, Dict[str, Any]]:
        """
        Complete enhancement pipeline: analyze → recommend → enhance.
        
        Args:
            fig: Original visualization
            data: DataFrame used for visualization
            problem_statement: User's problem statement
            viz_spec: LLM visualization specification
            
        Returns:
            Tuple of (enhanced_figure, enhancement_report)
        """
        try:
            # Step 1: Analyze
            logger.info("Step 1: Analyzing visualization with Groq VLM...")
            analysis = self.analyze_visualization(fig, data, problem_statement, viz_spec)
            
            # Step 2: Generate enhanced spec
            logger.info("Step 2: Generating enhanced specification...")
            enhanced_spec = self.generate_enhanced_specification(viz_spec, analysis)
            
            # Step 3: Apply enhancements
            logger.info("Step 3: Applying enhancements to figure...")
            enhanced_fig = self.enhance_figure_with_annotations(
                fig,
                enhanced_spec.get('enhancements', {})
            )
            
            # Create report
            report = {
                'original_spec': viz_spec,
                'enhanced_spec': enhanced_spec,
                'vlm_analysis': analysis,
                'enhancement_status': 'completed'
            }
            
            logger.info("Enhancement pipeline completed successfully")
            return enhanced_fig, report
        
        except Exception as e:
            logger.error(f"Error in enhancement pipeline: {str(e)}")
            return fig, {
                'original_spec': viz_spec,
                'vlm_analysis': {'error': str(e)},
                'enhancement_status': 'failed'
            }


# Alias for backward compatibility
VLMEnhancer = GroqVLMEnhancer
