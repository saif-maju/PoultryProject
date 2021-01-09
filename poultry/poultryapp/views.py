from django.shortcuts import render
from django.http import HttpResponse
from .scrapper import DataScrapper
from .models import Product
from django.db.models import Count, Avg
from django.views import generic
from .graph import barChart, violinChart, histChart
from django.http import JsonResponse

def index(request):
    # ds = DataScrapper()
    # ds.scrap_data()()
    # prices = list(Product.objects.filter(category='chicken').values_list('price',flat=True))
    # prices = list(filter(lambda x:x<1000,prices))
    # price_img = histChart(prices,'Chicken Price Distribution','Price','Count')
    count = Product.objects.all().count()
    cat_count = Product.objects.values('category').annotate(count=Count('name')).order_by('-count')
    categories = [d['category'] for d in cat_count]
    count = [d['count'] for d in cat_count]
    data = {}
    for i in range(len(categories)):
        data[categories[i]] = count[i]
    
    return render(request,"home.html",{'count':count,'data':data})
    # return render(request,"home.html")


def categories(request):

    cat_count = Product.objects.values('category').annotate(count=Count('name')).order_by('-count')
    categories = [d['category'] for d in cat_count]
    count = [d['count'] for d in cat_count]
    category_count = barChart(categories,count,'Products in Categories','Category','Count')


    cat_avg = Product.objects.values('category').annotate(avg=Avg('price')) .order_by('-avg')  
    categories = [d['category'] for d in cat_avg]   
    avgs = [d['avg'] for d in cat_avg]
    category_avg = barChart(categories,avgs,'Average Price of Category','Category','Average Price')

    prices = list(Product.objects.filter(category='chicken').values_list('price',flat=True))
    # prices = list(filter(lambda x:x<1000,prices))
    chicken_price_img = histChart(prices,'Chicken Price Distribution','Price','Count')

    prices = list(Product.objects.filter(category='beef').values_list('price',flat=True))
    # prices = list(filter(lambda x:x<1000,prices))
    beef_price_img = histChart(prices,'Beef Price Distribution','Price','Count')

    prices = list(Product.objects.filter(category='fish').values_list('price',flat=True))
    # prices = list(filter(lambda x:x<1000,prices))
    fish_price_img = histChart(prices,'Fish Price Distribution','Price','Count')

    context = {'category_count':category_count,'category_avg':category_avg,'chicken':chicken_price_img,'beef':beef_price_img,'fish':fish_price_img}
    return render(request,"categories.html",context)

def brands(request):
    brands = list(Product.objects.values_list('brand',flat=True).distinct())
    print(brands)
    return render(request,"brands.html",{'brands':brands})

def scrap(request):
    brand = request.GET.get('brand_name', None)
    m = globals()['DataScrapper']()
    func = getattr(m, brand)
    func()
    num = Product.objects.filter(brand=brand).count()
    print(num)
    data = {
            'num': num
            }
    return JsonResponse(data)

class ProductListView(generic.ListView):
    model = Product
    template_name = "products.html"    
