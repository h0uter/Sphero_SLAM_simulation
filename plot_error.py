import plotly.plotly as py
import plotly.graph_objs as go

# plotly
# import plotly
# plotly.tools.set_credentials_file(
#     username='houterm', api_key='putYaOwnKey')

def plot(sphero, step_count):
    if step_count == 40000:
    # if step_count == 1000:
        x_error_behaviour = go.Scatter(
            x=sphero.plot_time_list,
            y=sphero.plot_x_error_list,
            name='x direction'
        )
        y_error_behaviour = go.Scatter(
            x=sphero.plot_time_list,
            y=sphero.plot_y_error_list,
            name='y direction'
        )
        x_unfiltered_error_behaviour = go.Scatter(
            x=sphero.plot_time_list,
            y=sphero.plot_x_unfiltered_error_list,
            name='unfiltered x direction'
        )
        y_unfiltered_error_behaviour = go.Scatter(
            x=sphero.plot_time_list,
            y=sphero.plot_y_unfiltered_error_list,
            name='unfiltered y direction'
        )

        layout = go.Layout(
            title=go.layout.Title(
                # text='Error Behaviour 3: Maze',
                xref='paper',
                x=0
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='Time (s)',
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
                    text='Error (pixels)',
                    font=dict(
                        family='Courier New, monospace',
                        size=28,
                        color='#000'
                    )
                ),
                # showticklabels=False
            ),
            legend=dict(
                # x=0,
                # y=0,
                x= 1.1,
                y= 1.2,
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
        # print(sphero.plot_time_list)
        # print(sphero.plot_x_error_list)
        data = [x_error_behaviour, y_error_behaviour, x_unfiltered_error_behaviour, y_unfiltered_error_behaviour]

        fig = go.Figure(data=data, layout=layout)
        # py.iplot(fig, filename='styling-names')

        # py.plot(data, filename='error behaviour', auto_open=True)
        py.plot(fig, filename='unfiltered_error', auto_open=True)
