from datetime import datetime

FORM_DATE_STRING = '%Y-%m-%d'


class Error(Exception):
    pass

# Met extra uitleg comments

def parse_form(form):
    """Parses the main pharmytweet form."""

    # Haal de naam uit het formulier, raise anders een error.
    if 'name' in form:
        name = form['name']
    else:
        raise Error

    # Haal "rangeOrAmountFrom" uit het formulier, raise anders een error.
    if 'rangeOrAmountFrom' in form:
        range_or_amount_from = form['rangeOrAmountFrom']
    else:
        raise Error

    # Haal de begindatum uit het formulier, raise anders een error.
    if 'begin_date' in form:
        # Probeer de begindatum te parsen naar een date type, raise anders een error.
        try:
            from_date = datetime.strptime(form['begin_date'], FORM_DATE_STRING)
        except ValueError:
            raise Error
    else:
        raise Error

    # Haal "show_tweets" uit het formulier, zet het anders op False.
    if 'show_tweets' in form:
        show_tweets = form['show_tweets']
    else:
        show_tweets = False

    # Probeer op basis van range_or_amount_from de datums te parsen naar een date type en return de resultaten, raise anders een error.
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
            return name, range_or_amount_from, from_date, amount, show_tweets
        else:
            raise Error
    else:
        raise Error
