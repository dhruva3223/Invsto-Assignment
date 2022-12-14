from django.shortcuts import render, redirect
import pandas as pd
from .models import Data
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
from django.core.files.storage import FileSystemStorage


def index(request):
    if request.method == "POST":
        request_file = request.FILES['document']
        if request_file:
            fs = FileSystemStorage()
            fs.delete("HINDALCO.xlsx")
            fs.save(request_file.name, request_file)
            Data.objects.all().delete()
            df = pd.read_excel("media/HINDALCO.xlsx")
            for df in df.itertuples():
                obj = Data.objects.create(
                    datetime=df.datetime,
                    close=df.close,
                    high=df.high,
                    low=df.low,
                    open=df.open,
                    volume=df.volume,
                    instrument=df.instrument,
                )
                obj.save()
            return redirect(analysis)
    return render(request, "index.html")


def SMA(data, period=30, column='close'):
    return data[column].rolling(window=period).mean()


def analysis(request):
    data = Data.objects.all()
    values = data.values()
    df = pd.DataFrame.from_records(values)
    df = df.set_index(pd.DatetimeIndex(df['datetime'].values))

    df['SMA20'] = SMA(df, 20)
    df['SMA50'] = SMA(df, 50)

    df['Signal'] = np.where(df['SMA20'] > df['SMA50'], 1, 0)
    df['Position'] = df['Signal'].diff()

    df['Buy'] = np.where(df['Position'] == 1, df['close'], np.NAN)
    df['Sell'] = np.where(df['Position'] == -1, df['close'], np.NAN)
    plt.figure(figsize=(16, 8))
    plt.title('HINDALCO Simple Moving Average Crossover', fontsize=18)
    plt.plot(df['close'], alpha=0.6, label='Close', zorder=1)
    plt.plot(df['SMA20'], alpha=0.6, label='SMA20', zorder=1)
    plt.plot(df['SMA50'], alpha=0.6, label='SMA50', zorder=1)
    plt.scatter(df.index, df['Buy'], alpha=1, label='Buy Signal',
                marker='^', color='green', zorder=3, s=100)
    plt.scatter(df.index, df['Sell'], alpha=1, label='Sell Signal',
                marker='v', color='red', zorder=3, s=100)
    plt.xlabel('datetime', fontsize=18)
    plt.ylabel('Close Price', fontsize=18)
    plt.legend(loc='best')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    figure = base64.b64encode(image_png)
    figure = figure.decode('utf-8')

    return render(request, "analysis.html", {"figure": figure})
