import numpy as np
import pandas as pd

def generate_dummy_employee_data(employee_id):
    # Generate dummy data for an employee with three values for Productivity:
    # One less than 5, exactly 5, and one more than 5
    productivity_values = [3, 5, 8]
    teamwork = np.random.uniform(1, 10, size=3)

    data = {
        'Employee_ID': [employee_id] * 3,
        'Productivity': productivity_values,
        'Teamwork': teamwork
    }

    employee_data = pd.DataFrame(data)
    return employee_data, ['Productivity', 'Teamwork']
