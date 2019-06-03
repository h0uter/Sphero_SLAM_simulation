import plotly.plotly as py
import plotly.graph_objs as go

# plotly
# import plotly
# plotly.tools.set_credentials_file(
#     username='houterm', api_key='KK2RpBgrE4WFWr0Fi6si')


def plot(sphero, step_count):
    if step_count == 40000:
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

        layout = go.Layout(
            title=go.layout.Title(
                text='Error Behaviour 3: Maze',
                xref='paper',
                x=0
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='Time (s)',
                    font=dict(
                        family='Courier New, monospace',
                        size=28,
                        color='#7f7f7f'
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
                        color='#7f7f7f'
                    )
                ),
                # showticklabels=False
            ),
            legend=dict(
                # x=0,
                # y=1,
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#000'
                ),
                # bgcolor='#E2E2E2',
                # bordercolor='#FFFFFF',
                # borderwidth=2
            )
        )
        # print(sphero.plot_time_list)
        # print(sphero.plot_x_error_list)
        data = [x_error_behaviour, y_error_behaviour]

        fig = go.Figure(data=data, layout=layout)
        # py.iplot(fig, filename='styling-names')

        # py.plot(data, filename='error behaviour', auto_open=True)
        py.plot(fig, filename='error behaviour 3 Maze', auto_open=True)
