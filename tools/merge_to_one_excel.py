import pandas as pd

main_table = pd.read_excel('main2023.xlsx')
rows_count = len(main_table.index)
print(rows_count)


additional_data = pd.read_excel('data2023.xlsx')
rows_count = len(additional_data.index)
print(rows_count)


main_table["Назва закладу"] = main_table["Назва закладу"].str.upper()
additional_data["Назва закладу"] = additional_data["Назва закладу"].str.upper()


merged_data = main_table.merge(additional_data, on=["Назва закладу", "spec_num", "specialization", "form"], how="inner")


merged_data.to_excel(r'data2023F.xlsx', index=False)
rows_count = len(merged_data.index)
print(rows_count)
print("Done")

