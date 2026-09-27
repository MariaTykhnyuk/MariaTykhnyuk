from django.shortcuts import render, redirect
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Страница «{title}» не найдена."
        })

    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()

    for entry_name in entries:
        if entry_name.lower() == query.lower():
            return redirect("entry", title=entry_name)

    results = []

    for entry_name in entries:
        if query.lower() in entry_name.lower():
            results.append(entry_name)

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results
    })


def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title:
            return render(request, "encyclopedia/new_page.html", {
                "error": "Введите название страницы.",
                "title": title,
                "content": content
            })

        if not content:
            return render(request, "encyclopedia/new_page.html", {
                "error": "Введите содержание страницы.",
                "title": title,
                "content": content
            })

        entries = util.list_entries()

        for entry_name in entries:
            if entry_name.lower() == title.lower():
                return render(request, "encyclopedia/new_page.html", {
                    "error": f"Страница «{title}» уже существует.",
                    "title": title,
                    "content": content
                })

        util.save_entry(title, content)

        return redirect("entry", title=title)

    return render(request, "encyclopedia/new_page.html")


def edit_page(request, title):
    current_content = util.get_entry(title)

    if current_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Страница «{title}» не найдена."
        })

    if request.method == "POST":
        new_content = request.POST.get("content", "").strip()

        if not new_content:
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "content": new_content,
                "error": "Содержание страницы не может быть пустым."
            })

        util.save_entry(title, new_content)

        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": current_content
    })


def random_page(request):
    entries = util.list_entries()

    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "В энциклопедии пока нет страниц."
        })

    title = random.choice(entries)

    return redirect("entry", title=title)

