import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import numpy as np

# import functions from .py files
import app_graphing as app_gr
import app_wrangling as app_wr

# load board game data
boardgame_data = app_wr.call_boardgame_data()

# dictionary for tab 1 slider
max_year = boardgame_data["year_published"].max().year
slider_dict = {x: str(x) for x in range(1950, (max_year + 1), 5)}

# dictionary for dropdowns
col_key_list = ["category", "mechanic", "publisher"]
col_value_list = [app_wr.subset_data(boardgame_data, v) for v in col_key_list]
col_dict = dict(zip(col_key_list, col_value_list))

# radio dict
radio_options = [
    {"label": " Categories", "value": "category"},
    {"label": " Mechanics", "value": "mechanic"},
    {"label": " Publishers", "value": "publisher"},
]

# extents for 3D plot
extents_3d = {
    "min_x": boardgame_data["x"].min(),
    "max_x": boardgame_data["x"].max(),
    "min_y": boardgame_data["y"].min(),
    "max_y": boardgame_data["y"].max(),
    "min_z": boardgame_data["z"].min(),
    "max_z": boardgame_data["z"].max(),
}


# title for all tabs
def title():
    """
    :return: A Div containing dashboard title.
    """
    return html.Div(
        children=[html.H1("Board Game Data Explorer", style={"font-weight": "normal"})]
    )


# description card tab 1
def description_card_tab1():
    """
    :return: A Div containing welcome message and descriptions on tab 1.
    """
    return html.Div(
        id="description-card-tab1",
        children=[
            html.H5("Welcome to the Board Game Data Explorer"),
            dcc.Markdown(
                id="intro1",
                children="Use the tab selectors above to view either \
                    **Game Trends**, **Top Games**, or the **3D Game Explorer**. \
                    Descriptions are available on each tab using the **button** \
                    to the right. A **dataset** description is also available.",
            ),
        ],
    )


# Data set description for tab 1
def data_set_desc_tab1():
    """
    :return: A Div containing description of the data set,
    which pops out in the tab 1 modal.
    """
    return html.Div(
        children=[
            html.H4("Description of Dataset"),
            dcc.Markdown(
                "This dataset comes from the [BoardGameGeek](https://boardgamegeek.com/) \
                    website and includes board games with descriptions, general game \
                    details, publisher, and user ratings.",
            ),
            dcc.Markdown(
                "Note that he dataset is filtered to remove any games with less than \
                    50 user ratings and is limited to games published after 1950."
            ),
        ]
    )


# tab 1 description for modal button


def tab_1_description():
    """
    :return: A Div containing description of tab 1
    that goes in the pop out modal on tab 1.
    """
    return html.Div(
        children=[
            html.H4("Game Trends"),
            dcc.Markdown(
                "Select Categories, Mechanics, or Publishers and filter on the \
                    minimum number of user ratings for a board game."
            ),
            html.H5("Timeseries Subtab"),
            dcc.Markdown(
                "**Average Game Ratings** provides a plot of each game's \
                    average user rating vs published year. Note that \
                    the blue trendline represents the annual average of all \
                    published games regardless of user selection."
            ),
            dcc.Markdown(
                "**Game Counts** provides the total count of games published in each year \
                    based on the user selections."
            ),
            html.H5("Density Subtab"),
            dcc.Markdown(
                "View user rating density plots based on user selections. Also allows \
                    subsetting the data based on a year range using a slider"
            ),
            dcc.Markdown(
                "If no elements are selected from the dropdown menu, the top 5 Categories, \
                    Mechanics or Publishers based on the mean average user rating will \
                    be displayed."
            ),
        ]
    )


# tab 2 description for modal button
def tab_2_description():
    """
    :return: A Div containing description of tab 2
    that goes in the pop out modal on tab 2.
    """
    return html.Div(
        children=[
            html.H4("Top Games"),
            dcc.Markdown(
                "This tab allows users to select any combination of game categories, \
                mechanics and publishers as well as the minimum number of user ratings \
                for a game. The top 10 games containing all selections and ranked by \
                user rating will be displayed."
            ),
            dcc.Markdown(
                "Below the barchart is also a button which will show a table of \
                information for the 10 games."
            ),
        ]
    )


