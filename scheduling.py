"""
Construction Scheduling Module
Generates realistic timelines and week-by-week schedules
"""

class ConstructionScheduler:
    def __init__(self):
        # Phase duration multipliers (relative to base)
        self.phase_durations = {
            'excavation_foundation': 0.15,
            'structure_masonry': 0.25,
            'roofing': 0.10,
            'plastering': 0.15,
            'electrical_plumbing': 0.12,
            'flooring_tiling': 0.10,
            'carpentry_doors_windows': 0.08,
            'painting_finishing': 0.05
        }
        
        # Dependencies between phases
        self.dependencies = {
            'excavation_foundation': [],
            'structure_masonry': ['excavation_foundation'],
            'roofing': ['structure_masonry'],
            'plastering': ['roofing'],
            'electrical_plumbing': ['plastering'],
            'flooring_tiling': ['electrical_plumbing'],
            'carpentry_doors_windows': ['plastering'],
            'painting_finishing': ['flooring_tiling', 'carpentry_doors_windows']
        }
    
    def generate_schedule(self, area, floors, timeline, complexity='medium'):
        """Generate comprehensive construction schedule"""
        
        # Calculate base duration
        base_duration = self._calculate_base_duration(area, floors, complexity)
        
        # Adjust for user timeline if provided
        if timeline > 0:
            target_duration = timeline
            compression_factor = base_duration / timeline if timeline < base_duration else 1.0
        else:
            target_duration = base_duration
            compression_factor = 1.0
        
        # Generate phase schedule
        phases = self._generate_phase_schedule(target_duration, compression_factor)
        
        # Generate week-by-week schedule
        weekly_schedule = self._generate_weekly_schedule(phases, target_duration)
        
        # Calculate milestones
        milestones = self._calculate_milestones(phases)
        
        # Identify critical path
        critical_path = self._identify_critical_path(phases)
        
        return {
            'total_weeks': int(target_duration / 7),
            'total_days': target_duration,
            'base_duration': base_duration,
            'compression_factor': round(compression_factor, 2),
            'phases': phases,
            'weekly_schedule': weekly_schedule,
            'milestones': milestones,
            'critical_path': critical_path,
            'is_aggressive': compression_factor > 1.2
        }
    
    def _calculate_base_duration(self, area, floors, complexity):
        """Calculate realistic base duration in days"""
        # Base formula: 0.5 days per sq ft for medium complexity
        complexity_factors = {
            'simple': 0.4,
            'medium': 0.5,
            'complex': 0.65,
            'luxury': 0.85
        }
        
        factor = complexity_factors.get(complexity, 0.5)
        base_days = int(area * floors * factor)
        
        # Floor multiplier (higher floors take more time)
        floor_multiplier = 1 + (floors - 1) * 0.15
        
        total_days = int(base_days * floor_multiplier)
        
        # Minimum duration constraints
        min_duration = 90  # At least 3 months
        
        return max(total_days, min_duration)
    
    def _generate_phase_schedule(self, total_duration, compression_factor):
        """Generate schedule for each phase"""
        phases = {}
        current_day = 0
        
        for phase_name, duration_ratio in self.phase_durations.items():
            # Calculate phase duration
            phase_duration = int(total_duration * duration_ratio)
            
            # Adjust for compression
            if compression_factor > 1:
                phase_duration = max(int(phase_duration / compression_factor), 5)
            
            # Calculate start and end dates
            start_day = current_day
            end_day = current_day + phase_duration
            
            phases[phase_name] = {
                'name': self._format_phase_name(phase_name),
                'start_day': start_day,
                'end_day': end_day,
                'duration_days': phase_duration,
                'start_week': int(start_day / 7) + 1,
                'end_week': int(end_day / 7) + 1,
                'dependencies': self.dependencies[phase_name],
                'status': 'planned'
            }
            
            current_day = end_day
        
        return phases
    
    def _generate_weekly_schedule(self, phases, total_duration):
        """Generate week-by-week breakdown"""
        total_weeks = int(total_duration / 7) + 1
        weekly_schedule = []
        
        for week in range(1, total_weeks + 1):
            week_start = (week - 1) * 7
            week_end = week * 7
            
            # Find active phases in this week
            active_phases = []
            for phase_name, phase_data in phases.items():
                if phase_data['start_day'] < week_end and phase_data['end_day'] > week_start:
                    active_phases.append({
                        'name': phase_data['name'],
                        'progress': self._calculate_phase_progress(
                            phase_data, week_start, week_end
                        )
                    })
            
            weekly_schedule.append({
                'week': week,
                'start_day': week_start,
                'end_day': min(week_end, total_duration),
                'active_phases': active_phases,
                'phase_count': len(active_phases)
            })
        
        return weekly_schedule
    
    def _calculate_phase_progress(self, phase_data, week_start, week_end):
        """Calculate progress percentage for a phase in a given week"""
        phase_start = phase_data['start_day']
        phase_end = phase_data['end_day']
        phase_duration = phase_data['duration_days']
        
        # Calculate overlap
        overlap_start = max(phase_start, week_start)
        overlap_end = min(phase_end, week_end)
        overlap_days = max(0, overlap_end - overlap_start)
        
        # Calculate progress in this week
        progress = (overlap_days / phase_duration) * 100 if phase_duration > 0 else 0
        
        return round(progress, 1)
    
    def _calculate_milestones(self, phases):
        """Identify key project milestones"""
        milestones = [
            {
                'name': 'Foundation Complete',
                'day': phases['excavation_foundation']['end_day'],
                'week': phases['excavation_foundation']['end_week']
            },
            {
                'name': 'Structure Complete',
                'day': phases['structure_masonry']['end_day'],
                'week': phases['structure_masonry']['end_week']
            },
            {
                'name': 'Roofing Complete',
                'day': phases['roofing']['end_day'],
                'week': phases['roofing']['end_week']
            },
            {
                'name': 'MEP Work Complete',
                'day': phases['electrical_plumbing']['end_day'],
                'week': phases['electrical_plumbing']['end_week']
            },
            {
                'name': 'Project Completion',
                'day': phases['painting_finishing']['end_day'],
                'week': phases['painting_finishing']['end_week']
            }
        ]
        
        return milestones
    
    def _identify_critical_path(self, phases):
        """Identify critical path phases"""
        # For construction, typically sequential phases form critical path
        critical_phases = [
            'excavation_foundation',
            'structure_masonry',
            'roofing',
            'plastering',
            'electrical_plumbing',
            'painting_finishing'
        ]
        
        return [phases[phase]['name'] for phase in critical_phases if phase in phases]
    
    def _format_phase_name(self, phase_name):
        """Convert phase key to readable name"""
        return phase_name.replace('_', ' ').title()
