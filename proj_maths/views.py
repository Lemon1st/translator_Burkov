from django.shortcuts import render
from django.core.cache import cache
from . import terms_work
from . import terms_db


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_db.db_get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    cache.clear()
    if request.method == "POST":
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Перевод должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Введенное слово должно быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш перевод принят"
            terms_db.db_write_term(new_term, new_definition, user_name)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    stats = terms_db.db_get_term_stats()
    return render(request, "stats.html", stats)


def show_translator(request):
    cache.clear()
    if request.method == "POST":
        requested = request.POST.get("txt")
        lang = request.POST.get("lang")
        translation = ''
        context = {"user": "пользователь"}
        if lang == 'en':
            translation = terms_db.db_find_translation_engtorus(requested)
            if translation is None:
                context["success"] = False
                context["comment"] = "Слова нет в словаре!"
                return render(request, "term_request.html", context)
        if lang == 'rus':
            translation = terms_db.db_find_translation_rustoeng(requested)
            if translation is None:
                context["success"] = False
                context["comment"] = "Слова нет в словаре!"
                return render(request, "term_request.html", context)
        return render(request, "Translator_window.html", {"result": translation, "start": requested, "language_start": lang})
    else:
        return render(request, "Translator_window.html")
