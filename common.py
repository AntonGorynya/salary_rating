def predict_salary(payment_from, payment_to):
    if payment_from and payment_to:
        return (payment_from + payment_to)/2
    if payment_from:
        return payment_from * 1.2
    if payment_to:
        return payment_to * 0.8
    return None
