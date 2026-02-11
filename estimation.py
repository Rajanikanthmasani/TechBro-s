"""
Construction Cost and Material Estimation Module
Calculates detailed cost breakdowns and material requirements
"""

class ConstructionEstimator:
    def __init__(self):
        # Base rates (can be configured)
        self.rates = {
            'cement': 400,  # per bag (50kg)
            'sand': 50,     # per cubic foot
            'aggregate': 60, # per cubic foot
            'steel': 60,    # per kg
            'bricks': 8,    # per brick
            'paint': 300,   # per liter
            'tiles': 50,    # per sq ft
            'plumbing': 150, # per sq ft
            'electrical': 100, # per sq ft
            'doors': 8000,  # per door
            'windows': 5000, # per window
            'labor_mason': 800,  # per day
            'labor_helper': 500, # per day
            'labor_carpenter': 900, # per day
            'labor_electrician': 1000, # per day
            'labor_plumber': 1000, # per day
        }
        
        # Complexity multipliers
        self.complexity_factors = {
            'simple': 0.85,
            'medium': 1.0,
            'complex': 1.25,
            'luxury': 1.6
        }
    
    def calculate_materials(self, area, floors, complexity='medium'):
        """Calculate material requirements"""
        total_area = area * floors
        complexity_factor = self.complexity_factors.get(complexity, 1.0)
        
        # Foundation and structure calculations
        foundation_area = area * 1.1  # 10% extra for foundation
        
        # Cement calculation (bags)
        cement_bags = int((total_area * 0.4 + foundation_area * 0.3) * complexity_factor)
        
        # Sand (cubic feet)
        sand_cft = int((total_area * 1.2 + foundation_area * 0.8) * complexity_factor)
        
        # Aggregate (cubic feet)
        aggregate_cft = int((total_area * 0.8 + foundation_area * 0.6) * complexity_factor)
        
        # Steel (kg)
        steel_kg = int((total_area * 8 + foundation_area * 12) * complexity_factor)
        
        # Bricks
        bricks = int(total_area * 50 * complexity_factor)
        
        # Paint (liters) - walls and ceiling
        paint_area = total_area * 3  # approximate wall area
        paint_liters = int((paint_area / 120) * complexity_factor)  # 120 sq ft per liter
        
        # Tiles (sq ft)
        tiles_sqft = int(total_area * 0.7 * complexity_factor)  # 70% of floor area
        
        # Doors and windows
        doors = max(3, floors * 4)
        windows = max(4, floors * 6)
        
        materials = {
            'cement': {
                'quantity': cement_bags,
                'unit': 'bags',
                'rate': self.rates['cement'],
                'cost': cement_bags * self.rates['cement']
            },
            'sand': {
                'quantity': sand_cft,
                'unit': 'cft',
                'rate': self.rates['sand'],
                'cost': sand_cft * self.rates['sand']
            },
            'aggregate': {
                'quantity': aggregate_cft,
                'unit': 'cft',
                'rate': self.rates['aggregate'],
                'cost': aggregate_cft * self.rates['aggregate']
            },
            'steel': {
                'quantity': steel_kg,
                'unit': 'kg',
                'rate': self.rates['steel'],
                'cost': steel_kg * self.rates['steel']
            },
            'bricks': {
                'quantity': bricks,
                'unit': 'nos',
                'rate': self.rates['bricks'],
                'cost': bricks * self.rates['bricks']
            },
            'paint': {
                'quantity': paint_liters,
                'unit': 'liters',
                'rate': self.rates['paint'],
                'cost': paint_liters * self.rates['paint']
            },
            'tiles': {
                'quantity': tiles_sqft,
                'unit': 'sq ft',
                'rate': self.rates['tiles'],
                'cost': tiles_sqft * self.rates['tiles']
            },
            'doors': {
                'quantity': doors,
                'unit': 'nos',
                'rate': self.rates['doors'],
                'cost': doors * self.rates['doors']
            },
            'windows': {
                'quantity': windows,
                'unit': 'nos',
                'rate': self.rates['windows'],
                'cost': windows * self.rates['windows']
            }
        }
        
        total_material_cost = sum(item['cost'] for item in materials.values())
        
        return {
            'materials': materials,
            'total_material_cost': total_material_cost
        }
    
    def calculate_costs(self, area, floors, complexity='medium'):
        """Calculate comprehensive cost breakdown"""
        total_area = area * floors
        complexity_factor = self.complexity_factors.get(complexity, 1.0)
        
        # Get material costs
        material_estimate = self.calculate_materials(area, floors, complexity)
        material_cost = material_estimate['total_material_cost']
        
        # Labor costs (estimated based on area and complexity)
        base_labor_cost = total_area * 350 * complexity_factor
        
        # Breakdown by trade
        mason_cost = base_labor_cost * 0.35
        helper_cost = base_labor_cost * 0.25
        carpenter_cost = base_labor_cost * 0.15
        electrician_cost = base_labor_cost * 0.12
        plumber_cost = base_labor_cost * 0.13
        
        labor_breakdown = {
            'masons': int(mason_cost),
            'helpers': int(helper_cost),
            'carpenters': int(carpenter_cost),
            'electricians': int(electrician_cost),
            'plumbers': int(plumber_cost)
        }
        
        total_labor_cost = sum(labor_breakdown.values())
        
        # Additional costs
        plumbing_cost = int(total_area * self.rates['plumbing'] * complexity_factor)
        electrical_cost = int(total_area * self.rates['electrical'] * complexity_factor)
        
        # Miscellaneous (10% of material + labor)
        misc_cost = int((material_cost + total_labor_cost) * 0.10)
        
        # Contingency (5% of total)
        subtotal = material_cost + total_labor_cost + plumbing_cost + electrical_cost + misc_cost
        contingency = int(subtotal * 0.05)
        
        total_cost = subtotal + contingency
        
        # Cost per sq ft
        cost_per_sqft = int(total_cost / total_area)
        
        return {
            'material_cost': material_cost,
            'labor_cost': total_labor_cost,
            'labor_breakdown': labor_breakdown,
            'plumbing_cost': plumbing_cost,
            'electrical_cost': electrical_cost,
            'miscellaneous_cost': misc_cost,
            'contingency': contingency,
            'total_cost': total_cost,
            'cost_per_sqft': cost_per_sqft,
            'breakdown_percentage': {
                'materials': round((material_cost / total_cost) * 100, 1),
                'labor': round((total_labor_cost / total_cost) * 100, 1),
                'plumbing': round((plumbing_cost / total_cost) * 100, 1),
                'electrical': round((electrical_cost / total_cost) * 100, 1),
                'miscellaneous': round((misc_cost / total_cost) * 100, 1),
                'contingency': round((contingency / total_cost) * 100, 1)
            }
        }
