from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Category, Ingredient
from .forms import NewItemForm
from django.db.models import Q
from collections import Counter
from .forms import ComparisonForm,NewItemForm



def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    ingredients = item.ingredients.all()

    return render(request, 'item/detail.html', {
        'item': item,
        'ingredients': ingredients,
    })
@login_required
def create_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect('item:detail', pk=item.pk)  # Redirect to a detail view or another appropriate view
    else:
        form = NewItemForm()
    return render(request, 'item/form.html', {'form': form, 'title': 'Create New Item'})

def browse(request):
    query = request.GET.get('query','')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter()
    if category_id:
        items = items.filter(category=category_id)
    if query:
        items = items.filter(Q(name__icontains=query)|Q(brands__icontains=query))
    return render(request, 'item/browse.html',  {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),})

def compare_items(request):
    if request.method == 'POST':
        form = ComparisonForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']
            item1 = form.cleaned_data['item1']
            item2 = form.cleaned_data['item2']

            # Get the ingredients for each item and count the safety levels
            item1_ingredients = item1.ingredients.all()
            item2_ingredients = item2.ingredients.all()
            item1_counts = Counter(ingredient.safety for ingredient in item1_ingredients)
            item2_counts = Counter(ingredient.safety for ingredient in item2_ingredients)

            return render(request, 'item/comparison_page.html', {
                'category': category,
                'item1': item1,
                'item2': item2,
                'item1_safe_count': item1_counts['S'],
                'item1_risky_count': item1_counts['R'],
                'item2_safe_count': item2_counts['S'],
                'item2_risky_count': item2_counts['R'],})
    else:
        form = ComparisonForm()
    return render(request, 'item/compare_items.html', {'form': form})

def comparison_page(request, item_id1, item_id2):
    # Retrieve the items from the database
    item1 = get_object_or_404(Item, pk=item_id1)
    item2 = get_object_or_404(Item, pk=item_id2)

    # Count the number of risky and safe ingredients for each item
    item1_ingredients = item1.ingredient_set.values_list('safety', flat=True)
    item2_ingredients = item2.ingredient_set.values_list('safety', flat=True)
    item1_risky_count = item1_ingredients.count('R')
    item2_risky_count = item2_ingredients.count('R')
    item1_safe_count = item1_ingredients.count('S')
    item2_safe_count = item2_ingredients.count('S')

    return render(request, 'item/comparison_page.html', {
        'item1': item1,
        'item2': item2,
        'item1_safe_count': item1_safe_count,
        'item1_risky_count': item1_risky_count,
        'item2_safe_count': item2_safe_count,
        'item2_risky_count': item2_risky_count,
    })