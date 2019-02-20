import os
import statistics as stat
from datetime import datetime

import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import HoverTool, Range1d
from bokeh.plotting import ColumnDataSource, figure
from bokeh.resources import CDN
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import MDS
from sqlalchemy import create_engine

from django.http import JsonResponse
from django.shortcuts import redirect, render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
engine = create_engine(
    'sqlite:////' + os.path.join(BASE_DIR, "fund.db"))
mds_picture = []


def home(request):
    if request.method == "POST":
        year = request.POST['year']
        return redirect('/test/' + year + '/')
    return render(request, "home.html", locals())


def test(request, year):
    script_profit, div_profit, script_mds, div_mds = winrate(year)
    return render(request, "test.html", locals())


def mds(request, month):
    month = int(month) - 1
    return JsonResponse(mds_picture[month])


def get_timestamp(date):
    return int(pd.read_sql(sql='select strftime("%s", ?, "localtime")', con=engine, params=[date]).loc[0][0])


def get_nav(names, start, end):
    date = pd.read_sql(sql='select distinct date from price where date between ? and ? order by date asc',
                       con=engine, index_col='date', params=[start, end]).index
    nav = np.zeros((len(names), len(date)))
    for j in range(len(names)):
        temp = pd.read_sql(sql='select * from price where fund_id = ? and date between ? and ? order by date asc',
                           con=engine, index_col='date', params=[names[j], start, end])
        nav[j][0] = temp.iloc[0]['nav']
        for i, day in enumerate(date[1:]):
            try:
                nav[j][i + 1] = temp.loc[day]['nav']
            except:
                nav[j][i + 1] = nav[j][i]
    return nav


def get_colors(names, name_choose):
    temp = pd.DataFrame(names, columns=['id'])
    color_choose = []
    for i in range(4):
        color_choose.append(temp[temp['id'] == name_choose[i]].index[0])
    color = []
    for i in range(len(names)):
        if i in color_choose:
            color.append('red')
        else:
            color.append('purple')
    return color


def get_mds(names, name_choose, year):
    TOOLTIPS = [
        ("fund_id", "@name"),
    ]

    for k in range(11):
        if k < 9:
            start = get_timestamp(year + '-0' + str(k + 1) + '-01')
            end = get_timestamp(year + '-0' + str(k + 1) + '-31')
        else:
            start = get_timestamp(year + '-' + str(k + 1) + '-01')
            end = get_timestamp(year + '-' + str(k + 1) + '-31')
        nav = get_nav(names, start, end)

        length = len(nav[0]) - 1
        rate = np.zeros((len(names), length))
        for j in range(len(names)):
            for i in range(length):
                rate[j][i] = (nav[j][i + 1] - nav[j][i]) / nav[j][i]
        temp = []
        for i, j in enumerate(rate):
            if np.cov(j) == 0:
                temp.append(i)
        rate = np.delete(rate, temp, 0)
        temp_names = np.delete(names, temp, 0)

        similarity = np.zeros((len(rate), len(rate)))
        for i in range(len(rate)):
            for j in range(len(rate)):
                corr = np.corrcoef(rate[i], rate[j])[0][-1]
                similarity[i][j] = 1 - (corr * 0.5 + 0.5)
        for i in range(len(rate)):
            similarity[i][i] = 0
        mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1).fit(
            similarity).embedding_
        source = ColumnDataSource(data=dict(
            x=mds[:, 0],
            y=mds[:, 1],
            name=temp_names,
            color=get_colors(temp_names, name_choose),
        ))
        p = figure(plot_width=700, plot_height=700, tooltips=TOOLTIPS,
                   title="MDS", toolbar_location=None, tools="")
        p.x_range = Range1d(-0.6, 0.6)
        p.y_range = Range1d(-0.6, 0.6)
        p.circle(x='x', y='y', color='color', size=6.5, source=source)
        script_mds, div_mds = components(p, CDN)
        mds_dict = {'script': script_mds, 'div': div_mds}
        mds_picture.append(mds_dict)


