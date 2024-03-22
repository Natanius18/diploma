import json

import joblib
import pandas as pd
from flask import Flask, request
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

specialities = pd.read_csv('readyDatasets/map_spec_full_to_smoothed_means.csv', delimiter='$')
universities = pd.read_csv('readyDatasets/universities.csv', delimiter='$')

df = pd.read_csv('readyDatasets/preprocessed_dataframe.csv')
map_uni_code = pd.read_csv('readyDatasets/map_uni_code_to_smoothed_means.csv', delimiter='$')
map_uni_to_authority = pd.read_csv('readyDatasets/uni_to_Орган_управління.csv')
map_spec_full = pd.read_csv('readyDatasets/map_spec_full_to_smoothed_means.csv', delimiter='$')
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
x_train, _, _, _ = train_test_split(x, y, test_size=0.25, random_state=13)
x_train = x_train[best_features]
sc = StandardScaler()
sc.fit_transform(x_train)


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
    podano_zayav = request.args.get('podano_zayav')
    max_val = request.args.get('max_val')
    super_val = request.args.get('super_val')
    kvota = request.args.get('kvota')
    spec_full = request.args.get('spec_full')
    spec_full = map_spec_full[map_spec_full['spec_full'] == spec_full].iloc[0, 1]

    uni_code = int(request.args.get('uni_code'))
    uni_code = map_uni_code[map_uni_code['uni_code'] == uni_code].iloc[0, 1]
    authority = map_uni_to_authority[map_uni_to_authority['uni_code'] == uni_code].iloc[0, 1]

    filtered_df = df[(df['spec_full'] == spec_full) & (df['uni_code'] == uni_code)]

    year_values = [year_to_smooth_mean[smooth_mean] for smooth_mean in filtered_df['Рік']]

    features = {
        'Подано заяв на бюджет': [podano_zayav],
        'Макс. обсяг держзамовлення': [max_val],
        'Суперобсяг': [super_val],
        'uni_code': [uni_code],
        'квота-1': [kvota],
        'Орган управління': [authority],
        'spec_full': [spec_full]
    }

    input_info = pd.DataFrame(data=features)
    test_data = sc.transform(input_info)

    res = loaded_model.predict(test_data)[0]

    data = {
        'Prediction': str(int(res)),
        'Рік': year_values,
        'УСЬОГО': filtered_df['УСЬОГО'].tolist(),
        'Подано заяв на бюджет': filtered_df['Подано заяв на бюджет'].tolist()
    }

    return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
