from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# load dataset
df = pd.read_csv("cost_of_living_us.csv")

@app.route("/")
def index():
    # sample county
    county = "Travis County"
    county_data = df[df["county"] == county].iloc[0]

    # expense breakdown
    expenses = {
        "Housing": county_data["housing_cost"],
        "Food": county_data["food_cost"],
        "Transportation": county_data["transportation_cost"],
        "Healthcare": county_data["healthcare_cost"],
        "Childcare": county_data["childcare_cost"],
        "Other": county_data["other_necessities_cost"],
        "Taxes": county_data["taxes"]
    }

    exp_df = pd.DataFrame(list(expenses.items()), columns=["Category", "Cost"])

    # pie chart
    fig = px.pie(exp_df, values="Cost", names="Category", title=f"Expense Breakdown - {county}")
    graph_html = fig.to_html(full_html=False)

    return render_template("index.html", plot=graph_html)

if __name__ == "__main__":
    app.run(debug=True)