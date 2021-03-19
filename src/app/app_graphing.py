"""
contains graph calls for dashboard
"""

import altair as alt
import app_wrangling as app_wr
import plotly.graph_objs as go


def scatter_plot_dates(data, col="category", list_=[None]):
    """
    Takes in inputs filtering data and creates scatter plot
    for comparison of user ratings over time

    data: a pandas df generated from app_wrangling.call_boardgame_data()
    col: string
    list_: list

    returns: altair plot
    """
    alt.data_transformers.disable_max_rows()

    if (list_ == [None]) or (not list_):
        set_data = data
        set_color = alt.value("grey")
    else:
        set_data = app_wr.call_boardgame_radio(data, col, list_).explode("group")
        set_color = alt.Color("group:N", title="Group")

    reduced_data = app_wr.remove_columns(set_data)

    scatter_plot = (
        alt.Chart(reduced_data)
        .mark_circle(size=60, opacity=0.2)
        .encode(
            alt.X(
                "year_published:T",
                axis=alt.Axis(title=None),
                scale=alt.Scale(zero=False),
            ),
            alt.Y(
                "average_rating:Q",
                axis=alt.Axis(
                    title="Average Rating",
                    titleFontSize=12,
                    offset=14,
                    titleFontWeight=600,
                ),
            ),
            color=set_color,
            tooltip=[
                alt.Tooltip("name:N", title="Name"),
                alt.Tooltip("average_rating:Q", title="Average Rating"),
                alt.Tooltip("year_published:T", title="Year Published", format="%Y"),
            ],
        )
        .properties(
            title=alt.TitleParams(
                text="Game Popularity based on Published Year",
                subtitle="Light grey line shows annual average rating of ALL games",
                anchor="start",
                fontSize=20,
                dy=-20,
                dx=20,
            ),
            width=650,
            height=150,
        )
    )

    # THIS NEEDS TO BE DONE OUTSIDE OF ALTAIR
    # OR IDEALLY USE EXPIREMENTAL ALTAIR TRANSFORMER
    line_plot = (
        alt.Chart(data[["year_published", "average_rating"]])
        .mark_line(color="dark grey", size=3)
        .encode(x="year_published:T", y="mean(average_rating)")
    )

    scatter_plot = scatter_plot + line_plot
    return scatter_plot


def count_plot_dates(data, col="category", list_=[None]):
    """
    Takes input filtering data and creates
    a plot counting how many game occurrences

    data: a pandas df generated from app_wrangling.call_boardgame_data()
    col: string
    list_: list of strings input

    return: altair plot
    """
    alt.data_transformers.disable_max_rows()

    if (list_ == [None]) or (not list_):
        set_data = data
        set_color = alt.value("#2ca02c")
    else:
        set_data = app_wr.call_boardgame_radio(data, col, list_).explode("group")
        set_color = alt.Color("group:N", title="Group")

    reduced_data = app_wr.remove_columns(set_data)

    alt.data_transformers.disable_max_rows()
    count_plot = (
        alt.Chart(reduced_data)
        .mark_bar()
        .encode(
            alt.X(
                "year_published:T",
                axis=alt.Axis(title=None),
                scale=alt.Scale(zero=False),
            ),
            alt.Y(
                "count():Q",
                axis=alt.Axis(
                    title="Count of Games Published",
                    titleFontSize=12,
                    offset=8,
                    titleFontWeight=600,
                ),
            ),
            color=set_color,
            tooltip=[
                alt.Tooltip("group:N", title="Group"),
                alt.Tooltip("count():Q", title="Number of Games"),
                alt.Tooltip("year_published:T", title="Year_Published", format="%Y"),
            ],
        )
        .properties(
            title=alt.TitleParams(
                text="Game Count based on Published Year",
                anchor="start",
                fontSize=20,
                dy=-20,
                dx=20,
            ),
            width=650,
            height=150,
        )
    )

    return count_plot


def rank_plot_dates(
    data, col="category", year_in=1990, year_out=2010, color_="#ff7f0e"
):
    """
    Creates altair graph of set column for set years

    data: a pandas df generated from app_wrangling.call_boardgame_data()
    col: string
    year_in: int
    year_out: int

    return: altair plot
    """
    plot_data = app_wr.call_boardgame_top(data, col, year_in, year_out)

    rank_plot = (
        alt.Chart(plot_data)
        .mark_bar(color=color_)
        .encode(
            alt.X(
                str(col) + ":N",
                sort="-y",
                axis=alt.Axis(titleFontSize=12, titleFontWeight=600),
            ),
            alt.Y(
                "average_rating:Q",
                axis=alt.Axis(title="Average Rating"),
                scale=alt.Scale(domain=(5, 10)),
            ),
        )
        .properties(width=250, height=75)
    )

    rank_text = rank_plot.mark_text(align="center", baseline="bottom", dy=-3).encode(
        text=alt.Text("average_rating:Q", format=",.2r")
    )
    return rank_plot + rank_text


