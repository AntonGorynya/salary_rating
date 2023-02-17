def predict_average_salary(salaries):
    sum = 0
    count = 0
    for salary in salaries:
        if salary:
            sum += salary
            count += 1
    return round(sum/count, 2)


def predict_salary(payment_from, payment_to):
    if payment_from and payment_to:
        return (payment_from + payment_to)/2
    if payment_from:
        return payment_from * 1.2
    if payment_to:
        return payment_to * 0.8
    return None
