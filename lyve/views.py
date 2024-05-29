from django.shortcuts import render
from item.models import Category, Item, Ingredient


def home(request):
    return render(request, "lyve/home.html")

def about(request):
    return render(request, "lyve/about.html")

def labeling(request):
    return render(request, "lyve/labeling.html")
def products(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    categorized_items = {category: [] for category in categories}
    for item in items:
        categorized_items[item.category].append(item)

    return render(request, "lyve/products.html",{
        'categories': categories,
        'items': items,
        'categorized_items': categorized_items,
    })

from django.core.paginator import Paginator


def ingredients(request):
    ingredient_list = Ingredient.objects.all()

    # Paginate the ingredient list
    paginator = Paginator(ingredient_list, 100)  # Show 5 ingredients per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "lyve/ingredients.html", {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),  # Pass if the list is paginated
        'ingredients': page_obj.object_list,  # Pass the ingredients for the current page
    })


def ingredients_view(request, letter=None):
    if letter:
        ingredients = Ingredient.objects.filter(name__istartswith=letter.upper())
    else:
        ingredients = Ingredient.objects.all()

    return render(request, 'lyve/ingredients.html',
            {'ingredients': ingredients, 'letter': letter
             })


def compare(request):
    return render(request, "lyve/compare.html")

def skintype(request):
    return render(request, "lyve/skintype.html")

def skincareroutine(request):
        return render(request, "lyve/skincareroutine.html")
