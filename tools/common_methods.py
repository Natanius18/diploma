import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def get_train_test_data():
    clear_df = pd.read_csv('../readyDatasets/preprocessed_dataframe.csv')
    x = clear_df.drop(columns='УСЬОГО')
    y = clear_df['УСЬОГО']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=13)
    return x_train, x_test, y_train, y_test


def print_results(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("MSE:", mse, "\tR2 score:", r2)