# tab 3 description for modal button
def tab_3_description():
    """
    :return: A Div containing description of tab 3
    that goes in the pop out modal on tab 3.
    """
    return html.Div(
        children=[
            html.H4("3D Game Explorer"),
            dcc.Markdown(
                "The 3D Game Explorer shows a visual representation of game \
                similarity based on game categories, mechanics, and user ratings."
            ),
            dcc.Markdown(
                "The graph was generated using a \
                [t-SNE](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding)\
                analysis. Game similarity between mechanics and categories is shown on \
                the horizontal (x and y axes) and game similarity in user ratings \
                (both counts and average rating) is represented on the vertical \
                (z-axis)."
            ),
            dcc.Markdown(
                "Clicking on any game will provide game details at the bottom of the left\
                column."
            ),
        ]
    )


# control card for tab 1
def generate_control_card_tab1():
    """
    :return: A Div containing controls for graphs on tab 1,
    which go on the control card on the left.
    """
    return html.Div(
        id="control-card-tab1",
        children=[
            html.H6("Select:"),
            dcc.RadioItems(
                id="radio-selection-tab1",
                options=radio_options,
                value="mechanic",
                labelStyle={"display": "block"},
                persistence=False,
            ),
            html.Br(),
            html.H6("Select elements to view:"),
            dcc.Dropdown(id="radio-dependent-tab1", options=[], multi=True, value=[]),
            html.Br(),
            html.H6("Select minumum number of ratings:"),
            dcc.Slider(
                id="min-num-ratings",
                min=0,
                max=10000,
                step=100,
                value=5000,
                marks={0: "0", 5000: "5000", 10000: "10000"},
            ),
            html.Br(),
            html.Div(id="slider-output-container_2"),
        ],
    )


# control card for tab 2
def generate_control_card_tab2():
    """
    :return: A Div containing controls for graphs on tab 2,
    which go on the control card on the left.
    """
    return html.Div(
        id="control-card-tab2",
        children=[
            html.H6("Select categories:"),
            dcc.Dropdown(
                id="category-widget-tab2",
                value="",
                options=[
                    {"label": name, "value": name} for name in col_dict["category"]
                ],
                multi=True,
            ),
            html.Br(),
            html.H6("Select mechanics:"),
            dcc.Dropdown(
                id="mechanics-widget-tab2",
                value="",
                options=[
                    {"label": name, "value": name} for name in col_dict["mechanic"]
                ],
                multi=True,
            ),
            html.Br(),
            html.H6("Select publishers:"),
            dcc.Dropdown(
                id="publisher-widget-tab2",
                value="",
                options=[
                    {"label": name, "value": name} for name in col_dict["publisher"]
                ],
                multi=True,
            ),
            html.Br(),
            html.H6("Select minumum number of ratings:"),
            dcc.Slider(
                id="min-num-ratings2",
                min=0,
                max=10000,
                step=100,
                value=5000,
                marks={0: "0", 5000: "5000", 10000: "10000"},
            ),
            html.Br(),
            html.Div(id="slider-output-container_3"),
        ],
    )


# control card for tab 3
def generate_control_card_tab3():
    """
    :return: A Div containing controls for graphs on tab 3,
    which go on the control card on the left.
    """
    return html.Div(
        id="control-card-tab3",
        children=[
            html.H6("Select:"),
            dcc.RadioItems(
                id="radio-selection-tab3",
                options=radio_options,
                value="category",
                labelStyle={"display": "block"},
            ),
            html.Br(),
            html.H6("Select elements to view:"),
            dcc.Dropdown(
                id="radio-dependent-tab3",
                options=[],
                multi=True,
                value=["Negotiation", "Farming"],
            ),
            html.Br(),
            html.H6("Select game to highlight:"),
            dcc.Dropdown(
                id="games-dependent-tab3", options=[], multi=False, value=None
            ),
        ],
    )


