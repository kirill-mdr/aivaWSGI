"""
api.py
- provides the API endpoints for consuming and producing 
  REST requests and responses
"""

from flask import Flask, Blueprint, jsonify, request
from tensorflow import keras
from os import path
import pandas

api = Blueprint('api', __name__)
model = keras.models.load_model(path.dirname(path.abspath(__file__)) + '/Model')


@api.route('/options', methods=['GET'])
def get_options():
    data = [
        {
            'title': 'Специальность',
            'type': 'spec',
            'data': [
                'Data Analyst',
                'Data Engineer',
                'Data Scientist',
                'Machine Learning Engineer',
                'Все',
            ],
        },
        {
            'title': 'Уровень',
            'type': 'lvl',
            'data': [
                'Junior',
                'Middle',
                'Senior',
                'Director',
                'Все',
            ]
        },
        {
            'title': 'Страна',
            'type': 'country',
            'data': [
                'Канада',
                'Индия',
                'Великобритания',
                'США',
                'Все',
            ]

        },
        {
            'title': 'Формат работы',
            'type': 'remote',
            'data': [
                'Офис',
                'Гибрид',
                'Удаленка',
                'Все',
            ]

        },
        {
            'title': 'Год',
            'type': 'year',
            'data': [
                '2020',
                '2021',
                '2022',
                'Все',
            ]

        },
        {
            'title': 'Размер компании',
            'type': 'size',
            'data': [
                'Большая',
                'Средняя',
                'Маленькая',
                'Все',
            ]

        },
    ]
    return jsonify(data)


@api.route('/predict', methods=['POST'])
def predict():
    request_data = request.get_json()

    job_Data_Analyst, job_Data_Engineer, job_Data_Scientist, job_Machine_Learning_Engineer = 1, 1, 1, 1  # Job title
    Experience_level_EN, Experience_level_EX, Experience_level_MI, Experience_level_SE = 1, 1, 1, 1  # Exp level
    Employee_residence_Canada, Employee_residence_India, Employee_residence_UK, Employee_residence_USA = 1, 1, 1, 1  # Residence
    Remote_ratio_0, Remote_ratio_50, Remote_ratio_100 = 1, 1, 1  # Remote ratio
    Year_2020, Year_2021, Year_2022 = 1, 1, 1  # Year
    Company_size_L, Company_size_M, Company_size_S = 1, 1, 1  # Company Size

    if request_data['spec']:
        job_Data_Analyst, job_Data_Engineer, job_Data_Scientist, job_Machine_Learning_Engineer = request_data['spec'][
                                                                                                     0], \
                                                                                                 request_data['spec'][
                                                                                                     1], \
                                                                                                 request_data['spec'][
                                                                                                     2], \
                                                                                                 request_data['spec'][3]
    if request_data['lvl']:
        Experience_level_EN, Experience_level_EX, Experience_level_MI, Experience_level_SE = request_data['lvl'][0], \
                                                                                             request_data['lvl'][1], \
                                                                                             request_data['lvl'][2], \
                                                                                             request_data['lvl'][3]
    if request_data['country']:
        Employee_residence_Canada, Employee_residence_India, Employee_residence_UK, Employee_residence_USA = \
            request_data['country'][0], request_data['country'][1], request_data['country'][2], request_data['country'][
                3]
    if request_data['remote']:
        Remote_ratio_0, Remote_ratio_50, Remote_ratio_100 = request_data['remote'][0], request_data['remote'][1], \
                                                            request_data['remote'][2]
    if request_data['year']:
        Year_2020, Year_2021, Year_2022 = request_data['year'][0], request_data['year'][1], request_data['year'][2]
    if request_data['size']:
        Company_size_L, Company_size_M, Company_size_S = request_data['size'][0], request_data['size'][1], \
                                                         request_data['size'][2]

    to_predict = [[job_Data_Analyst, job_Data_Engineer, job_Data_Scientist, job_Machine_Learning_Engineer,
                   Experience_level_EN, Experience_level_EX, Experience_level_MI, Experience_level_SE,
                   Employee_residence_Canada, Employee_residence_India, Employee_residence_UK, Employee_residence_USA,
                   Remote_ratio_0, Remote_ratio_50, Remote_ratio_100,
                   Year_2020, Year_2021, Year_2022,
                   Company_size_L, Company_size_M, Company_size_S]]

    prediction = model.predict(to_predict)
    return jsonify({'result': str(prediction[0][0] * 1000)})


@api.route('/graph', methods=['GET'])
def get_graph_values():
    df = pandas.read_csv(path.dirname(path.abspath(__file__)) + '/dataset_sort.csv')

    def plot_vals(DF, job):
        DF = DF[(DF.job_title == job)]
        salary_mean = []
        for i in range(2020, 2020 + int(DF['work_year'].value_counts().count())):
            salary_mean.append(DF.loc[DF['work_year'] == i, 'salary_in_usd'].mean())
        return (DF['work_year'].unique().tolist(), salary_mean)

    params = ['Data Analyst', 'Data Engineer', 'Data Scientist', 'Machine Learning Engineer']
    if request.args.get('spec') in params:
        j = request.args.get('spec')
    else:
        return jsonify({'result': False, 'params': params})

    return jsonify({'result': plot_vals(df, j)})
