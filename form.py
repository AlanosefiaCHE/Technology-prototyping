from datetime import datetime
from multiprocessing.sharedctypes import Value

FORM_DATE_STRING = '%Y-%m-%d'


# Add more detailed errors
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

    if 'begin_date' in form:
        try:
            from_date = datetime.strptime(form['begin_date'], FORM_DATE_STRING)
        except ValueError:
            raise Error
    else:
        raise Error

    if 'show_tweets' in form:
        show_tweets = form['show_tweets']
    else:
        show_tweets = False

    if range_or_amount_from == 'range':
        if 'end_date' in form:
            try:
                until_date = datetime.strptime(
                    form['end_date'],
                    FORM_DATE_STRING)
            except ValueError:
                raise Error
            return name, range_or_amount_from, from_date, until_date, show_tweets
        else:
            raise Error
    elif range_or_amount_from == 'amountFrom':
        if 'amount' in form:
            amount = form['amount']
            return name, range_or_amount_from, amount, show_tweets
        else:
            raise Error
    else:
        raise Error
