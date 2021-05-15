import plotly
from IPython.html.widgets import interact
from plotly.graph_objs import graph_objs as go

plotly.offline.init_notebook_mode()
from plotly.offline import iplot


def view_image(w):
    x_data = [1, 2, 3]
    x1 = [i + w for i in x_data]
    fig1 = go.Scatter(x=x1, y=[4, 5, 6])
    fig2 = go.Scatter(x=x_data, y=[4, 5, 6])
    iplot([fig1, fig2])


interact(view_image, w=(0, 100))
