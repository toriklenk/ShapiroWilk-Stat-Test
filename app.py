from flask import Flask, render_template, request
from scipy.stats import shapiro

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get form data
        study_title = request.form.get('study_title', 'Untitled Study')
        data = request.form['data_points']

        # Validate input
        if not data.strip():
            return render_template('input_data.html', error="Please provide data points.")
        try:
            data_points = [float(x) for x in data.split()]
        except ValueError:
            return render_template('input_data.html', error="Please enter valid numbers.")

        # Perform Shapiro-Wilk test
        stat, p_value = shapiro(data_points)

        # Determine normality
        if p_value > 0.05:
            normality = "Yes, the data is normally distributed. Move forward with either the Dixon's Outlier Test (N ≤ 30) or the Grubbs' Test (N > 30)."
            explanation = "The p-value is greater than 0.05, so we fail to reject the null hypothesis."
        else:
            normality = "No, the data is not normally distributed. Move Forward with the IQR Outlier Test."
            explanation = "The p-value is less than or equal to 0.05, so we reject the null hypothesis."

        # Pass results to the template
        return render_template(
            'input_data.html',
            study_title=study_title,
            data=data_points,
            stat=stat,
            p_value=p_value,
            normality=normality,
            explanation=explanation,
            error=None
        )

    # Render initial page
    return render_template('input_data.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)