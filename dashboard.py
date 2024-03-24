import dash
import plotly.graph_objs as go
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

specialities = pd.read_csv('readyDatasets/map_spec_full_to_smoothed_means.csv', delimiter='$')
universities = pd.read_csv('readyDatasets/universities.csv', delimiter='$')
universities_list = universities['uni_name'].tolist()
df = pd.read_csv('readyDatasets/preprocessed_dataframe.csv')
map_spec_full = pd.read_csv('readyDatasets/map_spec_full_to_smoothed_means.csv', delimiter='$')
map_uni_code = pd.read_csv('readyDatasets/map_uni_code_to_smoothed_means.csv', delimiter='$')
map_uni_to_authority = pd.read_csv('readyDatasets/uni_to_Орган_управління.csv')
map_year = pd.read_csv('readyDatasets/map_Рік_to_smoothed_means.csv', sep='$')
year_to_smooth_mean = dict(zip(map_year['smooth_mean'], map_year['Рік']))
loaded_model = joblib.load('saved_models/xgb_regressor_only_known_features.sav')

best_features = [
    'Подано заяв на бюджет',
    'Макс. обсяг держзамовлення',
    'Суперобсяг',
    'uni_code',
    'квота-1',
    'Орган управління',
    'spec_full']

x = df.drop(columns='УСЬОГО')
y = df['УСЬОГО']
sc = StandardScaler()
sc.fit_transform(x[best_features])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


def input_fields_section():
    style = {'display': 'inline-block', 'margin': '10px', 'width': '150px', 'vertical-align': 'middle'}
    return html.Div(
        [
            dbc.FormFloating(
                [
                    dbc.Input(id='podano_zayav', type='number', placeholder=''),
                    dbc.Label("Подано заяв")
                ],
                style=style
            ),
            dbc.FormFloating(
                [
                    dbc.Input(id='max_val', type='number', placeholder=''),
                    dbc.Label("Макс. обсяг держзамовлення")
                ],
                style={'display': 'inline-block', 'margin': '8px', 'width': '250px', 'vertical-align': 'middle'}
            ),
            dbc.FormFloating(
                [
                    dbc.Input(id='super_val', type='number', placeholder=''),
                    dbc.Label("Суперобсяг")
                ],
                style=style
            ),
            dbc.FormFloating(
                [
                    dbc.Input(id='kvota', type='number', placeholder=''),
                    dbc.Label("Квота-1")
                ],
                style=style
            )
        ],
        style={'text-align': 'center', 'margin': '10px', 'justify-content': 'center'},
    )


def button_section():
    return html.Div([
        html.Button('Спрогнозувати', id='predict-button', className='floating-button')],
        style={'text-align': 'center', 'justify-content': 'center', 'margin-bottom': '10px'})


def prediction_output_section():
    return html.Div(
        id='prediction-output-container',
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
        children=[
            html.Div("✨", id='prediction-output')
        ]
    )


def plots_table_section():
    return html.Table(
        id='plots-table',
        children=[
            html.Tr([
                html.Td([
                    dcc.Graph(id='prediction-plot-total')
                ], style={'width': '720px', 'height': '300px'}),
                html.Td([
                    dcc.Graph(id='prediction-plot-podano')
                ], style={'width': '720px', 'height': '300px'})
            ]),
            html.Tr([
                html.Td([
                    dcc.Graph(id='prediction-plot-derzhzamovlennya')
                ], style={'width': '720px', 'height': '300px'}),
                html.Td([
                    dcc.Graph(id='prediction-plot-superobshag')
                ], style={'width': '720px', 'height': '300px'})
            ])
        ]
    )


def drop_downs(dropdown_spec_id, dropdown_uni_id,
               uni_value=universities_list[47],
               spec_value=specialities['spec_full'].iloc[91]):
    return html.Div([
        html.Div([
            dcc.Dropdown(id=dropdown_uni_id,
                         options=[{'label': uni, 'value': uni} for uni in universities_list],
                         value=uni_value,
                         style={'width': '700px', 'margin': '0px 10px', 'border-radius': '5px'},
                         placeholder='Оберіть заклад вищої освіти'),
            dcc.Dropdown(id=dropdown_spec_id,
                         options=[{'label': spec, 'value': spec} for spec in specialities['spec_full']],
                         value=spec_value,
                         style={'width': '300px', 'margin': '0px 10px', 'border-radius': '5px'},
                         placeholder='Оберіть спеціальність')
        ], style={'display': 'flex', 'justify-content': 'center'})
    ], style={'text-align': 'center', 'margin-top': '20px'})


app.layout = html.Div([
    html.H1("Передбачення результатів вступної кампанії 2024", style={'text-align': 'center', 'margin': '20px'}),
    html.Div("Введіть необхідні дані та натисніть кнопку нижче, щоб отримати прогноз результатів вступної кампанії:",
             style={'text-align': 'center', 'margin': '10px'}),
    input_fields_section(),
    drop_downs('specialities-dropdown', 'universities-dropdown', None, None),
    button_section(),
    prediction_output_section(),
    html.Div(
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
        children=[
            html.Div(id='prediction-output-2', hidden=True)
        ]
    ),
    html.Div([dbc.Button("Подивитися статистику за минулі роки",
                         id="open-button",
                         n_clicks=0,
                         style={'text-align': 'center', 'margin': '20px'})],
             style={'text-align': 'center', 'justify-content': 'center', 'margin-bottom': '10px'}),
    dbc.Collapse(
        [
            html.Div("Оберіть назву закладу та спеціальність, для яких бажаєте отримати статистику:",
                     style={'text-align': 'center', 'padding-top': '20px'}),
            drop_downs('specialities-dropdown-2', 'universities-dropdown-2'),
            plots_table_section()
        ],
        id="collapse",
        is_open=False)
])


