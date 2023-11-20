
import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import os

def main():
    df = pd.read_csv('WK_1-10.csv')  # Replace 'path_to_your_file' with the actual path

    cols_to_sum = ['PASS_COMP', 'PASS_YDS', 'PASS_TD', 'RUSH_YDS', 'RUSH_TD', 'REC', 'REC_YARDS', 'REC_TD', 'TARGETS']
    all_columns = cols_to_sum + ['OPP']  # Include 'OPP' column

    positions = df['POS'].unique()
    #position dropdown
    dropdown_position = dcc.Dropdown(
        id='position-dropdown',
        options=[{'label': position, 'value': position} for position in positions],
        value=positions[0], 
        className='control'
    )
    #column checklist
    checklist_columns = dcc.Checklist(
        id='column-checklist',
        options=[{'label': col, 'value': col} for col in all_columns if col != 'OPP'],  # Exclude 'OPP'
        value=cols_to_sum,
        className='control'
    )
    #sort by dropdown
    sorting_dropdown = dcc.Dropdown(
        id='sorting-dropdown',
        options=[{'label': col, 'value': col} for col in cols_to_sum],
        value=cols_to_sum[0],
        className='control'
    )

    bar_graph = dcc.Graph(className='chart' ,id='bar-graph', figure={})  # Create the bar graph (initially empty

    app = Dash(__name__)

    app.layout = html.Div(className='master-div', children=[
        html.H1('Stats allowed by Each Team',className='title'),
        html.Div(className='controls-container', children=[
            html.Div(className='dropdown-container', children=[
                html.Div('Select Position to filter', className='control-title'),
                dropdown_position
            ]),
            html.Div(className='dropdown-container', children=[
                html.Div('Columns to show', className='control-title'),
                checklist_columns
            ]),
            html.Div(className='dropdown-container', children=[
                html.Div('Sort table by and graph', className='control-title'),
            sorting_dropdown
            ])
        ]),
        html.Div(className='charts-container',children=[
            dash_table.DataTable(id='datatable', page_size=32),
            bar_graph  # Include the bar graph in the layout
        ])
    ])

    @app.callback(
        Output('datatable', 'columns'),
        [Input('column-checklist', 'value')]
    )
    def update_columns(selected_columns):
        columns = [{'name': 'OPP', 'id': 'OPP'}]  # 'OPP' column will always be first
        columns += [{'name': i, 'id': i} for i in all_columns if i in selected_columns and i != 'OPP']
        return columns

    @app.callback(
    Output('datatable', 'data'),
    Output('bar-graph', 'figure'),  # Output for the bar graph
    [Input('position-dropdown', 'value'),
     Input('sorting-dropdown', 'value')]
)
    def update_table_and_graph(selected_position, selected_sorting_column):
        filtered_df = df[df['POS'] == selected_position]
        result = filtered_df.groupby('OPP')[cols_to_sum].sum().reset_index()
        result = result.sort_values(by=selected_sorting_column, ascending=False)  # Sort by the selected column

        # Prepare data for the bar graph
        bar_data = {
            'x': result['OPP'],
            'y': result[selected_sorting_column],
            'type': 'bar',
            'name': f'{selected_sorting_column} by OPP'
        }
        bar_layout = {'title': f'{selected_sorting_column} by OPP'}
        bar_figure = {'data': [bar_data], 'layout': bar_layout}

        return result.to_dict('records'), bar_figure  # Return data for table and bar graph


    app.run_server(debug=True)

if __name__ == '__main__':
    main()

  