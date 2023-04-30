from dbconnect.models import Terms, Termauthors
from datetime import datetime, timedelta
from django.db.models import Count
from django.conf import settings
from django.utils.timezone import make_aware

def db_get_terms_for_table():
    terms = []
    for i, item in enumerate(Terms.objects.all()):
        terms.append([i + 1, item.term.capitalize(), item.definition.capitalize()])
    return terms


def db_find_translation_rustoeng(requested):
    item = Terms.objects.filter(term__iexact=str(requested).lower()).first()
    if item is None:
        return None
    else:
        return item.definition.capitalize()


def db_find_translation_engtorus(requested):
    item = Terms.objects.filter(definition__iexact=str(requested).lower()).first()
    if item is None:
        return None
    else:
        return item.term.capitalize()


def db_write_term(new_term, new_definition, author):
    term = Terms(term=new_term.lower(), definition=new_definition.lower())
    term.save()
    term_addition = Termauthors(termid=term.termid, termsource='user', termauthor=author)
    term_addition.save()


def db_get_term_stats():
    db_terms = len(Termauthors.objects.filter(termsource='db'))
    user_terms = len(Termauthors.objects.filter(termsource='user'))
    last_7_days_terms = len(Termauthors.objects.filter(termdate__gte=make_aware(datetime.now()) - timedelta(days=7)))
    last_1_days_terms = len(Termauthors.objects.filter(termdate__gte=make_aware(datetime.now()) - timedelta(days=1)))
    last_1_hour_terms = len(Termauthors.objects.filter(termdate__gte=make_aware(datetime.now()) - timedelta(hours=1)))
    most_popular = Termauthors.objects.values_list('termauthor').annotate(author_count=Count('termauthor')).order_by('-author_count').first()[0]
    most_amount = Termauthors.objects.values_list('termauthor').annotate(author_count=Count('termauthor')).order_by('-author_count').first()[1]
    print(last_7_days_terms)
    stats = {
        'terms_all': db_terms + user_terms,
        'terms_own': db_terms,
        'terms_added': user_terms,
        'terms_last_7_days': last_7_days_terms,
        'terms_last_1_days': last_1_days_terms,
        'terms_last_1_hour': last_1_hour_terms,
        'most_popular_author': most_popular,
        'most_popular_amount': most_amount
    }
    return stats
