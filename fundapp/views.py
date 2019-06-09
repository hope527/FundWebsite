import pandas as pd
import numpy as np

from django.http import JsonResponse
from django.shortcuts import redirect, render
from fundapp.profit_test import img
from datetime import datetime
from sqlalchemy import create_engine
from collections import defaultdict

engine = create_engine('sqlite:///fund.db')


def test(request):
    if request.method == "POST":
        url = "/test/" + "-".join([request.POST['start_year'], request.POST['start_month']]) + \
            "&" + "-".join([request.POST['end_year'], request.POST['end_month']]) + \
            "&" + request.POST['investement_type'] + \
            "& " + request.POST['sharpe_ratio'] + \
            "," + request.POST['std'] + \
            "," + request.POST['beta'] + \
            "," + request.POST['treynor_ratio'] + \
            "&" + request.POST['btest_time'] + \
            "&" + request.POST['money'] + \
            "&" + request.POST['buy_ratio0'] + \
            "," + request.POST['buy_ratio1'] + \
            "," + request.POST['buy_ratio2'] + \
            "," + request.POST['buy_ratio3'] + \
            "&" + request.POST['strategy'] + \
            "&" + request.POST['frequency'] + "/"
        return render(request, "test_show.html", locals())
    return render(request, "test.html", locals())


def test_respoonse(request, start, end, investement_type, ratio, btest_time, money, buy_ratio, strategy, frequency):
    ratio = ratio.split(",")
    response_data = img(start=datetime.strptime(start, '%Y-%m'),
                        end=datetime.strptime(end, '%Y-%m'),
                        investement_type=np.asarray(
                            investement_type.split(" ")),
                        sharpe_ratio=ratio[0],
                        std=ratio[1],
                        beta=ratio[2],
                        treynor_ratio=ratio[3],
                        btest_time=btest_time,
                        money=money,
                        buy_ratio=np.asarray(
                            buy_ratio.split(","), dtype=np.float),
                        strategy=strategy,
                        frequency=frequency)
    return JsonResponse(response_data)

def index(request):
    engine = create_engine('sqlite:///fund.db')
    items = pd.read_sql(
        sql='select * from basic_information limit 10', con=engine)
    items['url'] = "id=" + items['fund_id'] + "&area=" + items['area']
    items = items.to_dict('records', into=defaultdict(list))
    return render(request, "index.html", locals())


def index_response(request, page):
    items = pd.read_sql(
        sql='select * from basic_information limit ?,10', con=engine, params=[(page-1)*10])
    items['url'] = "id=" + items['fund_id'] + "&area=" + items['area']
    items = items.to_dict('index')
    return JsonResponse(items)


def search(request, column, keyword):
    items = pd.read_sql(sql='select * from basic_information', con=engine)
    temp = items[column].str.lower()
    if "fee" in column:
        items = items[items[column] <= float(keyword)]
    else:
        items = items[temp.str.contains(keyword.lower())]
    items['url'] = "id=" + items['fund_id'] + "&area=" + items['area']
    items = items.to_dict('index')
    return JsonResponse(items)


def index_form(request, fund_id, area):
    if area == "境內":
        item = pd.read_sql("select * from basic_information,domestic_information where basic_information.fund_id = ? and domestic_information.fund_id = ?",
                           con=engine, params=[fund_id, fund_id])
        item = item.drop(["fund_id"], axis=1)
        item = item.to_dict('records', into=defaultdict(list))
        return render(request, "index_form.html", locals())
    elif area == "境外":
        item = pd.read_sql("select * from basic_information,overseas_information where basic_information.fund_id = ? and overseas_information.fund_id = ?",
                           con=engine, params=[fund_id, fund_id])
        item = item.drop(["fund_id"], axis=1)
        item = item.to_dict('records', into=defaultdict(list))
        return render(request, "index_oversea.html", locals())