@app.callback(
    Output('prediction-output', 'children'),
    Output('prediction-output-2', 'hidden'),
    Output('prediction-output-2', 'children'),
    Input('predict-button', 'n_clicks'),
    State('specialities-dropdown', 'value'),
    State('universities-dropdown', 'value'),
    State('podano_zayav', 'value'),
    State('max_val', 'value'),
    State('super_val', 'value'),
    State('kvota', 'value')
)
def update_prediction(n_clicks, spec, uni_code, podano_zayav, max_val, super_val, kvota):
    if n_clicks is None:
        return '✨', True, ''

    spec_full = map_spec_full[map_spec_full['spec_full'] == spec].iloc[0, 1]

    uni_code = int(uni_code.split(' ')[0])
    uni_code = map_uni_code[map_uni_code['uni_code'] == uni_code].iloc[0, 1]

    authority = map_uni_to_authority[map_uni_to_authority['uni_code'] == uni_code].iloc[0, 1]

    features = {
        'Подано заяв на бюджет': [int(podano_zayav)],
        'Макс. обсяг держзамовлення': [int(max_val)],
        'Суперобсяг': [int(super_val)],
        'uni_code': [int(uni_code)],
        'квота-1': [int(kvota)],
        'Орган управління': [authority],
        'spec_full': [spec_full]
    }

    input_info = pd.DataFrame(data=features)
    test_data = sc.transform(input_info)

    res = int(loaded_model.predict(test_data)[0])
    prediction = str(res)

    if prediction.endswith('11'):
        message = f"З урахуванням наданих даних, модель передбачає, що з високою ймовірністю буде виділено {prediction} бюджетних місць"
    elif prediction.endswith('1'):
        message = f"З урахуванням наданих даних, модель передбачає, що з високою ймовірністю буде виділено {prediction} бюджетне місце"
    elif prediction.endswith(('2', '3', '4')):
        message = f"З урахуванням наданих даних, модель передбачає, що з високою ймовірністю буде виділено {prediction} бюджетні місця"
    else:
        message = f"З урахуванням наданих даних, модель передбачає, що з високою ймовірністю буде виділено {prediction} бюджетних місць"

    return prediction, False, message


def create_plot(x_values, y_values, title, x_title, y_title):
    plot_data = go.Scatter(x=x_values, y=y_values, mode='lines+markers', name=y_title)
    layout = go.Layout(title=title, title_x=0.5, title_y=0.85, xaxis=dict(title=x_title), yaxis=dict(title=y_title), paper_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=[plot_data], layout=layout)
    return fig


@app.callback(
    Output('prediction-plot-total', 'figure'),
    Output('prediction-plot-podano', 'figure'),
    Output('prediction-plot-derzhzamovlennya', 'figure'),
    Output('prediction-plot-superobshag', 'figure'),
    Input('specialities-dropdown-2', 'value'),
    Input('universities-dropdown-2', 'value')
)
def generate_plots(speciality, university):
    spec_full = map_spec_full[map_spec_full['spec_full'] == speciality].iloc[0, 1]
    uni_code = int(university.split(' ')[0])
    uni_code = map_uni_code[map_uni_code['uni_code'] == uni_code].iloc[0, 1]
    filtered_df = df[(df['spec_full'] == spec_full) & (df['uni_code'] == uni_code)]

    year_values = [year_to_smooth_mean[smooth_mean] for smooth_mean in filtered_df['Рік']]

    total_values = filtered_df['УСЬОГО'].tolist()
    podano_values = filtered_df['Подано заяв на бюджет'].tolist()
    derzhzamovlennya_values = filtered_df['Макс. обсяг держзамовлення'].tolist()
    superobshag_values = filtered_df['Суперобсяг'].tolist()

    fig_total = create_plot(year_values, total_values, 'Підсумкова кількість бюджетних місць по рокам', 'Рік', 'УСЬОГО')
    fig_podano = create_plot(year_values, podano_values, 'Подано заяв на бюджет по рокам', 'Рік',
                             'Подано заяв на бюджет')
    fig_derzhzamovlennya = create_plot(year_values, derzhzamovlennya_values, 'Макс. обсяг держзамовлення по рокам',
                                       'Рік', 'Макс. обсяг держзамовлення')
    fig_superobshag = create_plot(year_values, superobshag_values, 'Суперобсяг по рокам', 'Рік', 'Суперобсяг')

    return fig_total, fig_podano, fig_derzhzamovlennya, fig_superobshag


@app.callback(
    Output("collapse", "is_open", allow_duplicate=True),
    Output("open-button", "children"),
    Input("open-button", "n_clicks"),
    State("collapse", "is_open"),
    prevent_initial_call=True
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        is_open = not is_open
    if n_clicks % 2 == 1:
        message = "Приховати статистику"
    else:
        message = "Подивитися статистику за минулі роки"
    return is_open, message


if __name__ == '__main__':
    app.run_server()
