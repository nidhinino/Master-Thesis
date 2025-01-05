from flask import Flask
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# Load data
data = pd.read_csv('esg_counts.csv')

# Extract year and company name from filename
def create_alias(filename):
    pattern = r"^(.*?)_(\d{4})"
    match = re.match(pattern, filename)
    if match:
        company_name = match.group(1).replace('_', ' ')
        year = match.group(2)
        return f"{company_name} {year}", company_name, year
    else:
        return filename, filename, None

# Apply the function and create new columns
data[['Alias', 'Company', 'Year']] = pd.DataFrame(
    data['Filename'].apply(create_alias).tolist(), 
    columns=['Alias', 'Company', 'Year']
)

# Initialize Flask app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define styles
dropdown_style = {
    "width": "100%",
    "margin-bottom": "10px"
}

dropdown_container_style = {
    "margin-bottom": "20px",
    "z-index": 1000
}

plot_container_style = {
    "border": "1px solid #ddd",
    "border-radius": "5px",
    "padding": "15px",
    "margin": "10px",
    "background-color": "white",
    "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
}

# Layout
app.layout = dbc.Container([
    html.H1("ESG Counts Dashboard", className="text-center my-4"),
    dcc.Tabs(id="dashboard-tabs", value="individual", children=[
        dcc.Tab(label="Individual Counts Dashboard", value="individual"),
        dcc.Tab(label="Comparison Dashboard", value="comparison")
    ]),
    html.Div(id="dashboard-content")
])

def individual_dashboard():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Select Method Name:"),
                dcc.Dropdown(
                    id="method-dropdown",
                    options=[{"label": method, "value": method} for method in data["Folder"].unique()],
                    value='pypdf2',
                    placeholder="Choose a method",
                    clearable=True
                )
            ], md=4),
            dbc.Col([
                html.Label("Select Companies:"),
                dcc.Dropdown(
                    id="company-dropdown",
                    options=[
                        {"label": company, "value": company} 
                        for company in sorted(data["Company"].unique())
                    ],
                    value=data["Company"].unique().tolist(),
                    multi=True,
                    style=dropdown_style
                )
            ], md=4),
            dbc.Col([
                html.Label("Select Years:"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[
                        {"label": str(year), "value": str(year)} 
                        for year in sorted(data["Year"].unique())
                    ],
                    value=data["Year"].unique().tolist(),
                    multi=True,
                    style=dropdown_style
                )
            ], md=4)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Button("Submit", id="submit-button", color="primary", className="me-2")
            ])
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.Div("Please select a method to display the data.", id="prompt", 
                            style={"textAlign": "center", "color": "red"}), width=12)
        ]),

        dbc.Row(
            [
        dbc.Col([
            html.Div([
                dcc.Graph(id="bar-chart")
            ], style=plot_container_style)
        ], md=6),
        dbc.Col([
            html.Div([
                dcc.Graph(id="radar-chart")
            ], style=plot_container_style)
        ], md=6)
        ], className="mb-4"),
       
       dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="pie-chart")
            ], style=plot_container_style)
        ], md=6),
        dbc.Col([
            html.Div([
                dcc.Graph(id="stacked-bar")
            ], style=plot_container_style)
        ], md=6)
        ], className="mb-4"),

       
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="line-plot")
            ], style=plot_container_style)
        ], md=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="esg-heatmap", style={"height": "70vh"})
            ], style=plot_container_style)
        ], md=12)
    ])
    
    ])

def comparison_dashboard():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Select Companies:"),
                dcc.Dropdown(
                    id="comparison-company-dropdown",
                    options=[
                        {"label": company, "value": company} 
                        for company in sorted(data["Company"].unique())
                    ],
                    value=data["Company"].unique().tolist(),
                    multi=True,
                    style=dropdown_style
                )
            ], width=6),
            dbc.Col([
                html.Label("Select Years:"),
                dcc.Dropdown(
                    id="comparison-year-dropdown",
                    options=[
                        {"label": str(year), "value": str(year)} 
                        for year in sorted(data["Year"].unique())
                    ],
                    value=data["Year"].unique().tolist(),
                    multi=True,
                    style=dropdown_style
                )
            ], width=6)
        ], className="mb-4"),
        dbc.Row(
            [
        dbc.Col([
            html.Div([
                dcc.Graph(id="bar-plot-e")
            ], style=plot_container_style)
        ], md=6),
        dbc.Col([
            html.Div([
                dcc.Graph(id="bar-plot-s")
            ], style=plot_container_style)
        ], md=6)
        ], className="mb-4"),
       
        dbc.Row(
            [
        dbc.Col([
            html.Div([
                dcc.Graph(id="bar-plot-g")
            ], style=plot_container_style)
        ], md=6)
        ], className="mb-4"),
       
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id="comparison-heatmap", style={"height": "40vh"})
                ], style=plot_container_style)
            ], md=12)
        ])
        
    ])

