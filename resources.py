"""
Resource Planning Module
Calculates workforce requirements and resource allocation
"""

class ResourcePlanner:
    def __init__(self):
        # Productivity rates (sq ft per day per worker)
        self.productivity = {
            'excavation': 200,
            'foundation': 150,
            'masonry': 100,
            'plastering': 120,
            'flooring': 150,
            'painting': 200,
            'carpentry': 80,
            'electrical': 180,
            'plumbing': 160
        }
        
        # Standard crew composition
        self.crew_ratios = {
            'mason_to_helper': 1 / 2,  # 1 mason needs 2 helpers
            'carpenter_ratio': 0.15,    # 15% of total workforce
            'electrician_ratio': 0.10,  # 10% of total workforce
            'plumber_ratio': 0.10,      # 10% of total workforce
            'supervisor_ratio': 0.05    # 5% of total workforce
        }
    
    def plan_workforce(self, area, floors, timeline, complexity='medium'):
        """Calculate workforce requirements"""
        total_area = area * floors
        
        # Complexity factors
        complexity_factors = {
            'simple': 0.85,
            'medium': 1.0,
            'complex': 1.15,
            'luxury': 1.35
        }
        complexity_factor = complexity_factors.get(complexity, 1.0)
        
        # Calculate total labor days required
        base_labor_days = (total_area / 100) * 45 * complexity_factor  # 45 days per 100 sq ft
        
        # Adjust for timeline constraints
        if timeline > 0:
            # If timeline is tight, need more workers
            standard_duration = int(base_labor_days / 10)  # assuming 10 workers
            if timeline < standard_duration:
                workforce_multiplier = standard_duration / timeline
            else:
                workforce_multiplier = 1.0
        else:
            workforce_multiplier = 1.0
        
        # Calculate workforce by phase
        phases = self._calculate_phase_workforce(total_area, complexity_factor, workforce_multiplier)
        
        # Calculate overall workforce summary
        peak_masons = max(phase['masons'] for phase in phases.values())
        peak_helpers = max(phase['helpers'] for phase in phases.values())
        peak_carpenters = max(phase['carpenters'] for phase in phases.values())
        peak_electricians = max(phase['electricians'] for phase in phases.values())
        peak_plumbers = max(phase['plumbers'] for phase in phases.values())
        supervisors = max(1, int(peak_masons * self.crew_ratios['supervisor_ratio']))
        
        total_workforce = {
            'masons': peak_masons,
            'helpers': peak_helpers,
            'carpenters': peak_carpenters,
            'electricians': peak_electricians,
            'plumbers': peak_plumbers,
            'supervisors': supervisors,
            'total_peak': peak_masons + peak_helpers + peak_carpenters + peak_electricians + peak_plumbers + supervisors
        }
        
        # Calculate total labor days
        total_labor_days = int(base_labor_days * workforce_multiplier)
        
        return {
            'total_workforce': total_workforce,
            'phase_workforce': phases,
            'total_labor_days': total_labor_days,
            'average_daily_workers': int(total_labor_days / (timeline if timeline > 0 else 180)),
            'productivity_assumptions': self.productivity
        }
    
    def _calculate_phase_workforce(self, area, complexity_factor, multiplier):
        """Calculate workforce for each construction phase"""
        base_workers = int(10 * complexity_factor * multiplier)
        
        phases = {
            'excavation_foundation': {
                'duration_days': int(area / self.productivity['excavation']),
                'masons': max(2, int(base_workers * 0.3)),
                'helpers': max(4, int(base_workers * 0.6)),
                'carpenters': 0,
                'electricians': 0,
                'plumbers': 0
            },
            'structure_masonry': {
                'duration_days': int(area / self.productivity['masonry']),
                'masons': max(4, int(base_workers * 0.4)),
                'helpers': max(8, int(base_workers * 0.8)),
                'carpenters': max(1, int(base_workers * 0.15)),
                'electricians': 0,
                'plumbers': 0
            },
            'roofing': {
                'duration_days': int(area / 200),
                'masons': max(3, int(base_workers * 0.3)),
                'helpers': max(6, int(base_workers * 0.6)),
                'carpenters': max(2, int(base_workers * 0.2)),
                'electricians': 0,
                'plumbers': 0
            },
            'plastering': {
                'duration_days': int(area / self.productivity['plastering']),
                'masons': max(4, int(base_workers * 0.4)),
                'helpers': max(6, int(base_workers * 0.6)),
                'carpenters': 0,
                'electricians': 0,
                'plumbers': 0
            },
            'electrical_plumbing': {
                'duration_days': int(area / self.productivity['electrical']),
                'masons': 0,
                'helpers': max(2, int(base_workers * 0.2)),
                'carpenters': 0,
                'electricians': max(2, int(base_workers * 0.15)),
                'plumbers': max(2, int(base_workers * 0.15))
            },
            'flooring_tiling': {
                'duration_days': int(area / self.productivity['flooring']),
                'masons': max(3, int(base_workers * 0.3)),
                'helpers': max(4, int(base_workers * 0.4)),
                'carpenters': 0,
                'electricians': 0,
                'plumbers': 0
            },
            'carpentry_doors_windows': {
                'duration_days': int(area / self.productivity['carpentry']),
                'masons': 0,
                'helpers': max(2, int(base_workers * 0.2)),
                'carpenters': max(3, int(base_workers * 0.25)),
                'electricians': 0,
                'plumbers': 0
            },
            'painting_finishing': {
                'duration_days': int(area / self.productivity['painting']),
                'masons': 0,
                'helpers': max(3, int(base_workers * 0.3)),
                'carpenters': max(1, int(base_workers * 0.1)),
                'electricians': max(1, int(base_workers * 0.1)),
                'plumbers': 0
            }
        }
        
        return phases
