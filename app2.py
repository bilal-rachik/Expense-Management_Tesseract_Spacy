import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


from dash.dependencies import Input, Output

from datetime import datetime as dt


app = dash.Dash(

)
server = app.server


# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.png")
                        ),
                        html.H2("DASH - UBER DATA APP"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different time frames on the histogram."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2014, 4, 1),
                                    max_date_allowed=dt(2014, 9, 30),
                                    initial_visible_month=dt(2014, 4, 1),
                                    date=dt(2014, 4, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",

                                            placeholder="Select a location",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Select certain hours",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                "Source: [FiveThirtyEight](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)"
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Select any of the bars on the histogram to section data by time."
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

# Gets the amount of days in the specified month
# Index represents month (0 is April, 1 is May, ... etc.)
daysInMonth = [30, 31, 30, 31, 31, 30]

# Get index for the specified month in the dataframe
monthIndex = pd.Index(["Apr", "May", "June", "July", "Aug", "Sept"])

# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected

    # Put selected times into a list of numbers xSelec
# Selected Data in the Histogram updates the Values in the DatePicker
@app.callback(
    Output("bar-selector", "value"),
    [Input("histogram", "selectedData"), Input("histogram", "clickData")],
)
def update_bar_selector(value, clickData):
    holder = []
    if clickData:
        holder.append(str(int(clickData["points"][0]["x"])))
    if value:
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    if clickData:
        return {"points": []}











if __name__ == "__main__":
    app.run_server(debug=True,port=5050)