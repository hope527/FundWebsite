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
from dateutil.relativedelta import relativedelta

from django.http import JsonResponse
from django.shortcuts import redirect, render

mds_picture = []


def home(request):
    if request.method == "POST":
        start = request.POST['start']
        end = request.POST['end']
        return redirect('/test/' + " ".join([start, end]) + '/')
    return render(request, "home.html", locals())


def test(request, start, end):
    t = Test(start, end)
    script_profit, div_profit = t.get_profit()
    div_mds = t.mds_picture[0]['div']
    script_mds = t.mds_picture[0]['script']
    global mds_picture
    mds_picture = t.mds_picture
    return render(request, "test.html", locals())


def mds(request, start, end):
    return JsonResponse(mds_picture[(int(end[:4]) - int(start[:4])) * 12 + int(end[5:7]) - int(start[5:7])])


class Test:
    engine = create_engine('sqlite:///fund.db')
    mds_picture = []

    def __init__(self, start, end):
        self.start = self.get_timestamp(start)
        self.end = self.get_timestamp(end)
        self.start_str = start
        self.end_str = end

    def get_timestamp(self, date):
        return int(pd.read_sql(sql='select strftime("%s", ?, "localtime")', con=self.engine, params=[date]).loc[0][0])

    def get_nav(self, names, start, end):
        date = pd.read_sql(sql='select distinct date from price where date between ? and ? order by date asc',
                           con=self.engine, index_col='date', params=[start, end]).index
        nav = np.zeros((len(names), len(date)))
        for j in range(len(names)):
            temp = pd.read_sql(sql='select * from price where fund_id = ? and date between ? and ? order by date asc',
                               con=self.engine, index_col='date', params=[names[j], start, end])
            nav[j][0] = temp.iloc[0]['nav']
            for i, day in enumerate(date[1:]):
                try:
                    nav[j][i + 1] = temp.loc[day]['nav']
                except:
                    nav[j][i + 1] = nav[j][i]
        return nav

    def get_colors(self, names, name_choose):
        color = []
        for i in range(len(names)):
            if names[i] in name_choose:
                color.append('red')
            else:
                color.append('purple')
        return color

    def get_mds_picture(self, names_similarity, name_choose):
        TOOLTIPS = [
            ("fund_id", "@name"),
        ]

        for k in range(len(names_similarity)):
            mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1).fit(
                names_similarity[k]['similarity']).embedding_
            source = ColumnDataSource(data=dict(
                x=mds[:, 0],
                y=mds[:, 1],
                name=names_similarity[k]['names'],
                color=self.get_colors(
                    names_similarity[k]['names'], name_choose),
            ))
            p = figure(plot_width=700, plot_height=700, tooltips=TOOLTIPS,
                       title="MDS", toolbar_location=None, tools="")
            p.x_range = Range1d(-0.6, 0.6)
            p.y_range = Range1d(-0.6, 0.6)
            p.circle(x='x', y='y', color='color', size=6.5, source=source)
            script, div = components(p, CDN)
            mds_dict = {'script': script, 'div': div}
            self.mds_picture.append(mds_dict)

    def get_mds(self, names, start):
        names_similarity = []

        for k in range((int(self.end_str[:4]) - int(self.start_str[:4])) * 12 + int(self.end_str[5:7]) - int(self.start_str[5:7]) + 1):
            end = start + relativedelta(months=+1, days=-1)
            nav = self.get_nav(names, self.get_timestamp(
                start), self.get_timestamp(end))

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

            names_similarity.append(
                {'similarity': similarity, 'names': temp_names})
            start = start + relativedelta(months=+1)
        return names_similarity

    def get_profit_picture(self, profit_choose):
        date = pd.read_sql(sql='select distinct datetime(date, "unixepoch") from price where date between ? and ? order by date asc',
                           con=self.engine, params=[self.start, self.end])
        date['profit'] = profit_choose
        date.rename(
            columns={'datetime(date, "unixepoch")': 'date'}, inplace=True)
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

    def get_profit(self):

        start = self.start_str.replace(self.start_str[-2:], '01')
        start = datetime.strptime(start, '%Y-%m-%d') - relativedelta(months=+1)
        end = start + relativedelta(months=+1, days=-1)
        names = pd.read_sql(sql='select distinct fund_id from price where date between ? and ? order by random() limit 300',
                                con=self.engine, params=[self.get_timestamp(start), self.get_timestamp(end)])['fund_id'].values

        names_similarity = self.get_mds(names, start)
        clustering = AgglomerativeClustering(n_clusters=4).fit(
            names_similarity[0]['similarity'])
        camp = pd.DataFrame(data=clustering.labels_,
                            index=names_similarity[0]['names'], columns=['label'])
        name_choose = []
        for i in range(4):
            name_choose.append(camp[camp['label'] == i].sample(n=1).index[0])
        self.get_mds_picture(names_similarity, name_choose)

        nav_choose = self.get_nav(name_choose, self.start, self.end)
        interest_choose = 0
        for name in name_choose:
            interest_choose += (pd.read_sql(sql='select interest from interest where date between ? and ? and fund_id = ?',
                                            con=self.engine, params=[self.start, self.end, name])['interest'].sum())

        profit_choose = []
        temp = nav_choose[0][0] + nav_choose[1][0] + \
            nav_choose[2][0] + nav_choose[3][0]
        for i in range(len(nav_choose[0])):
            profit_choose.append(
                (nav_choose[0][i] + nav_choose[1][i] + nav_choose[2][i] + nav_choose[3][i] - temp) / temp * 100)
        profit_choose[-1] += interest_choose / temp * 100

        script_profit, div_profit = self.get_profit_picture(profit_choose)
        return script_profit, div_profit
