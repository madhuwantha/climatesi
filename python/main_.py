import base64
import random

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
import pandas as pd
import matplotlib.pyplot as plt

app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def plot_mac(data: dict):
    projects = data["projects"]
    ers = data["ers"]
    macs = data["macs"]
    df = pd.DataFrame({"Projects": projects,
                       "ER (CO2e)": ers,
                       "MAC ($/CO2e)": macs,
                       })
    df.sort_values(by=['MAC ($/CO2e)'], inplace=True)
    df.reset_index()
    df.set_index("Projects", inplace=True)
    df["Cumulative ER"] = df["ER (CO2e)"].cumsum()

    df["xpos"] = ""

    for index in df.index:
        i = df.index.get_loc(index)

        if i == 0:  # First index
            df.loc[index, "xpos"] = df.loc[index, "ER (CO2e)"] / 2

        else:
            a = df.loc[index, "ER (CO2e)"] / 2
            b = df.iloc[i - 1, 2]
            df.loc[index, "xpos"] = a + b

    df["xpos_labels"] = df["xpos"] - df["ER (CO2e)"] / 2

    print(df)

    plt.figure(figsize=(14, 8))
    plt.rcParams["font.size"] = 14

    xpos = df["xpos"].values.tolist()
    y = df["MAC ($/CO2e)"].values.tolist()
    w = df["ER (CO2e)"].values.tolist()
    l = []
    for i in range(0, len(y) + 1):
        l.append((random.random(), random.random(), random.random()))
    plt.bar(xpos,
            height=y,
            width=w,
            fill=True,
            color=l,
            alpha=0.75)

    for index in df.index:

        x_ref = df.loc[index, "xpos_labels"]
        y_ref = df.loc[index, "MAC ($/CO2e)"]

        if y_ref <= 0:
            plt.annotate(index, xy=(x_ref, y_ref), xytext=(x_ref, y_ref - 10))
        else:
            plt.annotate(index, xy=(x_ref, y_ref), xytext=(x_ref, y_ref + 10))
    # plt.rcParams['axes.facecolor'] = 'oldlace'
    plt.grid(True, color="lightgray", linewidth="1.4", linestyle="-")
    plt.xlim(0, df["ER (CO2e)"].sum())
    plt.ylim(df["MAC ($/CO2e)"].min() - 20,
             df["MAC ($/CO2e)"].max() + 20)

    plt.xlabel("CO2 equivalent emission (millions of metric ton)")
    plt.ylabel("Cost (US dollars per metric ton of CO2 equivalent)")
    plt.title("Marginal abatement cost curve for Mexico in 2020")

    plt.tight_layout()
    # plt.show()

    string_bytes = io.BytesIO()
    plt.savefig(string_bytes, format='jpg')
    string_bytes.seek(0)
    base64_jpg_data = base64.b64encode(string_bytes.read())

    return base64_jpg_data


class PlotData(BaseModel):
    projects: list
    ers: list
    macs: list


@app.post("/image")
def image(data:  PlotData):
    # projects = ["project 1", "project 2", "project 3", "project 4", "project 5", "project 6", "project 7"]
    #
    # ers = [120, 100, 40, 50, 60, 80, 200]
    #
    # macs = [-50, -20, -10, 10, 15, 25, 30]

    return plot_mac({
        "projects": data.projects,
        "ers": data.ers,
        "macs": data.macs
    })


@app.get("/")
async def root():
    return "index"


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
