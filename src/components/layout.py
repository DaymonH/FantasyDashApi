from dash import Dash, html, dash_table
from dash.dependencies import Input, Output
from dash_core_components import Input
import pandas as pd


def create_layout(app: Dash) -> html.Div:
    df = pd.read_csv('dash/WK_1-10.csv')
    # cols to group by
    cols_to_sum = ['PASS_COMP', 'PASS_YDS', 'PASS_TD', 'RUSH_YDS', 'RUSH_TD', 'REC', 'REC_YARDS', 'REC_TD', 'TARGETS']
    result = df.groupby('OPP')[cols_to_sum].sum().reset_index()

    positions = df['POS'].unique()  # Get unique positions from the dataframe

    # Create radio items for positions
    radio_items = [html.Label([html.Input(type='radio', id='radio', name='position', value=position), position]) for position in positions]

    
    # Callback to update the table based on selected position
    @app.callback(
        Output('datatable', 'data'),
        Input('radio', 'value')
    )
    def update_table(selected_position):
        # Filter the dataframe based on selected position
        filtered_df = df[df['POS'] == selected_position]
        result = filtered_df.groupby('OPP')[cols_to_sum].sum().reset_index()
        return result.to_dict('records')

    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(children='Fantasy Football Dashboard'),
            # Radio buttons for positions
            html.Div(radio_items),

            # Table for displaying data
            dash_table.DataTable(id='datatable', page_size=32)
        ]
    )