def rank_plot_facet(data, year_in=1990, year_out=2010):
    """
    Facets altair graphs

    data: a pandas df generated from app_wrangling.call_boardgame_data()
    year_in: int
    year_out: int

    return: altair plot
    """
    return alt.hconcat(
        rank_plot_dates(
            data=data,
            col="category",
            year_in=year_in,
            year_out=year_out,
            color_="#ff7f0e",
        ),
        rank_plot_dates(
            data=data,
            col="mechanic",
            year_in=year_in,
            year_out=year_out,
            color_="#17becf",
        ),
        rank_plot_dates(
            data=data,
            col="publisher",
            year_in=year_in,
            year_out=year_out,
            color_="#e377c2",
        ),
    )


def top_n_plot(data, cat=[None], mech=[None], pub=[None], n=10):
    """
    Creates altair graph for top "n" games with filtered data

    data: a pandas df generated from app_wrangling.call_boardgame_data()
    cat: list
    mech: list
    pub: list
    n: int

    return: altair plot
    """
    plot_data = app_wr.call_boardgame_filter(data, cat, mech, pub, n)

    alt.data_transformers.disable_max_rows()
    top_plot = (
        alt.Chart(plot_data)
        .mark_bar()
        .encode(
            alt.X("name:N", sort="-y", axis=alt.Axis(title=None, labels=False)),
            alt.Y(
                "average_rating:Q",
                axis=alt.Axis(title="Average Rating"),
                scale=alt.Scale(domain=(0, 10)),
            ),
            color=alt.Color(
                "name:N",
                title="Boardgame Name",
                sort=alt.EncodingSortField("-y", order="descending"),
            ),
            tooltip=[
                alt.Tooltip("name", title="Name"),
                alt.Tooltip("users_rated", title="# of Ratings"),
            ],
        )
        .properties(
            title=alt.TitleParams(
                text="Top 10 Games Based on User Selection",
                anchor="start",
                fontSize=20,
                dy=-20,
                dx=20,
            ),
            width=500,
            height=200,
        )
    )
    top_text = top_plot.mark_text(align="center", baseline="bottom", dy=-3).encode(
        text=alt.Text("average_rating:Q", format=",.2r")
    )

    return top_plot + top_text


def graph_3D(data, col="category", list_=[None], game=None):
    """
    3D t-sne graph data output

    data: a pandas df generated from app_wrangling.call_boardgame_data()
    col: string
    list_: list
    game: string (default None)

    return: fig_out, 3D plotly figure
    """
    # layout for the 3D plot
    axes = dict(
        title="",
        showgrid=True,
        zeroline=False,
        showticklabels=False,
        showspikes=False,
    )
    layout_out = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(xaxis=axes, yaxis=axes, zaxis=axes),
        legend=dict(yanchor="top", y=0.93, xanchor="right", x=0.99),
    )

    # plotting data
    if (list_ == [None]) or (not list_):
        set_data = data.copy(deep=True)
        set_data["group"] = "none"
    else:
        set_data = app_wr.call_boardgame_radio(data, col, list_).explode("group")

    data_out = []
    for idx, val in set_data.groupby(set_data.group):
        if idx == "none":
            marker_style = dict(
                size=val["average_rating"] * 1.6,
                symbol="circle",
                opacity=0.1,
                color="grey",
            )
            legend_show = False

        else:
            marker_style = dict(
                size=val["average_rating"] * 1.6, symbol="circle", opacity=0.4
            )
            legend_show = True

        scatter = go.Scatter3d(
            name=idx,
            x=val["x"],
            y=val["y"],
            z=val["z"],
            mode="markers",
            marker=marker_style,
            text=val["name"],
            hoverinfo="text+name",
            showlegend=legend_show,
        )
        data_out.append(scatter)

    if game:
        game_data = data[data["name"] == game]
        marker_style = dict(
            size=game_data["average_rating"] * 1.6,
            symbol="circle",
            opacity=1.0,
            color="violet",
        )

        scatter = go.Scatter3d(
            name=game,
            x=game_data["x"],
            y=game_data["y"],
            z=game_data["z"],
            mode="markers",
            marker=marker_style,
            text=game_data["name"],
            hoverinfo="text",
        )
        data_out.append(scatter)

    fig_out = {"data": data_out, "layout": layout_out}

    return fig_out
