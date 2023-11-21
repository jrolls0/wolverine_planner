from flask import Flask, render_template, request, redirect, url_for
from main import main, specific_travel_time
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/schedule-generator.html', methods=['GET', 'POST'])
def schedule_generator():
    if request.method == 'POST':
        min_credits = float(request.form.get('min_credits'))
        max_credits = float(request.form.get('max_credits'))
        num_desired_classes = int(request.form.get('num_scheds'))
        earliest_time = datetime.strptime(request.form.get('earliest_time'), '%H:%M').time()
        latest_time = datetime.strptime(request.form.get('latest_time'), '%H:%M').time()
        dorm_loc = request.form.get('dorm_loc')
        class_info = request.form.getlist('class_info')
        friday_off = request.form.getlist('prefer_fridays_off')
        sort_by = request.form.getlist('sort_by')
        
        all_info = main(class_info, dorm_loc, min_credits, max_credits, earliest_time, latest_time, num_desired_classes, friday_off, sort_by)  

        return render_template('schedule-generator.html', all_info=all_info)
    else:
        return render_template('schedule-generator.html', all_info=[])

@app.route('/travel-calculator.html', methods=['GET', 'POST'])
def travel_calculator():
    if request.method == 'POST':
        schedule = request.form.getlist('class_info')
        dorm_loc = request.form.get('dorm_loc')
        travel_time = specific_travel_time(dorm_loc, schedule)  
      
        return render_template('travel-calculator.html', travel_time=travel_time)
    else:
        return render_template('travel-calculator.html', travel_time=0)

if __name__ == '__main__':
    app.run(debug=True)
