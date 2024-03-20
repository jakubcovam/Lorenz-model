# Install packages
# install.packages("shiny")
# install.packages("deSolve")
# install.packages("plotly")

# Activate the libraries
library(shiny)
library(deSolve)
library(plotly)

# Define the Lorenz system
lorenz <- function(t, state, parameters) {
  with(as.list(c(state, parameters)), {
    dx <- sigma * (y - x)
    dy <- x * (rho - z) - y
    dz <- x * y - beta * z
    list(c(dx, dy, dz))
  })
}

# Define UI
ui <- fluidPage(
  titlePanel("Interactive Lorenz Attractor"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("sigma", "Sigma:", min = 0, max = 30, value = 10),
      sliderInput("rho", "Rho:", min = 0, max = 100, value = 28),
      sliderInput("beta", "Beta:", min = 0, max = 5, value = 8 / 3)
    ),
    mainPanel(
      plotlyOutput("lorenzPlot", height = "500px")
    )
  )
)

# Define server logic
server <- function(input, output) {
  output$lorenzPlot <- renderPlotly({
    times <- seq(0, 100, by = 0.01)
    state <- c(x = 1, y = 1, z = 1)
    parameters <- c(sigma = input$sigma, rho = input$rho, beta = input$beta)
    
    out <- ode(y = state, times = times, func = lorenz, parms = parameters)
    df <- as.data.frame(out)
    
    plot_ly(df, x = ~x, y = ~y, z = ~z, type = 'scatter3d', mode = 'lines') %>%
      layout(scene = list(xaxis = list(title = 'X'),
                          yaxis = list(title = 'Y'),
                          zaxis = list(title = 'Z')),
             margin = list(l = 0, r = 0, b = 0, t = 0, pad = 4))
  })
}

# Run the application
shinyApp(ui = ui, server = server)
