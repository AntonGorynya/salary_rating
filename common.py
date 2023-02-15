def predict_average_salary(salaries):
    sum = 0
    count = 0
    for salary in salaries:
        if salary:
            sum += salary
            count += 1
    return round(sum/count, 2)
