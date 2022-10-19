from datetime import datetime

FORM_DATE_STRING = '%Y-%m-%d'


class Error(Exception):
    pass


def parse_form(form):
    """Parses the main pharmytweet form."""

    if 'name' in form:
        name = form['name']
    else:
        raise Error

    if 'rangeOrAmountFrom' in form:
        range_or_amount_from = form['rangeOrAmountFrom']
    else:
        raise Error

    if 'from' in form:
        try:
            from_date = datetime.strptime(form['from'], FORM_DATE_STRING)
        except ValueError:
            raise Error
    else:
        raise Error

    if range_or_amount_from == 'range':
        if 'until' in form:
            until_date = datetime.strptime(form['until'], FORM_DATE_STRING)
            return name, range_or_amount_from, from_date, until_date
        else:
            raise Error
    elif range_or_amount_from == 'amountFrom':
        if 'amount' in form:
            amount = form['amount']
            return name, range_or_amount_from, amount
        else:
            raise Error
    else:
        raise Error
