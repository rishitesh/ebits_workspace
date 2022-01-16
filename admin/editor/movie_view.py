import dash_bootstrap_components as dbc
import dash_core_components as dcc

from datetime import date

import dash_html_components as html
import dash_table
from admin.editor.view_constants import *

LIGHT_BLUE_LEFT_ALLIGNED_STYLE ={'textAlign': 'left', 'color': '#7FDBFF'}
LIGHT_BLUE_CENTER_ALLIGNED_STYLE ={'textAlign': 'center', 'color': '#7FDBFF'}
CARD_STYLE = {"width": "10rem", "color":"#800000"}
TOP_MARGIN = {"margin-top": "15px"}

empty_row = html.Div([dbc.Row([dbc.Col(html.Div(style=CARD_STYLE))])])

movie_form = html.Div(
[

        # Movie Name
        dbc.Row(
            [
                dbc.Col(html.Label('Movie Name:'), width=2),
                dbc.Col(dbc.Input(id='movie_name', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True), width=6),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Release Date:'), width=2),
                dbc.Col(dcc.DatePickerSingle(
                            id='movie_release_date',
                            min_date_allowed=date(1925, 8, 5),
                            max_date_allowed=date(2075, 9, 19),
                            initial_visible_month=date(2022, 1, 1),
                            date=date(2022, 1, 1)
                 ), width=4),
            ]
        ),

        dbc.Row(
                dbc.Col(html.Label('Sentiments:'), width=2),
        ),
        dbc.Row(
            [

                dbc.Col(html.Label('Positive'), width=2),
                dbc.Col(dbc.Input(id='positive', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True,
                                  style={'width': '20%', 'display': 'inline-block', 'padding': '0 20'}), width=2),
                dbc.Col(html.Label('Negative'), width=1),
                dbc.Col(dbc.Input(id='negative', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True,
                                  style={'width': '20%', 'display': 'inline-block', 'padding': '0 20'}), width=2),
                dbc.Col(html.Label('Neutral'), width=1),
                dbc.Col(dbc.Input(id='neutral', placeholder="", type="text", bs_size="sx", className="mb-6", debounce=True,
                                  style={'width': '20%', 'display': 'inline-block', 'padding': '0 20'}), width=2),
            ]
        ),

        dbc.Row(
                [
                    dbc.Col(html.Label('Ebit Rating:'), width=2),
                    dbc.Col(dbc.Input(id='ebitRating', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True,
                                      style={'width': '20%', 'display': 'inline-block', 'padding': '0 20'}), width=2),
                ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Label('Genres:'), width=2),
                dbc.Col(dbc.Input(id='genres', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True), width=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Awards:'), width=2),
                dbc.Col(dbc.Input(id='awards', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True), width=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Certificates:'), width=2),
                dbc.Col(dbc.Input(id='certificates', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True), width=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Storyline:'), width=2),
                dbc.Col(dbc.Textarea(id='storyline', style={'width': '100%', 'height': 100, 'padding':2}, debounce=True), width=8),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Ebits Review:', style=TOP_MARGIN), width=2),
                dbc.Col(
                    dbc.Textarea(id='ebitsReview', placeholder="", style={'width': '100%', 'height': 100, 'margin-top':15},
                                 debounce=True),
                    width=8),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Platforms:', style=TOP_MARGIN), width=2),
                dbc.Col(dbc.Input(id='platforms', placeholder="", type="text", bs_size="md", className="mb-3",
                                  style=TOP_MARGIN,  debounce=True), width=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Languages:'), width=2),
                dbc.Col(dbc.Input(id='languages', placeholder="", type="text", bs_size="md", className="mb-3",
                                  debounce=True), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Label('Labels:'), width=2),
                dbc.Col(dbc.Input(id='labels', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Label('Trailers:'), width=2),
                dbc.Col(dbc.Input(id='trailers', placeholder="", type="text", bs_size="md", className="mb-3", debounce=True), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Label('Movie Photos:'), width=2),
                dbc.Col(
                    dcc.Upload(
                        id="movie-photos",
                        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                        style={
                            "width": "80%",
                            "height": "30px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                        },
                        # Allow multiple files to be uploaded
                        multiple=True,
                    ),
                    width=6),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Cast & Crew:', style=TOP_MARGIN), width=2),
                dbc.Col(dbc.Button(children='Click To Add', id="add_cast", n_clicks=0, className="mr-1", style=TOP_MARGIN), width=0.5),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(id="cast_container", style=TOP_MARGIN), width=8),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Label('Critic Reviews:', style=TOP_MARGIN), width=2),
                dbc.Col(dbc.Button(children='Click To Add', id="add_critic_review", n_clicks=0, className="mr-1", style=TOP_MARGIN), width=0.5),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(id="critic_review_container", style=TOP_MARGIN), width=8),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(dbc.Button(children='Add', id="movie-add", n_clicks=0, color="success", className="mr-1"), width=0.5),
                dbc.Col(dbc.Button(children='Modify', id="movie-modify", n_clicks=0, color="success", className="mr-1"),width=0.5),
                dbc.Col(dbc.Button(children='Clear', id="movie-clear", n_clicks=0, color="success", className="mr-1"), width=0.5),
            ]
        ),
        html.Div(id="output")
    ]

)




final_layout = html.Div(

    [
        html.H4(children='EBit Movie Editor', style=LIGHT_BLUE_CENTER_ALLIGNED_STYLE),
        dbc.Spinner(html.Div(id="loading-output"), color="secondary"),
        movie_form
    ]

)