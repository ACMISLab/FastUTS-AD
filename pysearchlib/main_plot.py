import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=[2.5, 3], y=[7,7], fill='tozeroy',
                    mode='none' # override default markers+lines
                    ))
fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 1, 7], fill='tonexty',
                    mode= 'none'))
fig.add_trace(go.Line(x=[1,2,3],y=[2,3,4]))

fig.show()
