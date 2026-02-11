"""
Modern Mestri - AI-Powered Construction Planning System
Main Flask Application
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

# Import modules
from estimation import ConstructionEstimator
from scheduling import ConstructionScheduler
from resources import ResourcePlanner
from ai_agent import AIAgent
from blueprints import BlueprintGenerator

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

import math

# Initialize modules
estimator = ConstructionEstimator()
scheduler = ConstructionScheduler()
resource_planner = ResourcePlanner()
ai_agent = AIAgent()
blueprint_gen = BlueprintGenerator()

def get_model_image(model_id):
    # Professional architectural renders from Unsplash for 3D Imaginator
    images = {
        'small_villa': 'https://images.unsplash.com/photo-1580587767526-cf3671a05014?auto=format&fit=crop&q=80&w=800',
        'modern_duplex': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=800',
        'custom': 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&q=80&w=800'
    }
    return images.get(model_id, images['custom'])

def get_structural_breakdown(area, floors, complexity):
    # Professional Indian Structural Logic
    # 1 pillar per 120-140 sq ft for residential
    base_spacing = 130 
    
    # Ensure minimum 6 pillars for any small house (grid system)
    min_pillars = 6
    calculated_pillars = math.ceil(area / base_spacing)
    
    # Adjust for floors (multi-story needs more support)
    factor = 1.0 + (floors - 1) * 0.2
    total_pillars = max(min_pillars, math.ceil(calculated_pillars * factor))
    
    return {
        'foundation': 'Isolated Footing' if floors < 3 else 'Raft/Pile Foundation',
        'pillars_count': int(total_pillars),
        'beams_est': f"{int(total_pillars * 1.8)} Linear Beams (PL & Roof)",
        'slab_thickness': "125mm - 150mm R.C.C (M20 Grade)",
        'reinforcement': "FE 500 TMT (Primary 12mm/16mm)"
    }

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_available': ai_agent.check_connection()
    })

@app.route('/api/plan', methods=['POST'])
def generate_plan():
    print(f"🔹 Request Received: {request.json}") # Debug Log
    try:
        data = request.json
        
        # Validate input
        required_fields = ['area', 'floors']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract parameters
        area_sq_yards = float(data['area'])
        area_sq_ft = area_sq_yards * 9  # Conversion
        floors = int(data['floors'])
        budget = float(data.get('budget', 0))
        timeline = int(data.get('timeline', 0))
        complexity = data.get('complexity', 'medium')
        facing = data.get('facing', 'north')
        
        # 1. Estimate
        cost_estimate = estimator.calculate_estimate(area_sq_ft, floors, complexity)
        material_estimate = estimator.calculate_materials(area_sq_ft, floors)
        
        # 2. Schedule
        schedule = scheduler.generate_schedule(area_sq_ft, floors, timeline)
        
        # 3. Resources
        labor_plan = resource_planner.estimate_labor(area_sq_ft, floors, timeline)
        
        # 4. Blueprint
        blueprints = {
            'classic': blueprint_gen.generate_layout(area_sq_ft, floors, 'classic'),
            'modern_open': blueprint_gen.generate_layout(area_sq_ft, floors, 'modern_open'),
            'compact_luxury': blueprint_gen.generate_layout(area_sq_ft, floors, 'compact_luxury')
        }
        
        # 5. AI Analysis (Safe Call)
        print("🔹 Starting AI Analysis...")
        try:
            ai_input = {
                'area': area_sq_ft,
                'area_sq_yards': area_sq_yards,
                'floors': floors,
                'budget': budget,
                'timeline': timeline,
                'complexity': complexity,
                'estimated_cost': cost_estimate['total_cost'],
                'schedule_duration': schedule['total_weeks']
            }
            ai_analysis = ai_agent.analyze_plan(ai_input)
        except Exception as e:
            print(f"⚠️ AI Analysis Failed: {e}")
            ai_analysis = {
                'analysis': "AI analysis unavailable. Proceeding with standard estimation.",
                'feasibility_score': 85,
                'budget_status': 'Unknown',
                'timeline_status': 'Unknown'
            }

        response = {
            'success': True,
            'project_summary': {
                'area': area_sq_yards,
                'area_ft': area_sq_ft,
                'floors': floors,
                'complexity': complexity,
                'facing': facing
            },
            'cost_estimate': cost_estimate,
            'material_estimate': material_estimate,
            'labor_plan': labor_plan,
            'schedule': schedule,
            'blueprints': blueprints,
            'ai_analysis': ai_analysis,
            'visualization': {
                'image_path': get_model_image(data.get('model_id', 'custom')),
                'message': f"Visualization for {floors}-floor {facing}-facing home"
            },
            'structural_analysis': get_structural_breakdown(area_sq_ft, floors, complexity)
        }
        
        print("✅ Plan Generated Successfully")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI agent"""
    try:
        data = request.json
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        response = ai_agent.chat(message, context)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """Get optimization suggestions"""
    try:
        data = request.json
        optimization_type = data.get('type', 'cost')  # cost, time, or both
        current_plan = data.get('plan', {})
        
        suggestions = ai_agent.suggest_optimizations(current_plan, optimization_type)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risks', methods=['POST'])
def analyze_risks():
    """Analyze project risks"""
    try:
        data = request.json
        
        risks = ai_agent.identify_risks(data)
        
        return jsonify({
            'success': True,
            'risks': risks
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🏗️  Modern Mestri - AI Construction Planning System")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
