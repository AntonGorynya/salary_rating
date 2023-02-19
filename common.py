def predict_salary(payment_from, payment_to):
    if payment_from and payment_to:
        return (payment_from + payment_to)/2
    if payment_from:
        return payment_from * 1.2
    if payment_to:
        return payment_to * 0.8
    return None


def predict_average_salary(salaries):
    vacancies_processed = len(salaries)
    average_salary = 'No information'
    if vacancies_processed:
        average_salary = round(sum(salaries) / vacancies_processed, 2)
    return vacancies_processed, average_salary
