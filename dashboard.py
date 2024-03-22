import dash
import plotly.graph_objs as go
from dash import dcc, html
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

app = dash.Dash()

app.layout = html.Div([
    html.H1("Передбачення результатів вступної кампанії 2024", style={'text-align': 'center'}),

    html.Div([
        dcc.Dropdown(id='specialities-dropdown',
                     options=[{'label': spec, 'value': spec} for spec in specialities['spec_full']],
                     value=specialities['spec_full'].iloc[91],
                     style={'width': '500px', 'margin': 'auto', 'background-color': 'rgba(46, 229, 157, 0.17)',
                            'border-radius': '3px'},
                     placeholder='Оберіть спеціальність'),
    ], style={'text-align': 'center', 'margin-top': '20px', 'justify-content': 'center'}),

    html.Div([
        dcc.Input(id='podano_zayav', type='number', placeholder='Подано заяв', value=64),
        dcc.Input(id='uni_code', type='number', placeholder='Код ЗВО', value=28),
        dcc.Input(id='max_val', type='number', placeholder='Максимальний обсяг держзамовлення', value=43),
        dcc.Input(id='super_val', type='number', placeholder='Суперобсяг', value=11328),
        dcc.Input(id='kvota', type='number', placeholder='квота-1', value=0),
    ], style={'text-align': 'center', 'margin': '10px'}),

    html.Div([
        html.Button('Спрогнозувати', id='predict-button', className='floating-button')],
        style={'text-align': 'center', 'justify-content': 'center', 'margin-bottom': '10px'}),

    html.Div(id='prediction-output-container',
             style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
             children=[
                 html.Div(id='prediction-output')]),

    html.Table(id='plots-table', style={'display': 'none'}, children=[
        html.Tr([
            html.Td([
                dcc.Graph(id='prediction-plot-total')
            ], style={'width': '45%', 'height': '35%'}),
            html.Td([
                dcc.Graph(id='prediction-plot-podano')
            ], style={'width': '45%', 'height': '35%'})
        ])
    ])
])


@app.callback(
    Output('plots-table', 'style'),
    Output('prediction-output', 'children'),
    Output('prediction-plot-total', 'figure'),
    Output('prediction-plot-podano', 'figure'),
    Input('predict-button', 'n_clicks'),
    State('specialities-dropdown', 'value'),
    State('uni_code', 'value'),
    State('podano_zayav', 'value'),
    State('max_val', 'value'),
    State('super_val', 'value'),
    State('kvota', 'value'))
def update_prediction(n_clicks, spec, uni_code, podano_zayav, max_val, super_val, kvota):
    if n_clicks is None:
        return {'display': 'none'}, '', {}, {}

    spec_full = map_spec_full[map_spec_full['spec_full'] == spec].iloc[0, 1]
    uni_code = map_uni_code[map_uni_code['uni_code'] == uni_code].iloc[0, 1]
    authority = map_uni_to_authority[map_uni_to_authority['uni_code'] == uni_code].iloc[0, 1]
    filtered_df = df[(df['spec_full'] == spec_full) & (df['uni_code'] == uni_code)]

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

    year_values = [year_to_smooth_mean[smooth_mean] for smooth_mean in filtered_df['Рік']]
    year_values.append('2024')

    total_values = filtered_df['УСЬОГО'].tolist()
    total_values.append(prediction)

    podano_values = filtered_df['Подано заяв на бюджет'].tolist()
    podano_values.append(podano_zayav)

    data = {
        'Prediction': prediction,
        'Рік': year_values,
        'УСЬОГО': total_values,
        'Подано заяв на бюджет': podano_values
    }

    plot_data_total = go.Scatter(x=data['Рік'], y=data['УСЬОГО'], mode='lines+markers', name='УСЬОГО')
    last_data_point = (data['Рік'][-1], data['УСЬОГО'][-1])
    annotation = go.layout.Annotation(
        x=last_data_point[0],
        y=int(last_data_point[1]) - 1,
        text='Прогноз',
        showarrow=False
    )
    layout_total = go.Layout(title='УСЬОГО по рокам',
                             title_x=0.5,
                             xaxis=dict(title='Рік'),
                             yaxis=dict(title='УСЬОГО'),
                             annotations=[annotation])
    fig_total = go.Figure(data=[plot_data_total], layout=layout_total)

    plot_data_podano = go.Scatter(x=data['Рік'], y=data['Подано заяв на бюджет'],
                                  mode='lines+markers', name='Подано заяв на бюджет')
    layout_podano = go.Layout(title='Подано заяв на бюджет по рокам', title_x=0.5, xaxis=dict(title='Рік'),
                              yaxis=dict(title='Подано заяв на бюджет'))
    fig_podano = go.Figure(data=[plot_data_podano], layout=layout_podano)

    return {'display': 'inline-block'}, prediction, fig_total, fig_podano


if __name__ == '__main__':
    app.run_server()
