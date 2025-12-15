from flask import Flask, render_template, request
import calendar
from config import PEOPLE, POSTS
from scheduler import generate_schedule

app = Flask(__name__)


@app.context_processor
def inject_globals():
    return dict(
        posts=POSTS,
        people=PEOPLE
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    schedule = None
    people_data = None
    month = int(request.form.get('month', 1))
    year = int(request.form.get('year', 2025))

    _, num_days = calendar.monthrange(year, month)
    days = list(range(1, num_days + 1))

    if request.method == 'POST':
        people_data = {}

        for p in PEOPLE:
            pref = request.form.get(f'post_{p}', 'Нет предпочтения')
            blocked = [d for d in days if request.form.get(f'block_{p}_{d}')]

            people_data[p] = {
                'pref': pref,
                'blocked': blocked
            }

        schedule = generate_schedule(people_data, POSTS, days)

    return render_template(
        'index.html',
        days=days,
        schedule=schedule,
        month=month,
        year=year,
        people_data=people_data  # ← важно для сохранения выбранных предпочтений
    )

if __name__ == '__main__':
    app.run(debug=True)
