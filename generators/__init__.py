"""
ETKM Visual Aide — Generator Registry
"""

from . import chevron_flow
from . import pyramid
from . import mind_map
from . import matrix_grid
from . import price_table
from . import decision_tree
from . import flowchart
from . import journey_map
from . import timeline_dots
from . import cycle_diagram
from . import day_plan

GENERATORS = {
    'chevron_flow':  chevron_flow.generate,
    'timeline_dots': timeline_dots.generate,
    'cycle_diagram': cycle_diagram.generate,
    'day_plan':      day_plan.generate,
    'pyramid':       pyramid.generate,
    'mind_map':      mind_map.generate,
    'matrix_grid':   matrix_grid.generate,
    'price_table':   price_table.generate,
    'decision_tree': decision_tree.generate,
    'flowchart':     flowchart.generate,
    'journey_map':   journey_map.generate,
}

LABELS = {
    'chevron_flow':  'Chevron Flow / Milestones',
    'timeline_dots': 'Timeline — Dot / Line',
    'cycle_diagram': 'Cycle Diagram',
    'day_plan':      'Day Plan (30-60-90)',
    'pyramid':       'Pyramid Diagram',
    'mind_map':      'Mind Map / Radial',
    'matrix_grid':   'Performance Matrix / Grid',
    'price_table':   'Price / Feature Table',
    'decision_tree': 'Decision Tree',
    'flowchart':     'Flow Chart',
    'journey_map':   'Customer Journey Map',
}


def generate_diagram(params):
    diagram_type = params.get('diagram_type', 'chevron_flow')
    generator = GENERATORS.get(diagram_type)
    if not generator:
        raise ValueError(f'Unknown diagram type: {diagram_type}')
    return generator(params)
