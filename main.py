from config import ROW_AMOUNT

from data_holder import DataHolder
from generator import RowGenerator
from openpyxl import Workbook

wb = Workbook()
sheet = wb.active
dh = DataHolder()

while True:
    print(
        ("Пожалуйста, выберите вероятности появления платёжных систем\n"
        "Помните, что сумма всех вероятностей должна быть равна единице")
    )
    custom_systems_probs = dict()
    for system in dh.SYSTEMS:
        prob = float(input(f"Введите вероятность появления системы {system}: "))
        custom_systems_probs[system] = prob

    print("\n")
    print(
        ("Пожалуйста, выберите вероятности появления конкретных банков\n"
        "Помните, что сумма всех вероятностей должна быть равна единице")
    )
    custom_banks_probs = dict()
    for bank in dh.BANKS:
        prob = float(input(f"Введите вероятность появления банка {bank}: "))
        custom_banks_probs[bank] = prob
        
    if (sum(custom_systems_probs.values()) == 1) and (sum(custom_banks_probs) == 1):
        dh.init_probs(custom_banks_probs, custom_systems_probs)
        break
    else:
        print("Сумма вероятностей не равна единице! Пожалуйста, попробуйте ещё раз")
        print("\n")

gen = RowGenerator(dh)

for _ in range(ROW_AMOUNT):
    rw = gen.generate_row()
    sheet.append(rw.get_row_as_tuple())

wb.save("synth_data.xlsx")
print("Датасет успешно сгенерирован")
