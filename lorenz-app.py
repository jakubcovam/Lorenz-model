import numpy as np
from scipy.integrate import odeint
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

footer_html = """
<style>.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgb(211, 211, 211);
    color: black;
    text-align: center;
}
</style>
<div class='footer'>
   By <a href="https://github.com/jakubcovam/" target="_blank">jakubcovam</a> using Streamlit.
</div>
 """

# Define the Lorenz system
def lorenz(X, t, sigma, beta, rho):
    x, y, z = X
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


# Initial conditions and time points
X0 = [1.0, 1.0, 1.0]
t = np.linspace(0, 50, 10000)

def app():
    st.title("Lorenz Attractor")

    st.sidebar.header('Parameters')
    sigma = st.sidebar.slider("Sigma (σ)", min_value=0, value=10, max_value=30, step=1)
    beta = st.sidebar.slider("Beta (β)", min_value=0.0, value=2.7, max_value=5.0, step=0.1)
    rho = st.sidebar.slider("Rho (ρ)", min_value=0, value=28, max_value=100, step=1)

    type_plot = st.sidebar.checkbox("Interactive plot")

    st.latex(r'''
        \begin{align*}
            \frac{dx}{dt} &= \sigma (y - x) \\
            \frac{dy}{dt} &= x (\rho - z) - y \\
            \frac{dz}{dt} &= x y - \beta z
        \end{align*}
        ''')

    # Solve the differential equations
    solution = odeint(lorenz, X0, t, args=(sigma, beta, rho))
    x, y, z = solution.T

    if type_plot:
        # Create an interactive 3D plot using Plotly
        fig = px.line_3d(x=x, y=y, z=z, width=850, height=850)
        st.plotly_chart(fig)
    else:
        # Create a 3D static plot
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z, lw=0.5)
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('y', fontsize=14)
        ax.set_zlabel('z', fontsize=14)
        ax.grid(True)
        # Display the plot in Streamlit
        st.pyplot(fig)

    # Render the footer
    st.sidebar.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    app()