def get_profit_picture(start, end, profit_choose):
    date = pd.read_sql(sql='select distinct datetime(date, "unixepoch") from price where date between ? and ? order by date asc',
                       con=engine, params=[start, end])
    date['profit'] = profit_choose
    date.rename(columns={'datetime(date, "unixepoch")': 'date'}, inplace=True)
    for i, j in enumerate(date['date']):
        date.loc[i, 'date'] = datetime.strptime(j, '%Y-%m-%d %H:%M:%S')
    date.index = date.date
    date = date.drop('date', axis=1)
    p = figure(x_axis_type="datetime", plot_width=1500,
               plot_height=500, title="Profit", toolbar_location=None, tools="")
    p.line(x='date', y='profit', line_width=3, source=date)
    p.add_tools(HoverTool(tooltips=[("date", "@date{%F}"), ("profit", "@profit")], formatters={
                'date': 'datetime', }, mode='vline'))
    script_profit, div_profit = components(p, CDN)
    return script_profit, div_profit


def winrate(year):
    past_year = str(int(year) - 1)
    start = get_timestamp(past_year + '-12-01')
    end = get_timestamp(past_year + '-12-31')

    names = pd.read_sql(sql='select distinct fund_id from price where date between ? and ?',
                            con=engine, params=[start, end])
    names = names['fund_id'].sample(n=300).values

    nav = get_nav(names, start, end)

    length = len(nav[0]) - 1
    rate = np.zeros((len(names), length))
    for j in range(len(names)):
        for i in range(length):
            rate[j][i] = (nav[j][i + 1] - nav[j][i]) / nav[j][i]
    temp = []
    for i, j in enumerate(rate):
        if np.cov(j) == 0:
            temp.append(i)
    rate = np.delete(rate, temp, 0)
    names = np.delete(names, temp, 0)
    nav = np.delete(nav, temp, 0)

    similarity = np.zeros((len(rate), len(rate)))
    for i in range(len(rate)):
        for j in range(len(rate)):
            corr = np.corrcoef(rate[i], rate[j])[0][-1]
            similarity[i][j] = 1 - (corr * 0.5 + 0.5)
    for i in range(len(rate)):
        similarity[i][i] = 0

    clustering = AgglomerativeClustering(n_clusters=4).fit(similarity)
    camp = pd.DataFrame(data=clustering.labels_,
                        index=names, columns=['label'])
    name_choose = []
    start = get_timestamp(year + '-01-01')
    end = get_timestamp(year + '-12-31')
    for i in range(4):
        name_choose.append(camp[camp['label'] == i].sample(n=1).index[0])

    nav_choose = get_nav(name_choose, start, end)
    interest_choose = 0
    for name in name_choose:
        interest_choose += (pd.read_sql(sql='select interest from interest where date between ? and ? and fund_id = ?',
                                        con=engine, params=[start, end, name])['interest'].sum())

    temp = np.zeros((len(name_choose), len(nav_choose[0]) - 1))
    for j in range(len(name_choose)):
        for i in range(len(nav_choose[0]) - 1):
            temp[j][i] = (nav_choose[j][i + 1] - nav_choose[j]
                          [i]) / nav_choose[j][i]

    rate_choose = []
    for i in range(len(temp[0])):
        rate_choose.append(
            (temp[0][i] + temp[1][i] + temp[2][i] + temp[3][i]) / 4)

    profit_choose = []
    temp = nav_choose[0][0] + nav_choose[1][0] + \
        nav_choose[2][0] + nav_choose[3][0]
    for i in range(len(nav_choose[0])):
        profit_choose.append(
            (nav_choose[0][i] + nav_choose[1][i] + nav_choose[2][i] + nav_choose[3][i] - temp) / temp * 100)
    profit_choose[-1] += interest_choose / temp * 100

    script_profit, div_profit = get_profit_picture(start, end, profit_choose)

    TOOLTIPS = [
        ("fund_id", "@name"),
    ]
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1).fit(
        similarity).embedding_
    source = ColumnDataSource(data=dict(
        x=mds[:, 0],
        y=mds[:, 1],
        name=names,
        color=get_colors(names, name_choose),
    ))
    p = figure(plot_width=700, plot_height=700, tooltips=TOOLTIPS,
               title="MDS", toolbar_location=None, tools="")
    p.x_range = Range1d(-0.6, 0.6)
    p.y_range = Range1d(-0.6, 0.6)
    p.circle(x='x', y='y', color='color', size=6.5, source=source)
    script_mds, div_mds = components(p, CDN)
    mds_dict = {'script': script_mds, 'div': div_mds}
    mds_picture.append(mds_dict)
    get_mds(names, name_choose, year)
    return script_profit, div_profit, script_mds, div_mds
