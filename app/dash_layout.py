# import functions needed
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table

# import functions from .py files
from functions import *
from wrangling import subset_data

# dictionary for tab 1 sliders
slider_dict={
                                    1950: "1950",
                                    1955: "1955",
                                    1960: "1960",
                                    1965: "1965",
                                    1970: "1970",
                                    1975: "1975",
                                    1980: "1980",
                                    1985: "1985",
                                    1990: "1990",
                                    1995: "1995",
                                    2000: "2000",
                                    2005: "2005",
                                    2010: "2010",
                                    2015: "2015",
                                }

#  set up app stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# title
def title():
    """
    :return: A Div containing dashboard title.
    """
    return html.Div(children=[html.H1("Board Game Trends Dashboard")])

# description card tab 1
def description_card():
    """
    :return: A Div containing welcome message and descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Welcome to our Board Games Dashboard"),
            html.Div(
                id="intro",
                children="Explore board game trends over time based on category, mechanics and publisher selection below.\
                Also visualize the top categories, mechanics and publishers by year using our interactive features."
            ),
        ],
    )


# control card for tab 1
def generate_control_card():
    """
    :return: A Div containing controls for graphs on tab 1.
    """
    return html.Div(
        id="control-card",
        children=[
            
            html.Label("Select what you want to view:"),
            html.Br(),
            html.Br(),
            dcc.RadioItems(
                id="radio-selection",
                options=[
                    {"label": "Categories", "value": "category"},
                    {"label": "Mechanics", "value": "mechanic"},
                    {"label": "Publishers", "value": "publisher"},
                ],
                value="mechanic",
                labelStyle={"display": "block"},
            ),html.Br(),
            html.Label("Select elements to view:"),html.Br(),html.Br(),
            dcc.Dropdown(id="radio-dependent", options=[], multi=True, value=[None]),
        ],
    )


# control card for tab 2
def generate_control_card_tab2():
    """
    :return: A Div containing controls for graphs on tab 2.
    """
    return html.Div(
        id="control-card2",
        children=[
            html.P(
                "Please select any combination of categories, mechanics, publishers and number of games to show"
            ),
            html.Br(),
            html.P("Please select categories:"),
            dcc.Dropdown(
                id="category-widget",
                value="Economic",
                options=[
                    {"label": name, "value": name} for name in subset_data("category")
                ],
                multi=True,
            ),
            
            html.Br(),
            html.P("Please select mechanics:"),
            dcc.Dropdown(
                id="mechanics-widget",
                value="Trick-taking",
                options=[
                    {"label": name, "value": name} for name in subset_data("mechanic")
                ],
                multi=True,
            ),
            
            html.Br(),
            html.P("Please select publishers:"),
            dcc.Dropdown(
                id="publisher-widget",
                value="3M",
                options=[
                    {"label": name, "value": name} for name in subset_data("publisher")
                ],
                multi=True
            ),
            html.Br(),
            html.Br(),
        ],
    )


# lower description for tab 1
def lower_description():
    """
    :return: A Div containing descritption for lower portion of tab 1.
    """
    return html.Div(
        children=[
            html.H4("Top 5 Categories, Mechanics and Publishers by Rating"),
            html.P(
                "Two sets of bar charts with year range sliders are provided to allow comparison for two different periods.",

            ), html.Br(),
            html.P("Drag the year sliders below to select your year ranges and compare the top 5 categories, mechanics and publishers \
                    between time periods.")
        ]
    )


# data set description for tab 1
def data_set_descirption():
    """
    :return: A Div containing descritption of the data set for tab 1.
    """
    return html.Div(
        children=[
            html.H4("Description of Dataset"),
            html.P(
                " This dataset comes from the Board Game Geek website and includes boardgames with descriptions, general game \
                    details, publisher, and user ratings for 10,000 boardgames published between 1950 and 2021."
            ),
        ]
    )


# below are the cards that are used in the layout


# card 1 containing the description and control card for tab 1
first_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                id="left-column",
                className="four columns",
                children=[
                    description_card(),
                    html.Br(),
                    generate_control_card(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                ],
            )
        ]
    )
)
# card 2 containing the two plots on upper portion of tab 1, the scatter plot and the counts stacked histogram
second_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.H4("Board Game Ratings and Counts from 1950 to 2016"),
                    html.P(
                        "Select either categories, mechanics or publishers. Then select different elements to view on the following two figures."
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
                    html.Iframe(
                        # stacked histogram
                        id="count",
                        style={
                            "border-width": "0",
                            "width": "100%",
                            "height": "250px",
                        },
                    ),
                ]
            ), html.Br(), html.Br()
        ]
    )
)


# card 3 containing the lowe description and collapsable data set description for tab 1
third_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Col(
                id="bottom left row",
                className="four columns",
                children=[
                    lower_description(),
                    
                ],
            )
        ]
    )
)

# card 4 containing the top slider and bar charts to view top categories, mechanics and publishers for selected time periods from the slider for tab 1
fourth_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    html.Div(
                        [
                            html.Iframe(
                                id="output-container-range-slider-non-linear",
                                style={
                                    "border-width": "0",
                                    "width": "315px",
                                    "height": "250px",
                                },
                            ),
                            html.Iframe(
                                id="output-container-range-slider-non-linear2",
                                style={
                                    "border-width": "0",
                                    "width": "315px",
                                    "height": "250px",
                                },
                            ),
                            html.Iframe(
                                id="output-container-range-slider-non-linear3",
                                style={
                                    "border-width": "0",
                                    "width": "315px",
                                    "height": "250px",
                                },
                            ),
                            dcc.RangeSlider(
                                id="non-linear-range-slider",
                                min=1950,
                                max=2016,
                                step=1,
                                value=[1990, 2010],
                                marks=slider_dict,
                            ),
                            html.Div(id="output-container-range-slider"),
                        ]
                    )
                ]
            )
        ]
    )
)

# card 5 containing the bottom slider and bar charts to view top categories, mechanics and publishers for selected time periods from the slider for tab 1
fifth_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    html.Div(
                        [
                            html.Iframe(
                                id="output-container-range-slider-non-linear4",
                                style={
                                    "border-width": "0",
                                    "width": "315px",
                                    "height": "250px",
                                },
                            ),
                            html.Iframe(
                                id="output-container-range-slider-non-linear5",
                                style={
                                    "border-width": "0",
                                    "width": "315px",
                                    "height": "250px",
                                },
                            ),
                            html.Iframe(
                                id="output-container-range-slider-non-linear6",
                                style={
                                    "border-width": "0",
                                    "width": "315px",
                                    "height": "250px",
                                },
                            ),
                            dcc.RangeSlider(
                                id="non-linear-range-slider2",
                                min=1950,
                                max=2016,
                                step=1,
                                value=[1990, 2010],
                                marks=slider_dict,
                            ),
                            html.Div(id="output-container-range-slider2"),
                        ]
                    )
                ]
            )
        ]
    )
)

# card 6 containing the control card and the silder for number of games for tab 2
sixth_card = dbc.Card(
    dbc.CardBody(
        [
            generate_control_card_tab2()
            
        ]
    )
)

# card 7 containing the top 10 games bar chart for tab 2
seventh_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                html.Iframe(
                    id="top_n_games",
                    style={
                        "border-width": "0",
                        "width": "100%",
                        "height": "300px",
                    }
                )
            )
        ]
    )
)

# card 8 containing the data table for the top n games for tab 2
eigth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Top 10 Games Facts Table:"),
            dash_table.DataTable(
                id="top_n_games_datatable",
                style_cell={
                    "whiteSpace": "normal",
                    "height": "auto",
                },
                style_table={
        'overflowY': 'scroll'
    },
                sort_action="native",
            ),
        ]
    )
)

# card 9 for data set description tab 1
ninth_card = dbc.Card(
    dbc.CardBody(
        [html.Div(
                        [
                            dbc.Button(
                                "Click here to view dataset description",
                                id="collapse-button",
                                className="mb-3",
                                color="primary",
                            ),
                            dbc.Collapse(
                                dbc.Card(dbc.CardBody(data_set_descirption())),
                                id="collapse",
                            ),
                        ]
                    )
        ]
    )
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

# app layout
app.layout = html.Div(
    [
        dbc.Container(
            [  # dashboard title
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    id="title_top",
                                    className="title on top",
                                    children=[title()],
                                )
                            ],
                            width=12,
                        )
                    ]
                )
            ]
        ),
        dcc.Tabs(
            [
                # tab 1
                dcc.Tab(
                    label="Game Dynamics Over Time",
                    children=[
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(first_card, width=3),
                                dbc.Col(second_card, width=9),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col([third_card,html.Br(), ninth_card] ,width=3),
                                dbc.Col([(fourth_card), html.Br(), (fifth_card)], width=9),
                            ],
                        ),
                    ],
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Top Games",
                    children=[
                        dbc.Container(
                            [ html.Br(),
                        html.Br(),
                        html.Br(),
                                
                                dbc.Row(
                                    [
                                        dbc.Col(sixth_card, width=3),
                                        dbc.Col(
                                            [(seventh_card),  html.Br(), (eigth_card)], width=9,style={'height':'100vh'}
                                        ),
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
    ]
)


# Set up callbacks/backend

# scatter plot tab 1
@app.callback(
    Output("scatter", "srcDoc"),
    Input("radio-selection", "value"),
    Input("radio-dependent", "value"),
)
def call_scatter(col, list_):
    chart = scatter_plot_dates(col, list_)
    return chart.to_html()


# stacked histogram of counts annual published counts
@app.callback(
    Output("count", "srcDoc"),
    Input("radio-selection", "value"),
    Input("radio-dependent", "value"),
)
def call_counts(col, list_):
    chart2 = count_plot_dates(col, list_)
    return chart2.to_html()


# 1st catergory bar chart tab 1
@app.callback(
    Output("output-container-range-slider-non-linear", "srcDoc"),
    Input("non-linear-range-slider", "value"),
)

# considering making general function for milestone 4
def update_output(value):
    transformed_value = [v for v in value]
    val1 = transformed_value[0]
    val2 = transformed_value[1]
    hist1 = rank_plot_dates(
        col="category", year_in=int(val1), year_out=int(val2), color_="#ff7f0e"
    )
    return hist1.to_html()


# 1st mechanics bar chart tab 1
@app.callback(
    Output("output-container-range-slider-non-linear2", "srcDoc"),
    Input("non-linear-range-slider", "value"),
)
def update_output2(value):
    transformed_value = [v for v in value]
    val1 = transformed_value[0]
    val2 = transformed_value[1]
    hist2 = rank_plot_dates(
        col="mechanic", year_in=int(val1), year_out=int(val2), color_="#17becf"
    )
    return hist2.to_html()


# 1st publisher bar chart tab 1
@app.callback(
    Output("output-container-range-slider-non-linear3", "srcDoc"),
    Input("non-linear-range-slider", "value"),
)
def update_output3(value):
    transformed_value = [v for v in value]
    val1 = transformed_value[0]
    val2 = transformed_value[1]
    hist3 = rank_plot_dates(
        col="publisher", year_in=int(val1), year_out=int(val2), color_="#e377c2"
    )
    return hist3.to_html()


# 2nd catergory bar chart tab 1


@app.callback(
    Output("output-container-range-slider-non-linear4", "srcDoc"),
    Input("non-linear-range-slider2", "value"),
)
def update_output4(value):
    transformed_value = [v for v in value]
    val1 = transformed_value[0]
    val2 = transformed_value[1]
    hist4 = rank_plot_dates(
        col="category", year_in=int(val1), year_out=int(val2), color_="#ff7f0e"
    )
    return hist4.to_html()


# 2nd mechanics bar chart tab 1
@app.callback(
    Output("output-container-range-slider-non-linear5", "srcDoc"),
    Input("non-linear-range-slider2", "value"),
)
def update_output5(value):
    transformed_value = [v for v in value]
    val1 = transformed_value[0]
    val2 = transformed_value[1]
    hist5 = rank_plot_dates(
        col="mechanic", year_in=int(val1), year_out=int(val2), color_="#17becf"
    )
    return hist5.to_html()


# 2nd publishers bar chart tab 1
@app.callback(
    Output("output-container-range-slider-non-linear6", "srcDoc"),
    Input("non-linear-range-slider2", "value"),
)
def update_output6(value):
    transformed_value = [v for v in value]
    val1 = transformed_value[0]
    val2 = transformed_value[1]
    hist6 = rank_plot_dates(
        col="publisher", year_in=int(val1), year_out=int(val2), color_="#e377c2"
    )
    return hist6.to_html()


# 1st year range slider output tab 1


@app.callback(
    dash.dependencies.Output("output-container-range-slider", "children"),
    dash.dependencies.Input("non-linear-range-slider", "value"),
)
def range_slider_select(value):
    transformed_value = [v for v in value]
    return "{} to {}".format(transformed_value[0], transformed_value[1])


# 2nd year range slider output tab 1


@app.callback(
    dash.dependencies.Output("output-container-range-slider2", "children"),
    dash.dependencies.Input("non-linear-range-slider2", "value"),
)
def range_slider_select2(value):
    transformed_value = [v for v in value]
    return "{} to {}".format(transformed_value[0], transformed_value[1])


# collapsable data set description
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# radio button selection options to populate drop down
@app.callback(
    dash.dependencies.Output("radio-dependent", "options"),
    [dash.dependencies.Input("radio-selection", "value")],
)
def update_options(chosen_selection):
    col = chosen_selection
    return [
        {
            "label": c,
            "value": c,
        }
        for c in subset_data(col)
    ]


# top n games bar chart tab 2
@app.callback(
    Output("top_n_games", "srcDoc"),
    Input("category-widget", "value"),
    Input("mechanics-widget", "value"),
    Input("publisher-widget", "value")
    
)
def call_top_n_games(c, m, p, n=10):
    top_n_games = top_n_plot(cat=c, mech=m, pub=p, n=10)
    return top_n_games.to_html()


# data table top n games bar chart tab 2
@app.callback(
    Output("top_n_games_datatable", "data"),
    Output(component_id="top_n_games_datatable", component_property="columns"),
    Input("category-widget", "value"),
    Input("mechanics-widget", "value"),
    Input("publisher-widget", "value")
    
)
def update_table(c, m, p, n=10):
    list_cols = ["name", "min_players", "max_players", 'min_playtime', 'max_playtime',"playing_time", 'year_published','category','mechanic','family', "artist", 'designer','publisher', 'average_rating', 'users_rated']
    table = call_boardgame_filter(cat=c, mech=m, pub=p, n=10)
    columns = [{"name": col, "id": col} for col in list_cols]
    columns[0]["name"] = ("Game name",)
    columns[1]["name"] = ("Minumum number of players")
    columns[2]["name"] = ("Minumum number of playerss")
    columns[3]["name"] = ("Minimum Playtime")
    columns[4]["name"] = ("Maximum Playtime")
    columns[5]["name"] = ('Playing time')
    columns[6]["name"] = ('Year published')
    columns[7]["name"] = ("Game category")
    columns[8]["name"] = ("Game mechanic")
    columns[9]["name"] = ("Game family")
    columns[10]["name"] = ("Game artist")
    columns[11]["name"] = ("Game designer")
    columns[12]["name"] = ("Game publisher")
    columns[13]["name"] =("Average game rating")
    columns[14]["name"] = ("User rating")


    data = table.to_dict("rows")
    return data, columns


# run
if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8055)