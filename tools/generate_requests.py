import pandas as pd

df = pd.read_excel('../readyDatasets/2018-2023.xlsx')

cols = ['spec_num', 'Спеціальність', 'specialization']
df['spec_full'] = df[cols].fillna('').apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

features = [
    'Подано заяв на бюджет',
    'Макс. обсяг держзамовлення',
    'Суперобсяг',
    'uni_code',
    'квота-1',
    'Орган управління',
    'spec_full',
    'УСЬОГО']

df.drop(columns=['spec_num', 'Спеціальність', 'specialization', 'Назва закладу', 'Фіксований обсяг',
                 'на загальних підставах', 'Усього рекомендовано'], inplace=True)

df.dropna(inplace=True)
data = df[features]

print(data)
url = 'http://127.0.0.1:5000/data?uni_code={}&spec_full={}&podano_zayav={}&max_val={}&super_val={}&kvota={}&total={}\n'
output_file = "output.txt"

# Open the file in write mode
with open(output_file, "w", encoding="utf-8") as f:
    # Loop through each row in the DataFrame
    for ind in df.index:
        url_string = url.format(
            df['uni_code'][ind],
            df['spec_full'][ind].strip(),
            df['Подано заяв на бюджет'][ind],
            df['Макс. обсяг держзамовлення'][ind],
            df['Суперобсяг'][ind],
            df['квота-1'][ind],
            df['УСЬОГО'][ind]
        )
        # Write the formatted URL string to the file
        f.write(url_string)
