#!/usr/bin/env python
# coding: utf-8

import click
import logging
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime

@click.command()
@click.option('--input',
			default=r'csv\measurements.csv',
			help='Input filename of the csv. (default=measurements.csv)')
@click.option('--output',
			default="images/fig-{}.png".format(datetime.now().strftime('%d_%m_%Y_%H_%M_%S')),
			help='Output filename.')
@click.option('--resolution',
			default=5,
			help='Quality of the resulting png. (default=5)')
@click.option('--save',
			default="yes",
			help='Save static output as png. (default=yes)')
def convert(input, output, resolution, save):
	## Read csv from file and clean it
	try:
		df = pd.read_csv(input)
		click.echo('Successfully read csv.')
	except Exception as e:
		click.echo(e)
		return
	# df = df.rename(columns={'0': 'Date', '1': 'Weight'})
	df = df.set_index('Date')
	df.index = pd.DatetimeIndex(data=df.index, dayfirst=True)
	df2 = pd.DataFrame(df['Weight'].resample('W').mean())
	df3 = pd.DataFrame(df['Weight'].resample('M').mean())

	## Plot figure
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df.index, y=df["Weight"],
	                    mode='lines+markers',
	                    name='daily',
	                    line_shape='spline'))
	fig.add_trace(go.Scatter(x=df2.index, y=df2["Weight"],
	                    mode='lines+markers',
	                    name='spline',
	                    line_shape='spline'))
	# fig.add_trace(go.Scatter(x=df3.index, y=df3["Weight"],
	#                     mode='lines+markers',
	#                     name='month',))

	fig.show()

	## Saving figure
	if save == "yes":
		fig.write_image(output, scale=5)
		click.echo("Image saved as {}".format(output))

# Save image to file
if __name__ == "__main__":
	try:
		convert()
	except Exception as e:
		click.echo(e)





