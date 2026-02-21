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

GENERATORS = {
    'chevron_flow':  chevron_flow.generate,
    'pyramid':       pyramid.generate,
    'mind_map':      mind_map.generate,
    'matrix_grid':   matrix_grid.generate,
    'price_table':   price_table.generate,
    'decision_tree': decision_tree.generate,
    'flowchart':     flowchart.generate,
    'journey_map':   journey_map.generate,
}

LABELS = {
    'chevron_flow':  'Chevron Flow / Milestone Timeline',
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
