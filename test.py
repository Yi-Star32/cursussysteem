from datetime import datetime

vb_string = '2025-05-18 12:00'
vb_datetime = datetime.strptime(vb_string, '%Y-%m-%d %H:%M')  # Converteer naar datetime-object

print(type(vb_datetime))  # Output: 2025-05-18 12:00:00