# sub-title card tab 1
sub_title_card_1 = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(description_card_tab1(), width=8),
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Dataset Description",
                                                id="open",
                                                style={"margin-left": "15px"},
                                            ),
                                            dbc.Modal(
                                                [
                                                    dbc.ModalBody(data_set_desc_tab1()),
                                                    dbc.ModalFooter(
                                                        dbc.Button(
                                                            "Close",
                                                            id="close",
                                                            className="ml-auto",
                                                        )
                                                    ),
                                                ],
                                                id="modal",
                                            ),
                                            html.Br(),
                                            html.Br(),
                                            html.Div(
                                                [
                                                    dbc.Button(
                                                        "Game Trends Tab Description ",
                                                        id="open2",
                                                        style={"margin-left": "15px"},
                                                    ),
                                                    dbc.Modal(
                                                        [
                                                            dbc.ModalBody(
                                                                tab_1_description()
                                                            ),
                                                            dbc.ModalFooter(
                                                                dbc.Button(
                                                                    "Close",
                                                                    id="close2",
                                                                    className="ml-auto",
                                                                )
                                                            ),
                                                        ],
                                                        id="modal2",
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        ]
    ),
    color="#F3F2F2",
)

# subtitle card tab 2
sub_title_card_2 = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Top Board Games"),
                        html.P(
                            "Use the interactive features below to view the top \
                            10 games based on choice of game categories, mechanics \
                            and publishers. "
                        ),
                    ],
                    width=9,
                ),
                dbc.Col(
                    [
                        dbc.Button("Top Games Tab Description", id="open3"),
                        dbc.Modal(
                            [
                                dbc.ModalBody(tab_2_description()),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Close", id="close3", className="ml-auto"
                                    )
                                ),
                            ],
                            id="modal3",
                        ),
                    ],
                    width=3,
                ),
            ]
        )
    ),
    color="#F3F2F2",
)


# subtitle card tab 3
sub_title_card_3 = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Board Game Explorer"),
                        dcc.Markdown(
                            "Select either categories, mechanics or publishers.\
                            Then select different elements to view on the\
                            following figure. **Click** any game on the plot to\
                            view details in the left column. **Larger** points \
                            indicate games with higher user ratings scores."
                        ),
                    ],
                    width=9,
                ),
                dbc.Col(
                    [
                        dbc.Button("3D Game Explorer Description", id="open4"),
                        dbc.Modal(
                            [
                                dbc.ModalBody(tab_3_description()),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Close", id="close4", className="ml-auto"
                                    )
                                ),
                            ],
                            id="modal4",
                        ),
                    ],
                    width=3,
                ),
            ]
        )
    ),
    color="#F3F2F2",
)


# card 1 containing the pop over "how to use tab 1" instructions and
# control card for tab 1
first_card_tab1 = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                id="control-card-tab-1",
                children=[
                    html.Div(
                        [
                            dbc.Button("How to use", id="popover-target", color="info"),
                            dbc.Popover(
                                [
                                    dbc.PopoverHeader(
                                        "How To Use The Game Trends Tab?"
                                    ),
                                    dbc.PopoverBody(
                                        "Select either categories, mechanics or \
                                        publishers below, then select elements \
                                        from the drop-down to visualize on this \
                                        tab. Use the slider to select the minimum \
                                        number ratings for the games shown in the \
                                        visualization. In the density plot tab,\
                                        choose a time period by dragging the \
                                        interactive slider. "
                                    ),
                                ],
                                id="popover",
                                is_open=False,
                                target="popover-target",
                            ),
                        ]
                    ),
                    html.Br(),
                    generate_control_card_tab1(),
                ],
            )
        ]
    ),
    color="#F3F2F2",
)


