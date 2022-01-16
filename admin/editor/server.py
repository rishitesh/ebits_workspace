import pickle

import dash
import dash_bootstrap_components as dbc
import json
import bson
import datetime
from pymongo import MongoClient
from dash.dependencies import Input, Output, State, MATCH, ALL
from admin.editor.movie_view import final_layout
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

empty_result = [""]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = final_layout

client = MongoClient('mongodb://0.0.0.0:27017/')
mongodb = client.ebit_database


def get_cast_row(index, cast_name, cast_role, cast_image):
    return html.Div([
        dbc.Row(
            [
                dbc.Col(html.Label(str(index) + "."), width=1),
                dbc.Col(html.Label('Name'), width=1),
                dbc.Col(dbc.Input(id={'cast_name': index}, value=cast_name, type="text", bs_size="md",
                                  className="mb-3", debounce=True), width=2),
                dbc.Col(html.Label('Role:'), width=1),
                dbc.Col(
                    dbc.Input(id={'cast_role': index}, value=cast_role, type="text", bs_size="md",
                              className="mb-3", debounce=True),
                    width=2),
                dbc.Col(html.Label('Image:'), width=1),
                dbc.Col(dcc.Upload(
                    id={'cast_image': index},
                    children=html.Div(["", html.A("Select Files")]),
                    contents=cast_image,
                    style={
                        "width": "80%",
                        "height": "30px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "textAlign": "center",

                    },
                    # Allow multiple files to be uploaded
                    multiple=False,
                ), width=2)
            ]
        )]
    )


def get_critics_review(index, publication_name, review_author, review_rating, review_title, review_date, critic_review):
    return \
        html.Div([
            dbc.Row(
                [
                    dbc.Col(html.Label(index), width=1),
                    dbc.Col(html.Label('Publication'), width=1),
                    dbc.Col(dbc.Input(id={'publication_name': index}, value=publication_name, type="text", bs_size="md",
                                      className="mb-3", debounce=True), width=1),
                    dbc.Col(html.Label('Author:'), width=1),
                    dbc.Col(
                        dbc.Input(id={'review_author': index}, value=review_author, type="text", bs_size="md",
                                  className="mb-3", debounce=True),
                        width=1),
                    dbc.Col(html.Label('Rating:'), width=1),
                    dbc.Col(
                        dbc.Input(id={'review_rating': index}, value=review_rating, type="text", bs_size="md",
                                  className="mb-3", debounce=True),
                        width=1),
                    dbc.Col(html.Label('Title:'), width=1),
                    dbc.Col(
                        dbc.Input(id={'review_title': index}, value=review_title, type="text", bs_size="md",
                                  className="mb-3", debounce=True),
                        width=1),
                    dbc.Col(html.Label('Date:'), width=1),
                    dbc.Col(
                        dbc.Input(id={'review_date': index}, value=review_date, type="text", bs_size="md",
                                  className="mb-3", debounce=True),
                        width=1),
                    dbc.Col(html.Label('Critic Review:'), width=1),
                    dbc.Col(
                        dbc.Input(id={'critic_review': index}, value=critic_review, type="text", bs_size="md",
                                  className="mb-3", debounce=True),
                        width=1),

                ]
            )
        ]
        )


@app.callback(
    [
        Output('cast_container', 'children')
    ],
    [
        Input('add_cast', 'n_clicks')
    ],
    [
        State({"cast_name": ALL}, "value"),
        State({"cast_role": ALL}, "value"),
        State({"cast_image": ALL}, "value"),
    ])
def add_cast(n_clicks, all_cast_names, all_cast_roles, all_cast_images):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    print(triggered)
    adding = len([1 for i in triggered if i in ("add_cast.n_clicks")])
    clearing = len([1 for i in triggered if i == "clear-done.n_clicks"])
    new_spec = [
        (cast_name, cast_role, cast_image) for cast_name, cast_role, cast_image in zip(all_cast_names, all_cast_roles,
                                                                                       all_cast_images)
    ]

    new_list = []
    if n_clicks > 0:
        if len(new_spec) == 0:
            print("inside len 0")
            new_list.append(get_cast_row(0, None, None, None))
        else:
            index = 0
            for i, (cast_name, cast_role, cast_image) in enumerate(new_spec):
                new_list.append(get_cast_row(i, cast_name, cast_role, cast_image))
                index = index + 1

            new_list.append(get_cast_row(index, "", "", None))
    else:
        new_list = [dbc.Row()]

    final_lst = [html.Div(new_list)]
    return final_lst


