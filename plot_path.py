import plotly.plotly as py
import plotly.graph_objs as go


def plot(sphero, step_count):
    if step_count == 17000:
        # if step_count == 1000:
        path = go.Scatter(
            x=sphero.plot_path[0],
            y=sphero.plot_path[1],
            name='Path'
        )
        predicted_path = go.Scatter(
            x=sphero.plot_predicted_path[0],
            y=sphero.plot_predicted_path[1],
            name='predicted Path'
        )

        layout = go.Layout(
            title=go.layout.Title(
                text='Path',
                xref='paper',
                x=0
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='x (pixels)',
                    font=dict(
                        family='Courier New, monospace',
                        size=28,
                        color='#000'
                    )
                ),
                # showticklabels=False
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text='y (pixels)',
                    font=dict(
                        family='Courier New, monospace',
                        size=28,
                        color='#000'
                    )
                ),
                # showticklabels=False
            ),
            legend=dict(
                x=0,
                y=0,
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#000'
                ),
                orientation="h",
                # bgcolor='#E2E2E2',
                # bordercolor='#FFFFFF',
                # borderwidth=2
            )
        )

        data = [path, predicted_path]

        fig = go.Figure(data=data, layout=layout)
        # py.iplot(fig, filename='styling-names')

        # py.plot(data, filename='error behaviour', auto_open=True)
        py.plot(fig, filename='path', auto_open=True)
