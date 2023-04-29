from dbconnect.models import Terms, Termauthors


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


def db_write_term(new_term, new_definition):
    term = Terms(term=new_term.lower(), definition=new_definition.lower())
    term.save()
    term_addition = Termauthors(termid=term.termid, termsource='user')
    term_addition.save()


def db_get_term_stats():
    db_terms = len(Termauthors.objects.filter(termsource='db'))
    user_terms = len(Termauthors.objects.filter(termsource='user'))
    terms = Terms.objects.all()
    defin_len = [len(term.definition) for term in terms]
    stats = {
        'terms_all': db_terms + user_terms,
        'terms_own': db_terms,
        'terms_added': user_terms,
        'words_avg': sum(defin_len) / len(defin_len),
        'words_max': max(defin_len),
        'words_min': min(defin_len)
    }
    return stats
