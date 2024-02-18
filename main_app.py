import json

import pandas as pd
from flask import Flask, request

app = Flask(__name__)

specialities = pd.read_csv('readyDatasets/map_spec_full_to_smoothed_means.csv', delimiter='$')
universities = pd.read_csv('readyDatasets/universities.csv', delimiter='$')

df = pd.read_csv('readyDatasets/preprocessed_dataframe.csv')
map_uni_code = pd.read_csv('readyDatasets/map_uni_code_to_smoothed_means.csv', delimiter='$')
map_spec_full = pd.read_csv('readyDatasets/map_spec_full_to_smoothed_means.csv', delimiter='$')
map_year = pd.read_csv('readyDatasets/map_Рік_to_smoothed_means.csv', sep='$')
year_to_smooth_mean = dict(zip(map_year['smooth_mean'], map_year['Рік']))


@app.route('/specialities', methods=['GET'])
def get_specialities():
    specialities_list = specialities['spec_full'].tolist()
    response = {'specialities': specialities_list}
    return json.dumps(response, ensure_ascii=False)


@app.route('/universities', methods=['GET'])
def get_universities():
    universities_list = universities['uni_name'].tolist()
    response = {'universities': universities_list}
    return json.dumps(response, ensure_ascii=False)


@app.route('/data', methods=['GET'])
def get_data():
    spec_full = request.args.get('spec_full')
    spec_full = map_spec_full[map_spec_full['spec_full'] == spec_full].iloc[0, 1]

    uni_code = int(request.args.get('uni_code'))
    uni_code = map_uni_code[map_uni_code['uni_code'] == uni_code].iloc[0, 1]

    filtered_df = df[(df['spec_full'] == spec_full) & (df['uni_code'] == uni_code)]

    year_values = [year_to_smooth_mean[smooth_mean] for smooth_mean in filtered_df['Рік']]

    data = {
        'Рік': year_values,
        'УСЬОГО': filtered_df['УСЬОГО'].tolist(),
        'Подано заяв на бюджет': filtered_df['Подано заяв на бюджет'].tolist()
    }

    return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
