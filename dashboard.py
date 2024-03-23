import dash
import plotly.graph_objs as go
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

specialities = pd.read_csv('readyDatasets/map_spec_full_to_smoothed_means.csv', delimiter='$')
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


def dropdown_section():
    return html.Div([
        dcc.Dropdown(
            id='specialities-dropdown',
            options=[{'label': spec, 'value': spec} for spec in specialities['spec_full']],
            value=specialities['spec_full'].iloc[91],
            style={'width': '500px', 'margin': 'auto', 'border-radius': '5px'},
            placeholder='Оберіть спеціальність'),
    ], style={'text-align': 'center', 'margin-top': '20px', 'justify-content': 'center'})


def input_fields_section():
    style = {'display': 'inline-block', 'margin': '10px', 'width': '150px', 'vertical-align': 'middle'}
    return html.Div(
        [
            dbc.FormFloating(
                [
                    dbc.Input(id='podano_zayav', type='number', value=64, placeholder=''),
                    dbc.Label("Подано заяв")
                ],
                style=style
            ),
            dbc.FormFloating(
                [
                    dbc.Input(id='uni_code', type='number', value=28, placeholder=''),
                    dbc.Label("Код ЗВО")
                ],
                style=style
            ),
            dbc.FormFloating(
                [
                    dbc.Input(id='max_val', type='number', value=43, placeholder=''),
                    dbc.Label("Макс. обсяг держзамовлення")
                ],
                style={'display': 'inline-block', 'margin': '8px', 'width': '250px', 'vertical-align': 'middle'}
            ),
            dbc.FormFloating(
                [
                    dbc.Input(id='super_val', type='number', value=11328, placeholder=''),
                    dbc.Label("Суперобсяг")
                ],
                style=style
            ),
            dbc.FormFloating(
                [
                    dbc.Input(id='kvota', type='number', value=0, placeholder=''),
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
            html.Div(id='prediction-output')
        ]
    )


def plots_table_section():
    return html.Table(
        id='plots-table',
        style={'display': 'inline-block'},
        children=[
            html.Tr([
                html.Td([
                    dcc.Graph(id='prediction-plot-total')
                ], style={'width': '45%', 'height': '35%'}),
                html.Td([
                    dcc.Graph(id='prediction-plot-podano')
                ], style={'width': '45%', 'height': '35%'})
            ])
        ]
    )


def input_for_plots():
    return html.Div(style={'display': 'inline-block'}, children=[
        dcc.Dropdown(
            id='specialities-dropdown-2',
            options=[{'label': spec, 'value': spec} for spec in specialities['spec_full']],
            value=specialities['spec_full'].iloc[91],
            style={'width': '500px', 'margin': 'auto', 'border-radius': '5px'},
            placeholder='Оберіть спеціальність'
        ),
        dcc.Input(
            id='uni_code-2',
            type='number',
            value=28,
            style={'width': '500px', 'margin': 'auto', 'border-radius': '5px'},
            placeholder='Код ЗВО'
        ),
    ])


app.layout = html.Div([
    html.H1("Передбачення результатів вступної кампанії 2024", style={'text-align': 'center', 'margin': '20px'}),
    html.Div("Введіть необхідні дані та натисніть кнопку нижче, щоб отримати прогноз результатів вступної кампанії:",
             style={'text-align': 'center', 'margin': '10px'}),
    input_fields_section(),
    dropdown_section(),
    button_section(),
    prediction_output_section(),
    input_for_plots(),
    plots_table_section()
])


@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-button', 'n_clicks'),
    State('specialities-dropdown', 'value'),
    State('uni_code', 'value'),
    State('podano_zayav', 'value'),
    State('max_val', 'value'),
    State('super_val', 'value'),
    State('kvota', 'value'))
def update_prediction(n_clicks, spec, uni_code, podano_zayav, max_val, super_val, kvota):
    if n_clicks is None:
        return ''

    spec_full = map_spec_full[map_spec_full['spec_full'] == spec].iloc[0, 1]
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

    res = loaded_model.predict(test_data)[0]
    prediction = str(int(res))

    return prediction


@app.callback(
    Output('prediction-plot-total', 'figure'),
    Output('prediction-plot-podano', 'figure'),
    Input('specialities-dropdown-2', 'value'),
    State('uni_code-2', 'value')
)
def generate_plots(speciality, uni_code):
    filtered_df = df[(df['spec_full'] == speciality) & (df['uni_code'] == uni_code)]

    year_values = [year_to_smooth_mean[smooth_mean] for smooth_mean in filtered_df['Рік']]

    total_values = filtered_df['УСЬОГО'].tolist()
    podano_values = filtered_df['Подано заяв на бюджет'].tolist()

    plot_data_total = go.Scatter(x=year_values, y=total_values, mode='lines+markers', name='УСЬОГО')

    layout_total = go.Layout(title='УСЬОГО по рокам',
                             title_x=0.5,
                             xaxis=dict(title='Рік'),
                             yaxis=dict(title='УСЬОГО'))
    fig_total = go.Figure(data=[plot_data_total], layout=layout_total)

    plot_data_podano = go.Scatter(x=year_values, y=podano_values,
                                  mode='lines+markers', name='Подано заяв на бюджет')
    layout_podano = go.Layout(title='Подано заяв на бюджет по рокам', title_x=0.5, xaxis=dict(title='Рік'),
                              yaxis=dict(title='Подано заяв на бюджет'))
    fig_podano = go.Figure(data=[plot_data_podano], layout=layout_podano)

    return fig_total, fig_podano


if __name__ == '__main__':
    app.run_server(debug=True)
