"""
Test script for Modern Mestri backend modules
Run this to verify all modules are working correctly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from estimation import ConstructionEstimator
from scheduling import ConstructionScheduler
from resources import ResourcePlanner
from blueprints import BlueprintGenerator
from ai_agent import AIAgent

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_estimation():
    print_section("Testing Cost Estimation Module")
    
    estimator = ConstructionEstimator()
    
    # Test project
    area = 2000
    floors = 2
    complexity = 'medium'
    
    print(f"\nProject: {area} sq ft, {floors} floors, {complexity} complexity")
    
    # Calculate costs
    cost_estimate = estimator.calculate_costs(area, floors, complexity)
    
    print(f"\n✓ Total Cost: ₹{cost_estimate['total_cost']:,}")
    print(f"✓ Cost per sq ft: ₹{cost_estimate['cost_per_sqft']:,}")
    print(f"✓ Material Cost: ₹{cost_estimate['material_cost']:,}")
    print(f"✓ Labor Cost: ₹{cost_estimate['labor_cost']:,}")
    
    # Calculate materials
    material_estimate = estimator.calculate_materials(area, floors, complexity)
    
    print(f"\n✓ Total Materials Cost: ₹{material_estimate['total_material_cost']:,}")
    print(f"✓ Cement: {material_estimate['materials']['cement']['quantity']} bags")
    print(f"✓ Steel: {material_estimate['materials']['steel']['quantity']} kg")
    print(f"✓ Bricks: {material_estimate['materials']['bricks']['quantity']:,} nos")
    
    return True

def test_scheduling():
    print_section("Testing Scheduling Module")
    
    scheduler = ConstructionScheduler()
    
    area = 2000
    floors = 2
    timeline = 180
    complexity = 'medium'
    
    print(f"\nProject: {area} sq ft, {floors} floors, {timeline} days target")
    
    schedule = scheduler.generate_schedule(area, floors, timeline, complexity)
    
    print(f"\n✓ Total Duration: {schedule['total_weeks']} weeks ({schedule['total_days']} days)")
    print(f"✓ Number of Phases: {len(schedule['phases'])}")
    print(f"✓ Is Aggressive: {schedule['is_aggressive']}")
    
    print("\nPhases:")
    for phase_name, phase_data in list(schedule['phases'].items())[:3]:
        print(f"  • {phase_data['name']}: {phase_data['duration_days']} days")
    
    return True

def test_resources():
    print_section("Testing Resource Planning Module")
    
    planner = ResourcePlanner()
    
    area = 2000
    floors = 2
    timeline = 180
    complexity = 'medium'
    
    print(f"\nProject: {area} sq ft, {floors} floors")
    
    labor_plan = planner.plan_workforce(area, floors, timeline, complexity)
    
    workforce = labor_plan['total_workforce']
    
    print(f"\n✓ Peak Workforce: {workforce['total_peak']} workers")
    print(f"✓ Masons: {workforce['masons']}")
    print(f"✓ Helpers: {workforce['helpers']}")
    print(f"✓ Carpenters: {workforce['carpenters']}")
    print(f"✓ Total Labor Days: {labor_plan['total_labor_days']:,}")
    
    return True

def test_blueprints():
    print_section("Testing Blueprint Generation Module")
    
    generator = BlueprintGenerator()
    
    area = 2000
    floors = 2
    
    print(f"\nProject: {area} sq ft, {floors} floors")
    
    blueprint = generator.generate_layout(area, floors)
    
    print(f"\n✓ Building Dimensions: {blueprint['building_dimensions']['length']} × {blueprint['building_dimensions']['width']} ft")
    print(f"✓ Total Rooms: {blueprint['total_rooms']}")
    
    print("\nFloor Layouts:")
    for floor in blueprint['floor_layouts']:
        print(f"  • {floor['floor_type']}: {len(floor['rooms'])} rooms")
    
    return True

def test_ai_agent():
    print_section("Testing AI Agent Module")
    
    agent = AIAgent()
    
    print("\nChecking AI connection...")
    is_connected = agent.check_connection()
    
    if is_connected:
        print("✓ AI is connected and ready!")
    else:
        print("⚠ AI is offline - using fallback mode")
        print("  (This is normal if Ollama is not running)")
    
    # Test analysis (will use fallback if AI not available)
    project_data = {
        'area': 2000,
        'floors': 2,
        'budget': 5000000,
        'timeline': 180,
        'complexity': 'medium',
        'estimated_cost': 4500000,
        'schedule_duration': 26
    }
    
    print("\nTesting plan analysis...")
    analysis = agent.analyze_plan(project_data)
    
    print(f"✓ Feasibility Score: {analysis['feasibility_score']}/100")
    print(f"✓ Budget Status: {analysis['budget_status']}")
    print(f"✓ Timeline Status: {analysis['timeline_status']}")
    
    return True

def run_all_tests():
    print("\n" + "="*60)
    print("  Modern Mestri - Backend Module Tests")
    print("="*60)
    
    tests = [
        ("Cost Estimation", test_estimation),
        ("Scheduling", test_scheduling),
        ("Resource Planning", test_resources),
        ("Blueprint Generation", test_blueprints),
        ("AI Agent", test_ai_agent)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ Error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print_section("Test Summary")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready to use.")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run_all_tests()
