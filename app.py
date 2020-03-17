import uuid
import pathlib
from images_trasfo.orient import image_to_text
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_reusable_components as drc
from dash.dependencies import Input, Output, State
from process_text.process import clean_text

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

app = dash.Dash(__name__)
server = app.server

def serve_layout():
    # Generates a session ID
    session_id = str(uuid.uuid4())

    # Post the image to the right key, inside the bucket named after the
    # session ID
    #store_image_string(utils.IMAGE_STRING_PLACEHOLDER, session_id)

    # App Layout
    return html.Div(
        id="root",
        children=[
            # Session ID
            #html.Div(session_id, id="session-id"),

            # Main body
            html.Div(
                id="app-container",
                className="row",
                children=[
                    # Banner display
                    html.Div(
                        id="banner",
                        children=[
                            html.Img(
                                id="logo", src=app.get_asset_url("Bigapps.png")
                                    ),
                            html.H2("Image Processing App", id="title"),
                                ],
                        ),
                    html.Div(
                        children=[
                            html.Div(className="seven columns",
                                 children=[html.Label('Images', style={'marginRight': 50}),
                            html.Div(
                                 id="image",
                                 children=[
                                     html.Div(
                                         id="div-interactive-image",
                                              ),
                                          ],
                                     )
                                 ]
                                ),
                            html.Div(
                            children=[
                                html.Label('Text', style={'marginRight': 60}),
                                dcc.Textarea(
                                id='textarea',
                                #maxLength='50%',
                                placeholder='Text output...',
                                style=

                                {'width': '40%', 'height': '100%', 'backgroundColor': '#272a31', 'color': '#fff',
                                 'min-width':'50px','max-width':'100%','min-height':'500px'

                                 }

                                    )
                                ]
                                )
                            ]),
                    ],
                ),
            # Sidebar
            html.Div(
                id="sidebar",
                children=[
                    drc.Card(
                        [
                          dcc.Upload(
                                id="upload-image",
                                children=[
                                    "Drag and Drop or ",
                                    html.A(children="Select an Image"),
                                ],
                                # No CSS alternative here
                                style={
                                    "color": "darkgray",
                                    "width": "100%",
                                    "height": "50px",
                                    "lineHeight": "50px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "borderColor": "darkgray",
                                    "textAlign": "center",
                                    "padding": "2rem 0",
                                    "margin-bottom": "2rem",
                                },
                                multiple=True,
                                accept="image/*",
                            ),

                        ]
                    ),
                    html.Div([

                        html.Label('TTC'),
                        dcc.Input(id='TTC', value='', type='text')
                    ,html.Label('Date de la dépense'),
                    dcc.Input(
                        id='DATE',type='text'),
                        html.Label('Adress'),
                        dcc.Input(id ='ADRESS', value='', type='text'),
                        html.Label('Marchand'),
                        dcc.Input(id='Marchand', value='', type='text')

                              ])
                ],
            ),
        ],
    )


app.layout = serve_layout

import pytesseract

# Installs: https://www.learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/


import spacy
import os
from process_model.get_model import my_nlp

model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'model')
nlp = my_nlp(model_dir)
def text_to_ner(text):
    doc = nlp(text)
    # print("Entities in '%s'" % test_text)
    print([(ent.text, ent.label_) for ent in doc.ents])

    entety_date = ''
    entety_adress= ''
    entety_ttc = ''
    entety_marchant = ''

    for ent in doc.ents:
        if ent.label_=="TTC":
            entety_ttc = ent.text
        if ent.label_=="Date":
            entety_date = ent.text
        if ent.label_ =="Adress":
            entety_adress = ent.text
        if ent.label_ =="Marchand":
            entety_marchant = ent.text
    return entety_date,entety_adress,entety_ttc,entety_marchant

def parse_contents(contents, filename, date):
    return html.Div([

            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=contents,width="55%",height="100%"),

        ])
@app.callback([Output('div-interactive-image', 'children'),
            Output('textarea', 'value'),
            Output('DATE', 'value'),
            Output('ADRESS', 'value'),
            Output('TTC', 'value'),
               Output('Marchand', 'value')],
            [Input('upload-image', 'contents')],
            [State('upload-image', 'filename'),
            State('upload-image', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        # Parse the string and convert to pil
        string = list_of_contents[0].split(';base64,')[-1]
        im_pil = drc.b64_to_pil(string)
        text = image_to_text(im_pil)
        txt = clean_text(text)
        print(txt)

        Date,adress,ttc,Marchand = text_to_ner(txt)

        print(Date,adress,ttc)

        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children,text,Date,adress,ttc,Marchand

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)