@app.callback(Output("dashboard-content", "children"), Input("dashboard-tabs", "value"))
def switch_dashboard(tab):
    if tab == "comparison":
        return comparison_dashboard()
    return individual_dashboard()

# Update the callback for individual dashboard
@app.callback([
    Output("bar-chart", "figure"),
    Output("radar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("stacked-bar", "figure"),
    Output("line-plot", "figure"),
    Output("esg-heatmap", "figure"),
    Output("prompt", "style")
], [Input("submit-button", "n_clicks")], [
    Input("company-dropdown", "value"),
    Input("method-dropdown", "value"),
    Input("year-dropdown", "value")
])
def update_individual_dashboard(n_clicks, selected_companies, selected_method, selected_years):
    if not selected_companies or not selected_years:
        return [{}, {}, {}, {}, {}, {}, {"textAlign": "center", "color": "red"}]
    
    filtered_data = data[
        (data["Company"].isin(selected_companies)) &
        (data["Year"].isin(selected_years))
    ]
    
    if selected_method:
        filtered_data = filtered_data[filtered_data["Folder"] == selected_method]
    
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=filtered_data["Alias"], y=filtered_data["Social_Count"], name="Social Count"))
    bar_fig.add_trace(go.Bar(x=filtered_data["Alias"], y=filtered_data["Environmental_Count"], name="Environmental Count"))
    bar_fig.add_trace(go.Bar(x=filtered_data["Alias"], y=filtered_data["Governance_Count"], name="Governance Count"))
    bar_fig.update_layout(title="Category-Wise Comparison", barmode="group", xaxis_title="Filename Alias", yaxis_title="Counts")
    
    radar_categories = ["Social_Count", "Environmental_Count", "Governance_Count"]
    radar_fig = go.Figure()
    for alias in filtered_data["Alias"].unique():
        values = filtered_data[filtered_data["Alias"] == alias][radar_categories].values.flatten().tolist()
        values += values[:1]
        radar_fig.add_trace(go.Scatterpolar(r=values, theta=radar_categories + [radar_categories[0]], fill="toself", name=alias))
    radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)), title="Method Efficiency (Radar Chart)")
    
    total_counts = filtered_data[["Social_Count", "Environmental_Count", "Governance_Count"]].sum()
    pie_fig = px.pie(names=total_counts.index, values=total_counts.values, title="Category Contribution")
    
    stacked_fig = go.Figure()
    stacked_fig.add_trace(go.Bar(x=filtered_data["Alias"], y=filtered_data["Social_Count"], name="Social Count"))
    stacked_fig.add_trace(go.Bar(x=filtered_data["Alias"], y=filtered_data["Environmental_Count"], name="Environmental Count", base=filtered_data["Social_Count"]))
    stacked_fig.add_trace(go.Bar(x=filtered_data["Alias"], y=filtered_data["Governance_Count"], name="Governance Count", base=filtered_data["Social_Count"] + filtered_data["Environmental_Count"]))
    stacked_fig.update_layout(title="Discrepancy Chart (Stacked Bar)", barmode="stack", xaxis_title="Filename Alias", yaxis_title="Counts")
    
    line_fig = go.Figure()
    for category in ["Social_Count", "Environmental_Count", "Governance_Count"]:
        line_fig.add_trace(go.Scatter(x=filtered_data["Alias"], y=filtered_data[category], mode="lines+markers", name=category))
    line_fig.update_layout(title="File-Specific Trends", xaxis_title="Filename Alias", yaxis_title="Counts")
    
    # Correct heatmap pivot and display
    filtered_data_melted = filtered_data.melt(
        id_vars=["Alias"], 
        value_vars=["Social_Count", "Environmental_Count", "Governance_Count"],
        var_name="Category", 
        value_name="Count"
    )
    height = 50 * len(filtered_data["Alias"].unique())
    esg_heatmap_fig = px.imshow(
        filtered_data_melted.pivot(index="Alias", columns="Category", values="Count"),
        labels={"x": "ESG Category", "y": "Company", "color": "Count"},
        color_continuous_scale="rdbu_r",
        text_auto=True,
        height=height
    )
    esg_heatmap_fig.update_layout(
        title="ESG Heatmap (Company vs. ESG Category)",
        xaxis_title="ESG Category",
        yaxis_title="Company",
    )

    
    return bar_fig, radar_fig, pie_fig, stacked_fig, line_fig, esg_heatmap_fig, {"display": "none"}


