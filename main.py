from data_holder import DataHolder
from generator import RowGenerator
from openpyxl import Workbook
from math import isclose

wb = Workbook()
sheet = wb.active
dh = DataHolder()
while True: 
    ROW_AMOUNT = int(input("Пожалуйста, введите количество строк для генерации (не менее 50000): "))
    if ROW_AMOUNT < 50_000:
        print("Пожалуйста, введите не менее чем 50 000 строк")
        continue
    else:
        break
print("\n")

custom_systems_probs = dict()
while True:
    print(
        ("Пожалуйста, выберите вероятности появления платёжных систем\n"
        "Помните, что сумма всех вероятностей должна быть равна единице")
    )
    print(f"Число доступных платёжных систем: {len(dh.SYSTEMS)}")
    for system in dh.SYSTEMS:
        prob = float(input(f"Введите вероятность появления системы {system}: "))
        custom_systems_probs[system] = prob

    if not isclose(sum(custom_systems_probs.values()), 1):
        print("Сумма вероятностей не равна единице! Пожалуйста, попробуйте ещё раз")
        print("\n")
    else:
        break


print("\n")

custom_banks_probs = dict()
while True:
    print(
        ("Пожалуйста, выберите вероятности появления конкретных банков\n"
        "Помните, что сумма всех вероятностей должна быть равна единице")
    )
    print(f"Число доступных банков: {len(dh.BANKS)}")
    for bank in dh.BANKS:
        prob = float(input(f"Введите вероятность появления банка {bank}: "))
        custom_banks_probs[bank] = prob

    if not isclose(sum(custom_banks_probs.values()), 1):
        print("Сумма вероятностей не равна единице! Пожалуйста, попробуйте ещё раз")
        print("\n")
    else:
        break

dh.init_probs(custom_banks_probs, custom_systems_probs)

gen = RowGenerator(dh)

print("Начинаю генерацию...")
sheet.append(dh.HEADER)
for _ in range(ROW_AMOUNT):
    rw = gen.generate_row()
    sheet.append(rw.get_row_as_tuple())

wb.save("synth_data.xlsx")
print("Датасет успешно сгенерирован")
