from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# load dataset
df = pd.read_csv("cost_of_living_us.csv")

@app.route("/")

def index():
    # get county from query string
    county = request.args.get("county", "Travis County, Texas")

    #get county's data, ignore caps and spaces
    matches = df[df["county"].str.strip().str.lower() == county.strip().lower()]

    if not matches.empty:
        county_data = matches.iloc[0]
    else:
        #if no match found. fall back to first row
        county_data = df.iloc[0]

    # expense dictionary
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

    # pass counties list for dropdown menu
    counties = sorted(df["county"].unique())

    return render_template("index.html", 
                           plot=graph_html,
                           counties=counties,
                           selected_county=county)

# run app
if __name__ == "__main__":
    app.run(debug=True)