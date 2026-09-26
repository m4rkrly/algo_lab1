from generator import RowGenerator
from openpyxl import Workbook

row_amount = 10
gen = RowGenerator()
wb = Workbook()
sheet = wb.active

for _ in range(10):
    rw = gen.generate_row()
    sheet.append(rw.get_row_as_tuple())

print("Successfully generated the dataset")
wb.save("synth_data.xlsx")