@app.callback([
    Output("bar-plot-e", "figure"),
    Output("bar-plot-s", "figure"),
    Output("bar-plot-g", "figure"),
    Output("comparison-heatmap", "figure"),
], [
    Input("comparison-company-dropdown", "value"),
    Input("comparison-year-dropdown", "value")
])
def update_comparison_dashboard(selected_companies, selected_years):
    filtered_data = data[
        (data["Company"].isin(selected_companies)) &
        (data["Year"].isin(selected_years))
    ]
    
    # Generate Bar Plots
    bar_e = px.bar(filtered_data, x="Alias", y="Environmental_Count", color="Folder", title="Environmental Count by Method", barmode="group")
    bar_s = px.bar(filtered_data, x="Alias", y="Social_Count", color="Folder", title="Social Count by Method", barmode="group")
    bar_g = px.bar(filtered_data, x="Alias", y="Governance_Count", color="Folder", title="Governance Count by Method", barmode="group")
    
    # Prepare Heatmap Data
    heatmap_data = filtered_data.melt(
        id_vars=["Alias", "Folder"],
        value_vars=["Social_Count", "Environmental_Count", "Governance_Count"],
        var_name="Category",
        value_name="Count"
    )
    
    # Create all possible method-category combinations
    methods = sorted(filtered_data["Folder"].unique())
    categories = ["Environmental", "Social", "Governance"]
    all_combinations = [(method, category) for method in methods for category in categories]
    
    # Map the original category names
    category_mapping = {
        "Social_Count": "Social",
        "Environmental_Count": "Environmental", 
        "Governance_Count": "Governance"
    }
    heatmap_data["Category"] = heatmap_data["Category"].map(category_mapping)
    
    # Create and sort Method_Category to ensure consistent order
    heatmap_data["Method_Category"] = heatmap_data["Folder"] + " - " + heatmap_data["Category"]
    expected_categories = [f"{method} - {category}" for method, category in all_combinations]
    
    # Generate pivot table
    pivot_table = heatmap_data.pivot(index="Method_Category", columns="Alias", values="Count")
    
    # Reindex to ensure all categories are present and in correct order
    pivot_table = pivot_table.reindex(expected_categories)
    print(pivot_table)

    # Generate Heatmap
    heatmap_fig = px.imshow(
        pivot_table,
        labels={"x": "PDF Alias", "y": "Method and ESG Category", "color": "Count"},
        color_continuous_scale="rdbu_r",
        text_auto=True,
        height=min(500, 50 * len(pivot_table.index))
    )
    
    heatmap_fig.update_layout(
        title="Comparison Heatmap (Methods vs. ESG)",
        xaxis_title="PDF Alias",
        yaxis_title="Method and ESG Category",
        margin={"t": 50, "l": 200, "r": 50, "b": 50},
        yaxis=dict(
        automargin=True,  # Automatically adjust margins for labels
        tickmode="array",  # Use array for tick values
        tickvals=list(range(len(pivot_table.index))),  # Set ticks for all rows
        ticktext=pivot_table.index.tolist(),  # Use row labels for ticks
        scaleanchor=None,  # Prevent scaling based on figure size
    ),
    )

    return bar_e, bar_s, bar_g, heatmap_fig


if __name__ == "__main__":
    app.run_server(debug=True)