# card 2 for tab 1 containing the two plots on upper portion of tab 1,
# the scatter plot and the counts stacked histogram
second_card_tab1 = dbc.Card(
    dbc.CardBody(
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Timeseries Plots",
                    children=(
                        [
                            html.Div(
                                [
                                    dbc.Col(
                                        [
                                            html.Br(),
                                            html.H5("Average Game Ratings"),
                                            html.H6(
                                                "Blue line shows annual average of \
                                                    ALL games in dataset"
                                            ),
                                            html.Iframe(
                                                # scatter plot
                                                id="scatter",
                                                style={
                                                    "border-width": "0",
                                                    "width": "100%",
                                                    "height": "250px",
                                                },
                                            ),
                                            html.Br(),
                                            html.H5("Published Game Counts"),
                                            html.Iframe(
                                                # stacked histogram
                                                id="count",
                                                style={
                                                    "border-width": "0",
                                                    "width": "100%",
                                                    "height": "250px",
                                                },
                                            ),
                                        ],
                                        width={"size": 10, "offset": 1},
                                    ),
                                    html.Br(),
                                ]
                            )
                        ]
                    ),
                ),
                dbc.Tab(
                    label="Density Plot",
                    children=(
                        html.Div(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.Br(),
                                                    html.H5("Game Density Plots"),
                                                    html.Br(),
                                                    html.Div(
                                                        id="top-range-slider-output",
                                                    ),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Div(
                                                        dcc.RangeSlider(
                                                            id="top-range-slider",
                                                            min=1950,
                                                            max=2016,
                                                            step=1,
                                                            value=[1990, 2010],
                                                            marks=slider_dict,
                                                        ),
                                                        style={
                                                            "width": "60%",
                                                            "display": "inline-block",
                                                            "align-items": "center",
                                                            "justify-content": "center",
                                                        },
                                                    ),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Iframe(
                                                        id="density_plot",
                                                        style={
                                                            "border-width": "0",
                                                            "width": "1050px",
                                                            "height": "550px",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "display": "inline-block",
                                                    "align-items": "center",
                                                    "justify-content": "center",
                                                },
                                            )
                                        ],
                                        width={"size": 6, "offset": 1},
                                    )
                                )
                            ]
                        )
                    ),
                ),
            ]
        )
    ),
    color="#F3F2F2",
)


# card 1 for tab 2 containing the pop over "how to use tab 2" instructions and
# control card for tab 2
first_card_tab2 = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                id="control-card-tab-2",
                children=[
                    html.Div(
                        [
                            dbc.Button(
                                "How to use", id="popover-target2", color="info"
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverHeader("How To Use The Top Games Tab?"),
                                    dbc.PopoverBody(
                                        "Select any combination of game categories, mechanics \
                                    and publishers in the dropdowns below to populate \
                                    the Top Games bar chart. User the slider to filter \
                                    based on mininum number of user ratings for a game."
                                    ),
                                ],
                                id="popover2",
                                is_open=False,
                                target="popover-target2",
                            ),
                        ]
                    ),
                    html.Br(),
                    generate_control_card_tab2(),
                ],
            ),
        ]
    ),
    color="#F3F2F2",
    style={"height": "30em"},
)


# Tab 2 card containing the top 10 games bar chart for tab 2
top_n_games_card_tab2 = dbc.Card(
    dbc.CardBody(
        [
            html.Br(),
            dbc.Col(
                [
                    html.H5("Top 10 Games"),
                    html.Div(
                        html.Iframe(
                            id="top-n-games",
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "1000px",
                            },
                        ),
                    ),
                ],
                width={"size": 12, "offset": 1},
            ),
        ]
    ),
    color="#F3F2F2",
    style={"height": "30rem"},
)

