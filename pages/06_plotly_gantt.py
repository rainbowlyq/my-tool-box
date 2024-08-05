# -*- coding: utf-8 -*-
"""
@File    : 06_plotly_gantt.py
@Time    : 2024/8/2 13:01
@Author  : lyq
@Description : 
"""

import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Plotly Gantt Chart", page_icon="🗓", layout="wide")

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


def load_sidebar(cols):
    flight_id = st.sidebar.selectbox("Flight ID Column", cols,
                                     index=cols.index('id') if 'id' in cols else 0)
    flight_no = st.sidebar.selectbox("Flight No Column", cols,
                                     index=cols.index('flightNo') if 'flightNo' in cols else 0)
    td = st.sidebar.selectbox("Departure Time Column", cols, index=cols.index('td') if 'td' in cols else 0)
    ta = st.sidebar.selectbox("Arrival Time Column", cols, index=cols.index('ta') if 'ta' in cols else 0)
    org = st.sidebar.selectbox("Origin Airport Column", cols,
                               index=cols.index('depaAirportFourCode') if 'depaAirportFourCode' in cols else 0)
    dest = st.sidebar.selectbox("Destination Airport Column", cols,
                                index=cols.index('arriAirportFourCode') if 'arriAirportFourCode' in cols else 0)
    tail = st.sidebar.selectbox("Tail Number Column", cols,
                                index=cols.index('aircraftRegisterNo') if 'aircraftRegisterNo' in cols else 0)
    fleet = st.sidebar.selectbox("Fleet Column", cols,
                                 index=cols.index('aircraftShortType') if 'aircraftShortType' in cols else None)
    return flight_id, flight_no, td, ta, org, dest, tail, fleet

def main():
    # st.title("Plotly Gantt Chart")

    # upload flights data
    file = st.sidebar.file_uploader("Upload your flights data file", type=["csv"])
    if file is None:
        return
    df = load_csv(file)

    # select columns
    flight_id, flight_no, td, ta, org, dest, tail, fleet = load_sidebar(df.columns.tolist())

    # process data
    # df['label'] = df[flight_no] + ' [' + df[org] + '-' + df[dest] + ']'
    df['label'] = df[org] + '-' + df[dest]
    df[tail] = 'T' + df[tail]
    df[td] = pd.to_datetime(df[td])
    df[ta] = pd.to_datetime(df[ta])

    # filter flights
    selected_fleets = st.sidebar.multiselect("Fleets to show", df[fleet].unique(), default=df[fleet].unique())
    df = df[df[fleet].isin(selected_fleets)]
    # selected_tails = st.sidebar.multiselect("Tails to show", df[tail].unique(), default=df[tail].unique())
    # df = df[df[tail].isin(selected_tails)]
    if len(df) == 0:
        return

    # create gantt chart
    fig = px.timeline(df, x_start=td, x_end=ta, y=tail, color=fleet, text='label',
                      hover_data=[flight_id, flight_no, tail, org, dest, td, ta, fleet], height=10 * len(df))
    fig.update_xaxes(rangeslider_visible=True, rangeslider_thickness=min(5 / len(df), 1),
                     # showspikes=True, spikesnap="cursor", spikemode="across"
                     )
    fig.update_yaxes(showgrid=True, autorange="reversed")
    fig.update_traces(textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()
