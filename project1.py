import os
import pandas as pd


class PriceMachine():



    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
    
    def load_prices(self, file_path=''):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

        HEADERS = ['№', 'Наименование', 'цена', 'вес', 'файл', 'цена за кг.']
        df = pd.DataFrame(columns=HEADERS)
        df_end = pd.DataFrame(columns=HEADERS)
        keyword = 'price'
        if file_path=='': file_path=None
        for fname in os.listdir(file_path):
            if keyword in fname:

                df_f = pd.read_csv(fname, delimiter=';',  encoding='utf-8')

                headers = list(df_f.columns)
                ind_name, ind_price, ind_weight = self._search_product_price_weight(headers)

                df[HEADERS[1]]=df_f[headers[ind_name]]
                df[HEADERS[3]] = df_f[headers[ind_weight]]
                df[HEADERS[5]] = df_f[headers[ind_price]]
                df[HEADERS[4]] = fname
                df[HEADERS[2]] = df[HEADERS[3]]*df[HEADERS[5]]
                df[HEADERS[5]] = df[HEADERS[5]].astype(float)

                if len(df_end)==0: df_end=df
                else:
                    df_end=pd.concat([df_end, df])

        df_end=df_end.sort_values (by='цена за кг.', ascending= True)
        df_end[HEADERS[0]] = range(1, len(df_end) + 1)
        df_end=df_end.dropna()
        df_end = df_end.reset_index(drop=True)

        self.data=df_end
        return df_end

    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        cols_name = ['товар', 'название', 'наименование', 'продукт']
        cols_price = ['розница', 'цена']
        cols_weight = ['вес', 'масса', 'фасовка']

        for header in headers:
            if header in cols_name: ind_name = headers.index(header)
            if header in cols_price: ind_price = headers.index(header)
            if header in cols_weight: ind_weight = headers.index(header)
        return (ind_name, ind_price, ind_weight)

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        df = self.data
        for i in range(len(df)):
            result += '<tr>'
            result += f'<td>{df["№"].values[i]}</td>'
            result += f'<td>{df["Наименование"].values[i]}</td>'
            result += f'<td>{df["цена"].values[i]}</td>'
            result += f'<td>{df["вес"].values[i]}</td>'
            result += f'<td>{df["файл"].values[i]}</td>'
            result += f'<td>{df["цена за кг."].values[i]}</td>'
            result += '</tr>'
        result += '</table>'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)


    def find_text(self, text):
        df = self.data
        matches = df[df['Наименование'].str.contains(text, case=False)]
        len_df=len(matches)
        if len_df > 0:

            return matches
        else:
            return f'Продукта с наименованием: {text}, не найдено.'

    
pm = PriceMachine()
print(pm.load_prices())

'''
    Логика работы программы
'''
while True:
    text = input('Введите наименование продукта: ')
    if text == "exit":
        print('Работа закончена.')
        break
    else:
        result_search = pm.find_text(text)
        print(result_search)

print('the end')
print(pm.export_to_html())
