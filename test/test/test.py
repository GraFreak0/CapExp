from datetime import datetime, timedelta

today = datetime.today()
first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d")
last_day_last_month = today.replace(day=1) - timedelta(days=1)
last_day_last_month = last_day_last_month.strftime("%Y-%m-%d")

print(first_day_last_month)
print(last_day_last_month)