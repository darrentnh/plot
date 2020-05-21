#!/usr/bin/env python3
# coding: utf-8

import click
import logging
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime

# Set CLI options
@click.command()
@click.option('--input', '-i',
            default=r'csv/measurements.csv',
            help='Input path to csv (default=csv\measurements.csv).')
@click.option('--output', '-o',
            default="fig-{}.png".format(datetime.now().strftime('%d_%m_%Y_%H_%M_%S')),
            help='Output filename.')
@click.option('--resolution', '-r',
            default=5.0,
            help='Quality of the resulting png (default=5.0).')
@click.option('--save/--no-save',
            default=True,
            help='Save static output as png (default=True).')
def convert(input, output, resolution, save):
    # Read csv from file
    try:
        df = pd.read_csv(input)
        click.echo('Successfully read csv.')
    except Exception as e:
        click.echo(e)
        return

    # Clean data
    df = df.set_index('Date')
    df.index = pd.DatetimeIndex(data=df.index, dayfirst=True)
    df2 = pd.DataFrame(df['Weight'].resample('W').mean())
    df3 = pd.DataFrame(df['Weight'].resample('M').mean())

    # Plot figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Weight"],
                        mode='lines+markers',
                        name='daily',
                        line_shape='spline'))
    fig.add_trace(go.Scatter(x=df2.index, y=df2["Weight"],
                        mode='lines+markers',
                        name='weekly',
                        line_shape='spline'))
    # fig.add_trace(go.Scatter(x=df3.index, y=df3["Weight"],
    #                     mode='lines+markers',
    #                     name='month',))

    fig.show()

    # Saving figure
    if save:
        fig.write_image("images/{}".format(output), scale=5)
        click.echo("Image saved as {}".format(output))

# Run script
if __name__ == "__main__":
    try:
        convert()
    except Exception as e:
        click.echo(e)
