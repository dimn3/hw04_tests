def year(request):
    import datetime
    return {
        'year': datetime.date.today().year
    }
