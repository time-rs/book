from math import ceil
import railroad
from railroad import Diagram, Choice, Sequence, Optional, ZeroOrMore, OneOrMore, Skip, Comment
from copy import deepcopy as copy

STROKE_WIDTH = 2
SKIP = False

css = f"""
path {{
    stroke-width:{STROKE_WIDTH};
    stroke:#000;
    fill:transparent;
}}
text {{
    font:13px monospace;
    text-anchor:middle;
}}
text.label{{
    text-anchor:start;
}}
text.comment{{
    font:12px monospace;
    opacity:0.8;
}}
rect{{
    stroke-width:{STROKE_WIDTH};
    stroke:#000;
    fill:transparent;
}}
rect.group-box {{
    stroke:gray;
    stroke-dasharray:10 5;
    fill:none;
}}
"""

class NamedDiagram:
    def __init__(self, name, diagram):
        self.name = name
        self.diagram = diagram

railroad.DIAGRAM_CLASS = ''
railroad.DEFAULT_STYLE = css
railroad.STROKE_ODD_PIXEL_LENGTH = STROKE_WIDTH % 2 == 1
railroad.CHAR_WIDTH = 7.5

padding = Sequence('padding:', Choice(0, 'zero', 'space', 'none'))
case_sensitive = Sequence('case_sensitive:', Choice(0, 'true', 'false'))
hour_repr = Sequence('repr:', Choice(0, '24', '12'))
month_repr = Sequence('repr:', Choice(0, 'numerical', 'long', 'short'))
period_case = Sequence('case:', Choice(0, 'lower', 'upper'))
sign = Sequence('sign:', Choice(0, 'automatic', 'mandatory'))
subsecond_digits = Sequence('digits:', Choice(
    0, '1+', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
weekday_repr = Sequence('repr:', Choice(
    0, 'long', 'short', 'sunday', 'monday'))
weekday_one_indexed = Sequence('one_indexed:', Choice(0, 'true', 'false'))
week_number_repr = Sequence('repr:', Choice(0, 'iso', 'sunday', 'monday'))
year_repr = Sequence('repr:', Choice(0, 'full', 'last_two'))
year_range = Sequence('range:', Choice(0, 'extended', 'standard'))
year_base = Sequence('base:', Choice(0, 'calendar', 'iso_week'))
ignore_count = Sequence('count:', Comment('number > 0'))
unix_timestamp_precision = Sequence('precision:',
    Choice(0, 'second', 'millisecond', 'microsecond', 'nanosecond'))

whitespace = Comment('whitespace')

# region: abbreviated diagram
abbreviated_v1 = NamedDiagram('abbreviated-v1', Diagram(
    ZeroOrMore(Choice(
        0,
        Comment('literal'),
        Sequence(
            '[',
            Optional(copy(whitespace), skip=SKIP),
            Comment('component'),
            Optional(copy(whitespace), skip=SKIP),
            ']',
        ),
        '[[',
    ), skip=SKIP)
))
abbreviated_v2 = NamedDiagram('abbreviated-v2', Diagram(
    ZeroOrMore(Choice(
        0,
        Comment('literal'),
        Sequence(
            '[',
            Optional(copy(whitespace), skip=SKIP),
            Comment('component'),
            Optional(copy(whitespace), skip=SKIP),
            ']',
        ),
        Sequence('\\', Choice(
            0,
            '[',
            ']',
            '\\',
        )),
    ), skip=SKIP)
))

# endregion abbreviated diagram

# region: individual components
def generate_diagram(name, *modifiers):
    if len(modifiers) == 0:
        return NamedDiagram(name, Diagram(Sequence(name)))

    return NamedDiagram(
        name,
        Diagram(Sequence(
            name,
            ZeroOrMore(
                Sequence(
                    copy(whitespace),
                    Choice(0, *modifiers),
                ),
                skip=SKIP,
            )
        ))
    )


day = generate_diagram('day', copy(padding))
month = generate_diagram('month', copy(
    padding), copy(month_repr), copy(case_sensitive))
ordinal = generate_diagram('ordinal', copy(padding))
weekday = generate_diagram('weekday', copy(
    weekday_repr), copy(weekday_one_indexed), copy(case_sensitive))
week_number = generate_diagram(
    'week_number', copy(padding), copy(week_number_repr))
year = generate_diagram('year', copy(padding), copy(
    year_repr), copy(year_range), copy(year_base), copy(sign))
hour = generate_diagram('hour', copy(padding), copy(hour_repr))
minute = generate_diagram('minute', copy(padding))
period = generate_diagram('period', copy(period_case), copy(case_sensitive))
second = generate_diagram('second', copy(padding))
subsecond = generate_diagram('subsecond', copy(subsecond_digits))
offset_hour = generate_diagram('offset_hour', copy(padding), copy(sign))
offset_minute = generate_diagram('offset_minute', copy(padding))
offset_second = generate_diagram('offset_second', copy(padding))
ignore = NamedDiagram('ignore', Diagram(Sequence(
    'ignore',
    copy(whitespace),
    copy(ignore_count),
)))
unix_timestamp = generate_diagram('unix_timestamp', copy(unix_timestamp_precision), copy(sign))
end = generate_diagram('end')

format_description = Comment('format_description')

first = NamedDiagram('first', Diagram(Sequence(
    'first',
    copy(whitespace),
    OneOrMore(
        Sequence(
            '[',
            copy(format_description),
            ']',
            Optional(copy(whitespace)),
        ),
    ),
)))
optional = NamedDiagram('optional', Diagram(Sequence(
    'optional',
    copy(whitespace),
    '[',
    copy(format_description),
    ']',
)))
# endregion individual components

all = [
    abbreviated_v1, abbreviated_v2,
    day, month, ordinal, weekday, week_number, year, hour, minute, period, second, subsecond,
    offset_hour, offset_minute, offset_second, first, optional, ignore, unix_timestamp, end
]

for item in all:
    with open(f'src/diagrams/{item.name}.svg', 'w') as f:
        item.diagram.format(ceil(STROKE_WIDTH / 2)).writeStandalone(f.write)