# table card
top_n_games_table_card_tab2 = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    dbc.Button(
                        "View Game Details",
                        id="collapse-button",
                        className="mb-3",
                        color="primary",
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Top 10 Games Facts Table:"),
                                    dash_table.DataTable(
                                        id="top-n-games-datatable",
                                        style_cell={
                                            "whiteSpace": "normal",
                                            "height": "auto",
                                            "font-family": "Verdana",
                                            "font-size": 10,
                                        },
                                        style_table={"overflowY": "scroll"},
                                        sort_action="native",
                                        style_data_conditional=[
                                            {
                                                "if": {"row_index": "odd"},
                                                "backgroundColor": "rgb(248, 248, 248)",
                                            }
                                        ],
                                        style_header={
                                            "backgroundColor": "rgb(230, 230, 230)",
                                            "fontWeight": "bold",
                                        },
                                    ),
                                ],
                                style={"height": "40rem", "width": "90rem"},
                            ),
                            color="#F3F2F2",
                        ),
                        id="collapse",
                    ),
                ],
            )
        ]
    ),
    color="#F3F2F2",
)

# card 1 for tab 3 containing the pop over "how to use tab 2" instructions and
# control card for tab 3
control_card_tab3 = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    dbc.Button("How to use", id="popover-target3", color="info"),
                    dbc.Popover(
                        [
                            dbc.PopoverHeader("How To Use The 3D Game Explorer Tab?"),
                            dbc.PopoverBody(
                                "Select game categories, mechanics and publishers or populate \
                                the 3D plot. Click and drag to  move around the \
                                3D plot, and use the mouse to zoom. Simply hover \
                                over and click a game to view game facts."
                            ),
                        ],
                        id="popover3",
                        is_open=False,
                        target="popover-target3",
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                id="left-column-tab3",
                className="four columns",  # not sure this is needed
                children=[generate_control_card_tab3()],
            ),
            html.Br(),
            html.H5("Selected Game Facts:"),
            html.H6("Name and Rating:"),
            html.Div(id="tsne-data-out-name"),
            html.Div(id="tsne-data-out-score"),
            html.Div(id="tsne-data-out-ratings"),
            html.Br(),
            html.H6("Categories:"),
            html.Div(id="tsne-data-out-categories"),
            html.Br(),
            html.H6("Mechanics:"),
            html.Div(id="tsne-data-out-mechanics"),
            html.Br(),
            html.H6("Publishers:"),
            html.Div(id="tsne-data-out-publishers"),
        ]
    ),
    color="#F3F2F2",
)


# card the tsne plot on tab 3
tab_3_plot = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Br(),
                    html.H5("3D Game Explorer"),
                    dcc.Graph(id="tsne-3d-plot", style={"height": "80vh"}),
                ]
            ),
        ]
    ),
    color="#F3F2F2",
)

# tab styling features for layout
tabs_styles = {"height": "44px" ""}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#119DFF",
    "color": "white",
    "padding": "6px",
}

#  set up app stylesheet and server
app = dash.Dash(
    __name__,
    title="Board Game Data Explorer",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server

# app layout
app.layout = html.Div(
    dbc.Container(
        html.Div(
            [  # dashboard title
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    id="title-top",
                                    children=[title()],
                                    style={"backgroundColor": "#DDDCDC"},
                                )
                            ]
                        )
                    ]
                ),
                dcc.Tabs(
                    [
                        dcc.Tab(
                            label="Game Trends",
                            children=[
                                html.Div(
                                    [
                                        dbc.Row([((dbc.Col(sub_title_card_1)))]),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                dbc.Col(first_card_tab1, width=3),
                                                dbc.Col(second_card_tab1, width=9),
                                            ]
                                        ),
                                    ]
                                )
                            ],
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Top Games",
                            children=[
                                html.Div(
                                    [
                                        dbc.Row([((dbc.Col(sub_title_card_2)))]),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                dbc.Col(first_card_tab2, width=3),
                                                dbc.Col(
                                                    [
                                                        top_n_games_card_tab2,
                                                    ],
                                                    width=9,
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Row(
                                            dbc.Col(top_n_games_table_card_tab2),
                                        ),
                                    ],
                                    style={"height": 1250},
                                )
                            ],
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="3D Game Explorer",
                            children=[
                                html.Div(
                                    [
                                        dbc.Row(dbc.Col(sub_title_card_3)),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                dbc.Col(control_card_tab3, width=3),
                                                dbc.Col(tab_3_plot, width=9),
                                            ]
                                        ),
                                    ]
                                )
                            ],
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                    ]
                ),
            ],
            style={"backgroundColor": "#DDDCDC"},
        ),
        fluid=True,
    ),
    style={"backgroundColor": "#DDDCDC"},
)


