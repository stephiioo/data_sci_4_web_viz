from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

url = '/home/stephanie_ogbebor/python_shiny/PLACES__Local_Data_for_Better_Health__County_Data_2023_release.csv'
df = pd.read_csv(url)
df_depression = df[(df['MeasureId'] == 'DEPRESSION') & (df['Data_Value_Type'] == 'Age-adjusted prevalence')]

@app.route('/', methods=['GET', 'POST'])
def index():
    counties = sorted(df_depression['LocationName'].unique())
    selected_county = request.form.get('county') or counties[0]
    
    img = plot_data(selected_county)
    
    return render_template("index.html", counties=counties, selected_county=selected_county, img=img)

def plot_data(County):
    overall_avg = df_depression['Data_Value'].mean()
    selected_county_avg = df_depression[df_depression['LocationName'] == County]['Data_Value'].mean()

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(['Selected County', 'Average across all Counties'], [selected_county_avg, overall_avg], color=['lightcoral', 'dodgerblue'])
   
    ax.axhline(selected_county_avg, color='gray', linestyle='dashed', alpha=0.7)
    ax.set_ylabel('Data Value (Age-adjusted prevalence) - Percent')
    ax.set_ylim(0, 30)
    ax.set_title('Depression Age-adjusted Prevalence Comparison')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return base64.b64encode(img.getvalue()).decode()


if __name__ == '__main__':
    app.run(debug=True)