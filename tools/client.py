import requests
from sklearn.metrics import mean_absolute_error

from tools.common_methods import print_results

real_values = []
predictions = []


def send_get_request(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            real_value = url.split('=')[7]
            prediction = response.text.split(sep=',')[0].split('"')[3]
            real_values.append(int(real_value))
            predictions.append(int(prediction))
            print("Expected:", real_value, "\t Response:", prediction)
        else:
            print("Error: HTTP Status Code", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)


output_file = "output.txt"

with open(output_file, "r", encoding="utf-8") as f:
    for line in f:
        url = line.strip()
        send_get_request(url)

print_results(real_values, predictions)
print('MAE:', mean_absolute_error(real_values, predictions))