# Set up callbacks/backend
# modal data set description
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal_description(n1, n2, is_open):
    """
    :return: Open modal callback if user clicks data set description button on tab 1.
    """
    if n1 or n2:
        return not is_open
    return is_open


# modal tab 1 description
@app.callback(
    Output("modal2", "is_open"),
    [Input("open2", "n_clicks"), Input("close2", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal_tab1(n1, n2, is_open):
    """
    :return: Open modal callback if user clicks tab 1 description button on tab 1.
    """
    if n1 or n2:
        return not is_open
    return is_open


# Button over select for how to use tab 1 on control card
@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover_tab1(n, is_open):
    """
    :return: Open pop-over callback for how to use button for tab 1.
    """
    if n:
        return not is_open
    return is_open


# radio button selection options to populate drop downs for tab1
@app.callback(
    dash.dependencies.Output("radio-dependent-tab1", "options"),
    dash.dependencies.Output("radio-dependent-tab1", "value"),
    [dash.dependencies.Input("radio-selection-tab1", "value")],
)
def update_options_tab1(chosen_selection):
    """
    :return: Callback to generate drop down based on radio button selection.
    """
    col = chosen_selection
    return [{"label": c, "value": c} for c in col_dict[col]], []


# scatter plot tab 1
@app.callback(
    Output("scatter", "srcDoc"),
    Input("radio-selection-tab1", "value"),
    Input("radio-dependent-tab1", "value"),
    Input("min-num-ratings", "value"),
)
def call_scatter_tab1(col, list_, n_ratings):
    """
    :return: Scatter plot of game ratings on tab 1.
    """
    chart = app_gr.scatter_plot_dates(boardgame_data, col, list_, n_ratings)
    return chart.to_html()


# stacked histogram of counts annual published counts
@app.callback(
    Output("count", "srcDoc"),
    Input("radio-selection-tab1", "value"),
    Input("radio-dependent-tab1", "value"),
    Input("min-num-ratings", "value"),
)
def call_counts_tab1(col, list_, n_ratings):
    """
    :return: Bar chart of published game counts on tab 1.
    """
    chart2 = app_gr.count_plot_dates(boardgame_data, col, list_, n_ratings)
    return chart2.to_html()


# year range slider output tab 1
@app.callback(
    dash.dependencies.Output("top-range-slider-output", "children"),
    dash.dependencies.Input("top-range-slider", "value"),
)
def range_slider_select_tab1(value):
    """
    :return: Tab 1 year range slider output years for density plot on tab 1.
    """
    transformed_value = [v for v in value]
    return "Years Selected: {} to {}".format(transformed_value[0], transformed_value[1])


# density plot tab 1
@app.callback(
    Output("density_plot", "srcDoc"),
    Input("radio-selection-tab1", "value"),
    Input("radio-dependent-tab1", "value"),
    Input("top-range-slider", "value"),
    Input("min-num-ratings", "value"),
)
def call_density_tab1(col, list_, value1, value2):
    """
    :return: Game rating density plot on tab 1.
    """
    transformed_value = [v for v in value1]
    val1 = transformed_value[0]
    val2 = transformed_value[1]
    density_chart = app_gr.rank_plot_density(
        boardgame_data,
        col,
        list_,
        year_in=int(val1),
        year_out=int(val2),
        n_ratings=value2,
    )
    return density_chart.to_html()


# modal for description tab 2
@app.callback(
    Output("modal3", "is_open"),
    [Input("open3", "n_clicks"), Input("close3", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal_tab(n1, n2, is_open):
    """
    :return: Open modal callback if user clicks tab 2 description button on tab 2.
    """
    if n1 or n2:
        return not is_open
    return is_open


# modal for description tab 3
@app.callback(
    Output("modal4", "is_open"),
    [Input("open4", "n_clicks"), Input("close4", "n_clicks")],
    [State("modal4", "is_open")],
)
def toggle_modal_tab3(n1, n2, is_open):
    """
    :return: Open modal callback if user clicks tab 3 description button on tab 3.
    """
    if n1 or n2:
        return not is_open
    return is_open


# Button over select for how to use tab 2 on control card
@app.callback(
    Output("popover2", "is_open"),
    [Input("popover-target2", "n_clicks")],
    [State("popover2", "is_open")],
)
def toggle_popover_tab2(n, is_open):
    """
    :return: Open pop-over callback for how to use button for tab 2.
    """
    if n:
        return not is_open
    return is_open


# Button over select for how to use tab 3 on control card
@app.callback(
    Output("popover3", "is_open"),
    [Input("popover-target3", "n_clicks")],
    [State("popover3", "is_open")],
)
def toggle_popover_tab3(n, is_open):
    """
    :return: Open pop-over callback for how to use button for tab 2.
    """
    if n:
        return not is_open
    return is_open


# top n games bar chart tab 2
@app.callback(
    Output("top-n-games", "srcDoc"),
    Input("category-widget-tab2", "value"),
    Input("mechanics-widget-tab2", "value"),
    Input("publisher-widget-tab2", "value"),
    Input("min-num-ratings2", "value"),
)
def call_top_n_games_tab2(c, m, p, value2):
    """
    :return: Top 10 games plot on tab 2.
    """
    top_n_games = app_gr.top_n_plot(
        data=boardgame_data,
        cat=c,
        mech=m,
        pub=p,
        n=10,
        n_ratings=value2,
    )
    return top_n_games.to_html()


# data table top n games bar chart tab 2
@app.callback(
    Output("top-n-games-datatable", "data"),
    Output(component_id="top-n-games-datatable", component_property="columns"),
    Input("category-widget-tab2", "value"),
    Input("mechanics-widget-tab2", "value"),
    Input("publisher-widget-tab2", "value"),
    Input("min-num-ratings2", "value"),
)
def update_table_tab2(c, m, p, value2):
    """
    :return: Data frame columns and ouput to
    populate data table(dcc.DataTable) on tab 2.
    """
    list_cols = [
        "name",
        "min_players",
        "max_players",
        "min_playtime",
        "max_playtime",
        "year_published",
        "category",
        "mechanic",
        "publisher",
        "average_rating",
        "users_rated",
    ]
    table = app_wr.call_boardgame_filter(
        data=boardgame_data, cat=c, mech=m, pub=p, n=10, n_ratings=value2
    )
    columns = [{"name": col, "id": col} for col in list_cols]
    columns[0]["name"] = ("Game Name",)
    columns[1]["name"] = "Min Players"
    columns[2]["name"] = "Max Players"
    columns[3]["name"] = "Min Playtime"
    columns[4]["name"] = "Max Playtime"
    columns[5]["name"] = "Year Published"
    columns[6]["name"] = "Categories"
    columns[7]["name"] = "Mechanics"
    columns[8]["name"] = "Publishers"
    columns[9]["name"] = "Avg. User Rating"
    columns[10]["name"] = "No. Ratings"

    table_out = app_wr.clean_table(table)
    data_out = table_out.to_dict("rows")
    return data_out, columns


# radio button selection options to populate dropdowns for tab3
@app.callback(
    dash.dependencies.Output("radio-dependent-tab3", "options"),
    [dash.dependencies.Input("radio-selection-tab3", "value")],
)
def update_options_tab3(chosen_selection):
    """
    :return: Callback to generate radio buttons on tab 3.
    """
    col = chosen_selection
    return [{"label": c, "value": c} for c in col_dict[col]]


# radio button selection options to populate game dropdown for tab3
@app.callback(
    Output("games-dependent-tab3", "options"),
    [Input("radio-selection-tab3", "value"), Input("radio-dependent-tab3", "value")],
)
def update_games_tab3(col, list_):
    """
    :return: Callback to generate drop down based on radio button selection on tab 3.
    """
    if col == "category":
        games = app_wr.call_boardgame_filter(boardgame_data, cat=list_)
    elif col == "mechanic":
        games = app_wr.call_boardgame_filter(boardgame_data, mech=list_)
    else:
        games = app_wr.call_boardgame_filter(boardgame_data, pub=list_)
    return games["name"].map(lambda x: {"label": x, "value": x})


# tsne graph tab 3
@app.callback(
    Output("tsne-3d-plot", "figure"),
    Input("radio-selection-tab3", "value"),
    Input("radio-dependent-tab3", "value"),
    Input("games-dependent-tab3", "value"),
)
def call_tsne_tab3(col, list_, game):
    """
    :return: Interactive TSNE plot tab 3.
    """
    fig = app_gr.graph_3D(boardgame_data, col, list_, game, extents_3d)
    return fig


# text output from tsne graph click
@app.callback(
    Output("tsne-data-out-name", "children"),
    Output("tsne-data-out-score", "children"),
    Output("tsne-data-out-ratings", "children"),
    Output("tsne-data-out-categories", "children"),
    Output("tsne-data-out-mechanics", "children"),
    Output("tsne-data-out-publishers", "children"),
    Input("tsne-3d-plot", "clickData"),
)
def display_click_message_tab3(clickData):
    """
    :return: Selected game data to put into control card on tab 3.
    """
    if clickData:
        click_point_np = np.array(
            [clickData["points"][0][i] for i in ["x", "y", "z"]]
        ).astype(np.float64)
        # Create a mask of the point clicked
        bool_mask_click = boardgame_data.loc[:, "x":"z"].eq(click_point_np).all(axis=1)
        # retreive data
        if bool_mask_click.any():
            data_out = boardgame_data[bool_mask_click]
            click_name = data_out.name.values[0]
            click_sc = "Avg Rating: " + str(round(data_out.average_rating.values[0], 2))
            click_rat = "No. of Ratings: " + str(data_out.users_rated.values[0])
            click_cat = ", ".join(data_out.category.values[0])
            click_mec = ", ".join(data_out.mechanic.values[0])
            click_pub = ", ".join(data_out.publisher.values[0])

        return click_name, click_sc, click_rat, click_cat, click_mec, click_pub
    return None, None, None, None, None, None


# slider output container first tab
@app.callback(
    dash.dependencies.Output("slider-output-container_2", "children"),
    [dash.dependencies.Input("min-num-ratings", "value")],
)
def update_output_tab1(value):
    """
    :return: Minimum number of games selected output
    text on tab 1 based on slider input.
    """
    return "Min Ratings: {}".format(value)


# slider output container second tab
@app.callback(
    dash.dependencies.Output("slider-output-container_3", "children"),
    [dash.dependencies.Input("min-num-ratings2", "value")],
)
def update_output_tab2(value):
    """
    :return: Minimum number of games selected
    output text on tab 2 based on slider input.
    """
    return "Min Ratings: {}".format(value)


# collapse button for top 10 games fact table
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse_tab2(n, is_open):
    """
    :return: Open top 10 games fact table on tab 2 if clicked.
    """
    if n:
        return not is_open
    return is_open


# run
if __name__ == "__main__":
    app.run_server(debug=False, host="127.0.0.1", port=8055)
