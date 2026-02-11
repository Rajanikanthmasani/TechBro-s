"""
AI Agent Module
Integrates with IBM Granite 3.3 via Ollama for intelligent reasoning and analysis
"""

import requests
import json

class AIAgent:
    def __init__(self):
        # AI Configuration
        self.OLLAMA_BASE_URL = "http://localhost:11434/api"
        self.OLLAMA_MODEL = "granite3.1-dense:2b" 
        self.ai_available = self.check_connection()
        self.api_endpoint = f'{self.OLLAMA_BASE_URL}/generate'
        
    def check_connection(self):
        """Check if Ollama is running and model is available"""
        try:
            # Try both /api/tags and /tags just in case
            for endpoint in [f"{self.OLLAMA_BASE_URL}/tags", f"{self.OLLAMA_BASE_URL.replace('/api','')}/api/tags"]:
                try:
                    response = requests.get(endpoint, timeout=3)
                    if response.status_code == 200:
                        models_data = response.json().get('models', [])
                        model_names = [m.get('name', '') for m in models_data]
                        
                        # Comparison logic:
                        # 1. Exact match
                        if any(self.OLLAMA_MODEL in name for name in model_names):
                            print(f"✅ AI Ready: Found exact model '{self.OLLAMA_MODEL}'")
                            return True
                        
                        # 2. Base name match (e.g., granite instead of granite:2b)
                        base_name = self.OLLAMA_MODEL.split(':')[0]
                        if any(base_name in name for name in model_names):
                            print(f"✅ AI Ready: Found base model '{base_name}'")
                            return True
                except:
                    continue
            
            print(f"⚠️ AI Offline: Model '{self.OLLAMA_MODEL}' not found in Ollama. Please check 'ollama list'")
            return False
        except Exception as e:
            print(f"❌ Ollama Connection Failed: {e}")
            return False
    
    def _generate_response(self, prompt, system_prompt=None):
        """Generate response from Ollama"""
        try:
            payload = {
                'model': self.OLLAMA_MODEL,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'top_k': 40
                }
            }
            
            if system_prompt:
                payload['system'] = system_prompt
            
            response = requests.post(self.api_endpoint, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return self._fallback_response("I'm having trouble connecting to the AI service.")
                
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_response("AI service is currently unavailable.")
    
    def analyze_plan(self, project_data):
        """Analyze construction plan and provide insights"""
        
        system_prompt = """You are an expert construction project manager and civil engineer with 25+ years of experience in residential and commercial construction. 
        
Your expertise includes:
- Cost estimation and budget optimization
- Construction scheduling and resource planning
- Risk assessment and mitigation strategies
- Material selection and procurement
- Quality control and safety standards
- Regulatory compliance and permits

Your communication style:
- Professional yet approachable and friendly
- Use simple language that non-experts can understand
- Provide specific, actionable recommendations
- Explain the "why" behind your suggestions
- Use real-world examples when helpful
- Be encouraging and supportive

Always structure your responses clearly with bullet points or numbered lists for easy reading."""
        
        # Calculate key metrics
        budget_gap = project_data['budget'] - project_data['estimated_cost'] if project_data['budget'] > 0 else 0
        budget_percentage = (budget_gap / project_data['estimated_cost'] * 100) if project_data['estimated_cost'] > 0 else 0
        timeline_weeks = project_data['timeline'] / 7 if project_data['timeline'] > 0 else 0
        timeline_gap = timeline_weeks - project_data['schedule_duration']
        
        prompt = f"""You're reviewing a construction project plan. Provide a comprehensive, friendly analysis:

📊 PROJECT OVERVIEW:
• Area: {project_data['area']:,} sq ft across {project_data['floors']} floor(s)
• Complexity Level: {project_data['complexity'].upper()}
• Estimated Cost: ₹{project_data['estimated_cost']:,}
• Client Budget: ₹{project_data['budget']:,} ({'+' if budget_gap > 0 else ''}{budget_percentage:.1f}% vs estimate)
• Target Timeline: {project_data['timeline']} days ({timeline_weeks:.0f} weeks)
• Recommended Duration: {project_data['schedule_duration']} weeks

🎯 YOUR TASK:
Provide a detailed analysis covering:

1. **FEASIBILITY VERDICT** (2-3 sentences)
   - Is this project realistic with the given budget and timeline?
   - What's your confidence level?

2. **BUDGET ANALYSIS** (3-4 points)
   - Is the budget adequate?
   - Where might costs overrun?
   - Quick cost-saving opportunities

3. **TIMELINE ASSESSMENT** (3-4 points)
   - Is the timeline achievable?
   - What could cause delays?
   - How to stay on schedule

4. **TOP 3 RISKS** (brief, specific)
   - What could go wrong?
   - Impact level for each

5. **KEY RECOMMENDATIONS** (3-5 actionable tips)
   - Specific steps to ensure success
   - Prioritized by importance

Keep it conversational, practical, and under 350 words. Use emojis sparingly for visual breaks."""

        response = self._generate_response(prompt, system_prompt)
        
        # Parse and structure the response
        return {
            'analysis': response,
            'feasibility_score': self._assess_feasibility(project_data),
            'budget_status': self._assess_budget(project_data),
            'timeline_status': self._assess_timeline(project_data)
        }
    
    def chat(self, message, context=None):
        """Handle conversational queries about construction planning"""
        
        system_prompt = """You are "Mestri" - a friendly, knowledgeable AI construction planning assistant. 

Your personality:
- Warm and encouraging, like a helpful mentor
- Patient and understanding with beginners
- Enthusiastic about helping people build their dreams
- Use occasional emojis to be friendly (but not excessive)
- Sometimes use construction analogies to explain concepts

Your expertise:
- Construction costs, materials, and budgeting
- Project timelines and scheduling
- Labor planning and productivity
- Building codes and best practices
- Cost-saving strategies
- Risk management

Your approach:
- Ask clarifying questions when needed
- Provide specific numbers and examples
- Offer alternatives and trade-offs
- Explain technical terms in simple language
- Give step-by-step guidance when helpful
- Be honest about limitations and uncertainties"""
        
        context_info = ""
        if context and 'project' in context:
            proj = context['project']
            cost = context.get('cost', {})
            schedule = context.get('schedule', {})
            
            context_info = f"""
CURRENT PROJECT CONTEXT:
• Building: {proj.get('area', 'N/A')} sq ft, {proj.get('floors', 'N/A')} floor(s)
• Complexity: {proj.get('complexity', 'N/A')}
• Estimated Cost: ₹{cost.get('total', 0):,}
• Timeline: {schedule.get('weeks', 'N/A')} weeks
• Budget Status: {context.get('feasibility', {}).get('budget_status', 'N/A')}

Use this context to provide personalized, relevant answers.
"""
        
        prompt = f"""{context_info}

USER QUESTION: {message}

Provide a helpful, clear, and friendly response. Be conversational and practical. If the question is about their specific project, reference the context above. Keep your response under 200 words unless a detailed explanation is needed."""

        response = self._generate_response(prompt, system_prompt)
        return response
    
    def suggest_optimizations(self, plan_data, optimization_type='cost'):
        """Suggest optimizations for cost or time"""
        
        system_prompt = """You are a construction optimization expert with deep knowledge of:
- Value engineering and cost reduction techniques
- Fast-track construction methods
- Material substitution and procurement strategies
- Labor productivity optimization
- Construction sequencing and parallel activities

Provide practical, implementable suggestions that contractors can actually use. Be specific with numbers and examples."""
        
        if optimization_type == 'cost':
            focus = "reducing costs while maintaining quality and safety standards"
            target = "Save 10-15% without compromising structural integrity or finish quality"
        elif optimization_type == 'time':
            focus = "reducing construction timeline through better scheduling and resource management"
            target = "Reduce duration by 15-20% through parallel activities and optimized workflows"
        else:
            focus = "balancing cost efficiency with faster completion"
            target = "Achieve 8-12% cost savings and 10-15% time reduction"
        
        prompt = f"""You're optimizing a construction project for: {focus}

TARGET: {target}

PROJECT DATA:
{json.dumps(plan_data, indent=2)}

Provide 6-8 SPECIFIC, ACTIONABLE optimization suggestions:

Format each suggestion as:
**[Category]: [Specific Action]**
- Expected Impact: [Quantified benefit]
- Implementation: [How to do it]
- Considerations: [What to watch out for]

Categories to cover:
• Material Procurement
• Labor Efficiency  
• Construction Methods
• Scheduling Optimization
• Technology/Tools
• Vendor Management

Be specific with percentages, costs, and timeframes. Make it practical and immediately actionable. Keep under 300 words."""

        response = self._generate_response(prompt, system_prompt)
        
        return {
            'optimization_type': optimization_type,
            'suggestions': response,
            'potential_savings': self._estimate_savings(plan_data, optimization_type)
        }
    
    def identify_risks(self, project_data):
        """Identify potential project risks"""
        
        system_prompt = """You are a construction risk management expert.
You identify potential risks, delays, and challenges in construction projects."""
        
        prompt = f"""Identify key risks and challenges for this construction project:

{json.dumps(project_data, indent=2)}

Provide:
1. Top 5 Risk Factors
2. Likelihood and Impact assessment
3. Mitigation strategies

Keep response structured and under 250 words."""

        response = self._generate_response(prompt, system_prompt)
        
        # Calculate risk scores
        risk_scores = self._calculate_risk_scores(project_data)
        
        return {
            'risk_analysis': response,
            'risk_scores': risk_scores,
            'overall_risk_level': self._determine_risk_level(risk_scores)
        }
    
    def _assess_feasibility(self, data):
        """Calculate feasibility score (0-100)"""
        score = 100
        
        # Budget feasibility
        if data['budget'] > 0:
            budget_ratio = data['budget'] / data['estimated_cost']
            if budget_ratio < 0.9:
                score -= 30
            elif budget_ratio < 1.0:
                score -= 15
        
        # Timeline feasibility
        recommended_weeks = data['schedule_duration']
        if data['timeline'] > 0:
            timeline_ratio = (data['timeline'] / 7) / recommended_weeks
            if timeline_ratio < 0.7:
                score -= 25
            elif timeline_ratio < 0.9:
                score -= 10
        
        return max(0, min(100, score))
    
    def _assess_budget(self, data):
        """Assess budget status"""
        if data['budget'] == 0:
            return 'not_specified'
        
        ratio = data['budget'] / data['estimated_cost']
        
        if ratio >= 1.2:
            return 'comfortable'
        elif ratio >= 1.0:
            return 'adequate'
        elif ratio >= 0.9:
            return 'tight'
        else:
            return 'insufficient'
    
    def _assess_timeline(self, data):
        """Assess timeline status"""
        if data['timeline'] == 0:
            return 'not_specified'
        
        recommended_days = data['schedule_duration'] * 7
        ratio = data['timeline'] / recommended_days
        
        if ratio >= 1.2:
            return 'relaxed'
        elif ratio >= 0.9:
            return 'realistic'
        elif ratio >= 0.7:
            return 'aggressive'
        else:
            return 'unrealistic'
    
    def _calculate_risk_scores(self, data):
        """Calculate risk scores for different categories"""
        risks = {
            'budget_risk': 0,
            'timeline_risk': 0,
            'complexity_risk': 0,
            'resource_risk': 0
        }
        
        # Budget risk
        if 'budget' in data and 'estimated_cost' in data:
            if data['budget'] > 0:
                ratio = data['budget'] / data['estimated_cost']
                if ratio < 1.0:
                    risks['budget_risk'] = min(100, int((1 - ratio) * 100))
        
        # Timeline risk
        if 'timeline' in data and 'schedule_duration' in data:
            if data['timeline'] > 0:
                ratio = (data['timeline'] / 7) / data['schedule_duration']
                if ratio < 1.0:
                    risks['timeline_risk'] = min(100, int((1 - ratio) * 150))
        
        # Complexity risk
        complexity_scores = {'simple': 20, 'medium': 40, 'complex': 60, 'luxury': 80}
        risks['complexity_risk'] = complexity_scores.get(data.get('complexity', 'medium'), 40)
        
        # Resource risk (based on area and floors)
        if 'area' in data and 'floors' in data:
            if data['area'] * data['floors'] > 3000:
                risks['resource_risk'] = 60
            elif data['area'] * data['floors'] > 2000:
                risks['resource_risk'] = 40
            else:
                risks['resource_risk'] = 20
        
        return risks
    
    def _determine_risk_level(self, risk_scores):
        """Determine overall risk level"""
        avg_risk = sum(risk_scores.values()) / len(risk_scores)
        
        if avg_risk < 30:
            return 'low'
        elif avg_risk < 50:
            return 'moderate'
        elif avg_risk < 70:
            return 'high'
        else:
            return 'very_high'
    
    def _estimate_savings(self, plan_data, optimization_type):
        """Estimate potential savings from optimization"""
        if optimization_type == 'cost':
            return {
                'percentage': '10-15%',
                'estimated_amount': 'Based on material procurement and labor efficiency'
            }
        elif optimization_type == 'time':
            return {
                'percentage': '15-20%',
                'estimated_reduction': 'Through parallel activities and resource optimization'
            }
        else:
            return {
                'percentage': '8-12%',
                'combined_benefit': 'Balanced optimization approach'
            }
    
    def _fallback_response(self, message):
        """Provide fallback response when AI is unavailable"""
        return f"{message} Using rule-based analysis instead."
