from math import ceil
import railroad
from railroad import Diagram, Choice, Sequence, Optional, ZeroOrMore, Skip, NonTerminal, Comment
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

railroad.DIAGRAM_CLASS = ''
railroad.DEFAULT_STYLE = css
railroad.STROKE_ODD_PIXEL_LENGTH = STROKE_WIDTH % 2 == 1
railroad.CHAR_WIDTH = 7.5

padding = Sequence('padding:', Choice(0, 'zero', 'space', 'none'))
hour_repr = Sequence('repr:', Choice(0, '24', '12'))
month_repr = Sequence('repr:', Choice(0, 'numerical', 'long', 'short'))
period_case = Sequence('case:', Choice(0, 'lower', 'upper'))
sign = Sequence('sign:', Choice(0, 'automatic', 'mandatory'))
subsecond_digits = Sequence('digits:', Choice(
    0, '1+', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
weekday_repr = Sequence('repr:', Choice(
    0, 'long', 'short', 'sunday', 'monday'))
weekday_one_indexed = Sequence('one_indexed:', Choice(0, 'false', 'true'))
week_number_repr = Sequence('repr:', Choice(0, 'iso', 'sunday', 'monday'))
year_repr = Sequence('repr:', Choice(0, 'full', 'last_two'))
year_base = Sequence('base:', Choice(0, 'calendar', 'iso_week'))

whitespace = Comment('whitespace')


# region: complete diagram
def generate_sequence(name, *modifiers):
    if len(modifiers) == 1:
        return Sequence(name, Optional(Sequence(copy(whitespace), Choice(0, *modifiers)), skip=SKIP))

    return Sequence(
        name,
        ZeroOrMore(Sequence(
            copy(whitespace),
            Choice(0, *modifiers),
        ), skip=SKIP),
    )


complete = Diagram(
    ZeroOrMore(Choice(
        0,
        NonTerminal('literal'),
        Sequence('[', Choice(
            1,
            '[',
            Sequence(
                Optional(copy(whitespace), skip=SKIP),
                Choice(
                    0,
                    generate_sequence(
                        'month',
                        copy(padding),
                        copy(month_repr),
                    ),
                    generate_sequence(
                        'weekday',
                        copy(weekday_repr),
                        copy(weekday_one_indexed),
                    ),
                    generate_sequence(
                        'week_number',
                        copy(padding),
                        copy(week_number_repr),
                    ),
                    generate_sequence(
                        'year',
                        copy(padding),
                        copy(year_repr),
                        copy(year_base),
                        copy(sign),
                    ),
                    generate_sequence(
                        'hour',
                        copy(padding),
                        copy(hour_repr),
                    ),
                    generate_sequence('period', copy(period_case)),
                    generate_sequence('subsecond', copy(subsecond_digits)),
                    generate_sequence(
                        'offset_hour',
                        copy(padding),
                        copy(sign),
                    ),
                    generate_sequence(
                        Choice(
                            0,
                            'day',
                            'ordinal',
                            'minute',
                            'second',
                            'offset_minute',
                            'offset_second',
                        ),
                        copy(padding),
                    ),
                ),
                Optional(copy(whitespace), skip=SKIP),
                ']',
            )
        ))
    ), skip=SKIP)
)

with open('src/diagrams/complete.svg', 'w') as f:
    complete.format(ceil(STROKE_WIDTH / 2)).writeSvg(f.write)
# endregion complete diagram

# region: abbreviated diagram
abbreviated = Diagram(
    ZeroOrMore(Choice(
        0,
        Comment('literal'),
        Sequence('[', Choice(
            1,
            '[',
            Sequence(
                Optional(copy(whitespace), skip=SKIP),
                Comment('component'),
                Optional(copy(whitespace), skip=SKIP),
                ']'
            )
        ))
    ), skip=SKIP)
)

with open('src/diagrams/abbreviated.svg', 'w') as f:
    abbreviated.format(ceil(STROKE_WIDTH / 2)).writeSvg(f.write)
# endregion abbreviated diagram

# region: individual components


class NamedDiagram:
    def __init__(self, name, diagram):
        self.name = name
        self.diagram = diagram


def generate_diagram(name, *modifiers):
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
month = generate_diagram('month', copy(padding), copy(month_repr))
ordinal = generate_diagram('ordinal', copy(padding))
weekday = generate_diagram('weekday', copy(
    weekday_repr), copy(weekday_one_indexed))
week_number = generate_diagram(
    'week_number', copy(padding), copy(week_number_repr))
year = generate_diagram('year', copy(padding), copy(
    year_repr), copy(year_base), copy(sign))
hour = generate_diagram('hour', copy(padding), copy(hour_repr))
minute = generate_diagram('minute', copy(padding))
period = generate_diagram('period', copy(period_case))
second = generate_diagram('second', copy(padding))
subsecond = generate_diagram('subsecond', copy(subsecond_digits))
offset_hour = generate_diagram('offset_hour', copy(padding), copy(sign))
offset_minute = generate_diagram('offset_minute', copy(padding))
offset_second = generate_diagram('offset_second', copy(padding))

all = [day, month, ordinal, weekday, week_number, year, hour, minute,
       period, second, subsecond, offset_hour, offset_minute, offset_second]

for item in all:
    with open(f'src/diagrams/{item.name}.svg', 'w') as f:
        item.diagram.format(ceil(STROKE_WIDTH / 2)).writeSvg(f.write)
# endregion individual components
