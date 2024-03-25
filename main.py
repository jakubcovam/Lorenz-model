import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


# Define the Lorenz system
def lorenz(t, state, sigma, beta, rho):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# Solve the Lorenz system
def solve_lorenz(sigma=10, beta=8/3, rho=28, init_state=[1, 1, 1], t_span=[0, 50], t_eval=np.linspace(0, 50, 10000)):
    return solve_ivp(lorenz, t_span, initial_state, args=(sigma, beta, rho), t_eval=t_eval)


# Initial conditions
initial_state = [1, 1, 1]

# Dash app setup
app = Dash(__name__)

# App layout with sliders next to the plot
app.layout = html.Div([
    html.H1("Lorenz Attractor", style={'textAlign': 'center'}),
    html.H2("Set parameters:", style={'textAlign': 'left'}),
    html.Div([
        html.Div([
            html.Label("Sigma:"),
            dcc.Slider(id='sigma-slider',
                       min=0,
                       max=30,
                       step=0.1,
                       value=10,
                       marks={i: f'{i}' for i in range(0, 31, 5)}),
            html.Div(id='sigma-value', style={'padding': '10px'}),

            html.Label("Beta:"),
            dcc.Slider(id='beta-slider',
                       min=0,
                       max=5,
                       step=0.1,
                       value=8/3,
                       marks={i: f'{i:.1f}' for i in [0, 1, 2, 3, 4, 5]}),
            html.Div(id='beta-value', style={'padding': '10px'}),

            html.Label("Rho:"),
            dcc.Slider(id='rho-slider',
                       min=0,
                       max=100,
                       step=0.1,
                       value=28,
                       marks={i: f'{i}' for i in range(0, 101, 10)}),
            html.Div(id='rho-value', style={'padding': '10px'}),
        ], style={'padding': 20, 'flex': 1}),

        html.Div([
            dcc.Graph(id='lorenz-plot'),
        ], style={'padding': 20, 'flex': 3}),
    ], style={'display': 'flex', 'flexDirection': 'row'})
])


# Callbacks to update the slider value labels
@app.callback(Output('sigma-value', 'children'), [Input('sigma-slider', 'value')])
def update_sigma_label(value):
    return f'Sigma: {value}'


@app.callback(Output('beta-value', 'children'), [Input('beta-slider', 'value')])
def update_beta_label(value):
    return f'Beta: {value:.1f}'


@app.callback(Output('rho-value', 'children'), [Input('rho-slider', 'value')])
def update_rho_label(value):
    return f'Rho: {value}'


# Callback to update graph based on slider inputs
@app.callback(
    Output('lorenz-plot', 'figure'),
    [Input('sigma-slider', 'value'),
     Input('beta-slider', 'value'),
     Input('rho-slider', 'value')]
)
def update_graph(sigma, beta, rho):
    sol = solve_lorenz(sigma=sigma, beta=beta, rho=rho, init_state=initial_state)
    fig = go.Figure(data=go.Scatter3d(x=sol.y[0], y=sol.y[1], z=sol.y[2], mode='lines', line=dict(color='blue', width=2)))
    fig.update_layout(scene=dict(xaxis_title='X Axis', yaxis_title='Y Axis', zaxis_title='Z Axis'),
                      margin=dict(l=0, r=0, b=0, t=0))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