@app.callback(
    Output('critic_review_container', 'children'),
    [
        Input('add_critic_review', 'n_clicks')
    ],
    [
        State({"publication_name": ALL}, "value"),
        State({"review_author": ALL}, "value"),
        State({"review_rating": ALL}, "value"),
        State({"review_title": ALL}, "value"),
        State({"review_date": ALL}, "value"),
        State({"critic_review": ALL}, "value")
    ]
    )
def add_critic_review(n_clicks, all_publication_name, all_review_author, all_review_rating, all_review_title, all_review_date,
                      all_critic_review):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    print(triggered)
    adding = len([1 for i in triggered if i in ("add_critic_review.n_clicks")])
    clearing = len([1 for i in triggered if i == "clear-done.n_clicks"])
    new_spec = [
        (publication_name, review_author, review_rating, review_title, review_date, critic_review)
        for publication_name, review_author, review_rating, review_title, review_date, critic_review
        in zip(all_publication_name, all_review_author, all_review_rating, all_review_title, all_review_date,
               all_critic_review)
    ]

    new_list = []
    if n_clicks > 0:
        if len(new_spec) == 0:
            print("inside len 0")
            new_list.append(get_critics_review(0, None, None, None, None, None, None))
        else:
            index = 0
            for i, (publication_name, review_author, review_rating, review_title, review_date, critic_review)  in enumerate(new_spec):
                new_list.append(get_critics_review(i, publication_name, review_author, review_rating, review_title, review_date, critic_review))
                index = index + 1

            new_list.append(get_critics_review(index, None, None, None, None, None, None))
    else:
        new_list = [dbc.Row()]

    final_lst = [html.Div(new_list)]
    return final_lst


@app.callback(
    [
        Output('output', 'children'),
    ],
    [
        Input('movie-add', 'n_clicks'),
        Input('movie-clear', 'n_clicks'),
    ],
    [
        State('movie_name', 'value'),
        State('movie_release_date', 'date'),
        State('positive', 'value'),
        State('negative', 'value'),
        State('neutral', 'value'),
        State('ebitRating', 'value'),
        State('genres', 'value'),
        State('awards', 'value'),
        State('certificates', 'value'),
        State('ebitsReview', 'value'),
        State('platforms', 'value'),
        State('languages', 'value'),
        State('labels', 'value'),
        State('trailers', 'value'),
        State('movie-photos', 'contents'),
    ]
)
def open_movie_add_new(add_clicks,
                       clear_button_clicks,
                       movie_name,
                       movie_release_date,
                       positive,
                       negative,
                       neutral,
                       ebits_rating,
                       genres,
                       awards,
                       certificates,
                       ebits_review,
                       platforms,
                       languages,
                       labels,
                       trailers,
                       photos,
                       ):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'movie-clear' in changed_id:
        return empty_result

    if add_clicks == 0:
        return empty_result

    post_dict = dict()
    post_dict["MovieName"] = movie_name
    post_dict["MovieReleaseDate"] = movie_release_date
    post_dict["Positive"] = positive
    post_dict["Negative"] = negative
    post_dict["Neutral"] = neutral
    post_dict["EbitRating"] = ebits_rating
    post_dict["Genres"] = genres
    post_dict["Awards"] = awards
    post_dict["Certificates"] = certificates
    post_dict["EbitsReview"] = ebits_review
    post_dict["Platforms"] = platforms
    post_dict["Languages"] = languages
    post_dict["Labels"] = labels
    post_dict["Trailers"] = trailers
    post_dict["PostDate"] = datetime.datetime.utcnow()

    photo_list = []
    if photos and len(photos) > 0:
        for content in photos:
            photo_list = photo_list + [bson.Binary(pickle.dumps(content))]

    post_dict["MoviePhotos"] = photo_list

    posts = mongodb.posts
    post_id = posts.insert_one(post_dict).inserted_id
    return_data = [str(post_id)]
    return return_data


if __name__ == '__main__':
    app.run_server(debug=True)
