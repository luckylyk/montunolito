INDEX_HEIGHT = 25
INDEX_WIDTH = 130
INDEX_SPACING = 15

ROWS_TOP = 25
ROWS_LEFT = 35
ROWS_SPACING = 50
ROWS_PADDING = 10
ROWS_WIDTH = INDEX_WIDTH + (ROWS_PADDING * 2)
ROWS_HEADER_SPACE = 50
ROWS_BOTTOM_SPACE = 0

CONNECTION_HANDLER_SIZE = 10

BEAM_CONNECTION_WIDTH = 5

GRID_SPACING = 33
PATTERN_WIDTH = 120

COLORS = {
    'note': 
        {
            'normal': 'black',
            'highlight': 'yellow',
            'selected': 'red'
        },
    'fingerstates':
        {
            'pressed': '#AADDBB',
            'released': '#ABABAB',
        },
    'bubble':
        {
            'closer':
                {
                    'hover': '#d0a895',
                    'free': "#B3B3B3",
                    'cross': "#4b4b4b"
                },
            'border': '#4b4b4b',
            'title': '#4b4b4b',
            'background': '#c8c8c8'
        },
    'graph':
        {
            'background': '#292929',
            'grid':  '#343434',
            'row':
                {
                    'background': '#4a4a4a',
                    'background_highlight': '#535353',
                    'number': 'white'
                },
            'index':
                {
                    'background': 
                        {
                            'min': '#6e6e6e',
                            'max':'#6eAA6e'
                        },
                    'border':
                        {
                            'highlight':  '#449999',
                            'selected': '#dfdfdf',
                        },
                    'plug_highlight': '#AA4455',
                    'item':
                        {
                            'background': '#7f7f7f',

                            'border':
                                {
                                    'highlight':  '#449999',
                                    'selected': '#dfdfdf',
                                },
                        },
                    'path':
                        {
                            'normal': '#AA4455',
                            'highlight': '#DDDD55',
                        },
                }
        },
}
