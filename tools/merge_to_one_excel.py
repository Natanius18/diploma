import pandas as pd

df = pd.read_csv('../readyDatasets/preprocessed_dataframe.csv')
rows_count = len(df.index)
print('preprocessed_dataframe', rows_count)


map_uni_code = pd.read_csv('../readyDatasets/map_uni_code_to_smoothed_means.csv', delimiter='$')
rows_count = len(map_uni_code.index)
print('map_uni_code_to_smoothed_means', rows_count)

areas = pd.read_excel('../readyDatasets/areas.xlsx')  # has column uni_code and several more
rows_count = len(areas.index)
print('areas', rows_count)

print('=========================')

# here I want to map uni_code values to smooth_mean using map_uni_code
areas_with_smoothed_means = areas.merge(map_uni_code, on=['uni_code'], how="inner")
areas_with_smoothed_means.drop(columns=['uni_code'], inplace=True)
areas_with_smoothed_means.rename(columns={'smooth_mean': 'uni_code'}, inplace=True)
rows_count = len(areas_with_smoothed_means.index)
print('areas_with_smoothed_means', rows_count)

merged_data = df.merge(areas_with_smoothed_means, on=['uni_code'], how="inner")

merged_data.to_csv(r'../readyDatasets/ds_with_areas.csv', index=False)
rows_count = len(merged_data.index)
print(rows_count)
print("Done")
