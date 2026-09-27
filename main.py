from config import ROW_AMOUNT

from data_holder import DataHolder
from generator import RowGenerator
from openpyxl import Workbook

dh = DataHolder()
gen = RowGenerator(dh)

wb = Workbook()
sheet = wb.active

for _ in range(ROW_AMOUNT):
    rw = gen.generate_row()
    sheet.append(rw.get_row_as_tuple())

print("Successfully generated the dataset")
wb.save("synth_data.xlsx")
