"""
Blueprint Generation Module
Creates simplified floor plan visualizations
"""

import math

class BlueprintGenerator:
    def __init__(self):
        # Standard room dimensions and ratios
        self.room_types = {
            'bedroom': {'min_area': 120, 'ratio': 1.2},
            'living_room': {'min_area': 200, 'ratio': 1.5},
            'kitchen': {'min_area': 80, 'ratio': 1.3},
            'bathroom': {'min_area': 40, 'ratio': 1.0},
            'dining': {'min_area': 100, 'ratio': 1.4},
            'balcony': {'min_area': 40, 'ratio': 2.0}
        }
    
    def generate_layout(self, area, floors, variation='classic'):
        """Generate simplified floor plan layout with variations"""
        
        # Calculate building dimensions
        building_dims = self._calculate_building_dimensions(area)
        
        # Generate room layout for each floor based on variation
        floor_layouts = []
        for floor_num in range(1, floors + 1):
            if variation == 'modern_open':
                layout = self._generate_modern_open_layout(area, floor_num, floors)
            elif variation == 'compact_luxury':
                layout = self._generate_luxury_layout(area, floor_num, floors)
            else:
                layout = self._generate_floor_layout(area, floor_num, floors)
            floor_layouts.append(layout)
        
        # Generate SVG representation
        svg_data = self._generate_svg(floor_layouts, building_dims)
        
        return {
            'variation_name': variation.replace('_', ' ').title(),
            'building_dimensions': building_dims,
            'floor_layouts': floor_layouts,
            'svg_data': svg_data,
            'total_rooms': sum(len(floor['rooms']) for floor in floor_layouts)
        }
    
    def _generate_modern_open_layout(self, area, floor_num, total_floors):
        """Modern Open Plan - Larger living spaces, integrated kitchen/dining"""
        rooms = []
        if floor_num == 1:
            remaining_area = area * 0.9 # Less wall space
            # Huge Open Area (Integrated Living/Dining/Kitchen)
            open_area = remaining_area * 0.6
            rooms.append(self._create_room('Open Living & Kitchen', open_area, 'living_room'))
            remaining_area -= open_area
            # Master Suite
            rooms.append(self._create_room('Guest Bedroom', remaining_area * 0.6, 'bedroom'))
            rooms.append(self._create_room('Designer Bath', remaining_area * 0.3, 'bathroom'))
        else:
            rooms = self._layout_upper_floor(area)
            
        return {
            'floor_number': floor_num,
            'floor_type': 'Ground Floor' if floor_num == 1 else f'Floor {floor_num}',
            'rooms': rooms,
            'total_area': area
        }

    def _generate_luxury_layout(self, area, floor_num, total_floors):
        """Compact Luxury - All bedrooms with attached baths, premium materials context"""
        rooms = []
        if floor_num == 1:
            remaining_area = area * 0.8
            rooms.append(self._create_room('Grand Foyer & Living', remaining_area * 0.4, 'living_room'))
            rooms.append(self._create_room('Gourmet Kitchen', remaining_area * 0.2, 'kitchen'))
            rooms.append(self._create_room('Suite 1 (W/ Bath)', remaining_area * 0.3, 'bedroom'))
            rooms.append(self._create_room('Powder Room', remaining_area * 0.1, 'bathroom'))
        else:
            # Luxury upper floor: fewer but larger suites
            remaining_area = area * 0.8
            rooms.append(self._create_room('Master Suite', remaining_area * 0.5, 'bedroom'))
            rooms.append(self._create_room('Master Bath', remaining_area * 0.15, 'bathroom'))
            rooms.append(self._create_room('Bedroom 2', remaining_area * 0.25, 'bedroom'))
            rooms.append(self._create_room('Private Balcony', remaining_area * 0.1, 'balcony'))

        return {
            'floor_number': floor_num,
            'floor_type': 'Ground Floor' if floor_num == 1 else f'Floor {floor_num}',
            'rooms': rooms,
            'total_area': area
        }
    
    def _calculate_building_dimensions(self, area):
        """Layout rooms for upper floors"""
        rooms = []
        remaining_area = area * 0.85
        
        # Calculate number of bedrooms based on area
        num_bedrooms = max(2, min(4, int(area / 400)))
        
        bedroom_area = remaining_area * 0.7 / num_bedrooms
        
        for i in range(num_bedrooms):
            room_name = f'Bedroom {i + 1}'
            rooms.append(self._create_room(room_name, bedroom_area, 'bedroom'))
        
        # Bathrooms (1 per 2 bedrooms)
        num_bathrooms = max(1, int(num_bedrooms / 2))
        bathroom_area = 50
        
        for i in range(num_bathrooms):
            room_name = f'Bathroom {i + 1}'
            rooms.append(self._create_room(room_name, bathroom_area, 'bathroom'))
        
        # Balcony
        balcony_area = min(remaining_area * 0.1, 60)
        rooms.append(self._create_room('Balcony', balcony_area, 'balcony'))
        
        return rooms
    
    def _create_room(self, name, area, room_type):
        """Create room object with dimensions"""
        ratio = self.room_types.get(room_type, {}).get('ratio', 1.2)
        
        width = math.sqrt(area / ratio)
        length = area / width
        
        return {
            'name': name,
            'type': room_type,
            'area': round(area, 1),
            'width': round(width, 1),
            'length': round(length, 1)
        }
    
    def _generate_svg(self, floor_layouts, building_dims):
        """Generate SVG representation of floor plan"""
        # This is a simplified representation
        # In a full implementation, this would create detailed SVG paths
        
        svg_width = 800
        svg_height = 600
        scale = min(svg_width / building_dims['length'], svg_height / building_dims['width'])
        
        # Generate basic SVG structure
        svg_elements = []
        
        # Building outline
        svg_elements.append({
            'type': 'rect',
            'x': 50,
            'y': 50,
            'width': building_dims['length'] * scale * 0.8,
            'height': building_dims['width'] * scale * 0.8,
            'fill': 'none',
            'stroke': '#333',
            'stroke-width': 3
        })
        
        # Room representations (simplified grid)
        y_offset = 60
        for floor in floor_layouts:
            x_offset = 60
            for room in floor['rooms']:
                room_width = min(room['length'] * scale * 0.15, 150)
                room_height = min(room['width'] * scale * 0.15, 100)
                
                svg_elements.append({
                    'type': 'rect',
                    'x': x_offset,
                    'y': y_offset,
                    'width': room_width,
                    'height': room_height,
                    'fill': self._get_room_color(room['type']),
                    'stroke': '#666',
                    'stroke-width': 1,
                    'opacity': 0.7
                })
                
                svg_elements.append({
                    'type': 'text',
                    'x': x_offset + room_width / 2,
                    'y': y_offset + room_height / 2,
                    'text': room['name'],
                    'font-size': 10,
                    'text-anchor': 'middle'
                })
                
                x_offset += room_width + 10
                if x_offset > svg_width - 100:
                    x_offset = 60
                    y_offset += 120
        
        return {
            'width': svg_width,
            'height': svg_height,
            'elements': svg_elements
        }
    
    def _get_room_color(self, room_type):
        """Get color for room type"""
        colors = {
            'bedroom': '#E3F2FD',
            'living_room': '#FFF3E0',
            'kitchen': '#F1F8E9',
            'bathroom': '#E0F2F1',
            'dining': '#FFF9C4',
            'balcony': '#E8F5E9'
        }
        return colors.get(room_type, '#F5F5F5')
