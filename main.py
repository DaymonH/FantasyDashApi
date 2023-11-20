import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import os
print (os.getcwd())
print (os.listdir())
def main():
    df = pd.read_csv('WK_1-10.csv')  # Replace 'path_to_your_file' with the actual path
    
    cols_to_sum = ['PASS_COMP', 'PASS_YDS', 'PASS_TD', 'RUSH_YDS', 'RUSH_TD', 'REC', 'REC_YARDS', 'REC_TD', 'TARGETS']
    all_columns = cols_to_sum + ['OPP']  # Include 'OPP' column

    positions = df['POS'].unique()
    #position dropdown
    dropdown_position = dcc.Dropdown(
        id='position-dropdown',
        options=[{'label': position, 'value': position} for position in positions],
        value=positions[0]  # Default value
    )
    #column checklist
    checklist_columns = dcc.Checklist(
        id='column-checklist',
        options=[{'label': col, 'value': col} for col in all_columns if col != 'OPP'],  # Exclude 'OPP'
        value=cols_to_sum  # Default value, initially show all cols_to_sum
    )
    #sort by dropdown
    sorting_dropdown = dcc.Dropdown(
        id='sorting-dropdown',
        options=[{'label': col, 'value': col} for col in cols_to_sum],
        value=cols_to_sum[0]  # Default value
    )

    # create dash app and layout
    external_css = ['assets/styles.css']  # Adjust the path according to your directory structure

    app = Dash(__name__, external_stylesheets=external_css)

    app.layout = html.Div(className='master-div', children=[
        html.H1('YRDS/TDs/ETC. allowed by Team filtered by Position'),
        html.Hr(),
        dropdown_position,
        checklist_columns,
        sorting_dropdown,
        dash_table.DataTable(id='datatable', page_size=32),
        
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
        [Input('position-dropdown', 'value'),
         Input('sorting-dropdown', 'value')]
    )
    def update_table(selected_position, selected_sorting_column):
        filtered_df = df[df['POS'] == selected_position]
        result = filtered_df.groupby('OPP')[cols_to_sum].sum().reset_index()
        result = result.sort_values(by=selected_sorting_column, ascending=False)  # Sort by the selected column
        return result.to_dict('records')

    app.run_server(debug=True)

if __name__ == '__main__':
    main()
