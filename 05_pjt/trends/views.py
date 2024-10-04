from django.shortcuts import render, redirect
from .models import Trend, Keyword
from bs4 import BeautifulSoup
from selenium import webdriver
from .forms import KeywordForm
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
# Create your views here.
import matplotlib as mpl

# 폰트 설정
mpl.rc('font', family='Malgun Gothic')

# 키워드 생성
def keyword(request):
    keywords = Keyword.objects.all()
    if request.method == "POST":
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trends:keyword')
    else:
        form = KeywordForm()
    context = {
        'form' : form,
        'keywords' : keywords,
    }
    return render(request, 'trends/keyword.html', context)

# 키워드 삭제
def keyword_detail(request, pk):
    article = Keyword.objects.get(pk=pk)
    article.delete()
    return redirect('trends:keyword')

# 크롤링 수행 및 크롤링.html 렌더링
def crawling(request):
    keywords = Keyword.objects.all()
    for keyword in keywords:
        keyword = keyword.name
        if Trend.objects.filter(name=f"{keyword}", search_period="all"):
            keyword = Trend.objects.get(name=f"{keyword}", search_period="all")
            keyword.result += 1
            keyword.save()
            print('중복으로 결과를 추가합니다.')
            continue
        url = f'https://www.google.com/search?q={keyword}'
        driver = webdriver.Chrome()
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        result_stats = soup.select_one("div#result-stats")
        result =''
        for r in result_stats.text:
            if r.isdecimal():
                result += r
            elif r == "개":
                break
        result = int(result)
        Trend.objects.create(name=keyword, result=result, search_period="all")
    trends = Trend.objects.filter(search_period="all")
    context = {
        'trends' : trends,
    }
    return render(request, 'trends/crawling.html', context)


def crawling_histogram(request):
    results = Trend.objects.filter(search_period = "all")
    names = []
    values = []
    x = np.arange(len(results))
    for result in results:
        names.append(result.name)
        values.append(result.result)
    plt.clf()
    plt.bar(x, values)
    plt.xticks(x, names)
    plt.title('Keyword Search Result')
    plt.xlabel('Keyword')
    plt.ylabel('Result')

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    context = {
        'results' : results,
        'image' : f"data:image/png;base64, {image_base64}"
    }
    return render(request, 'trends/crawling_histogram.html', context)

def crawling_advanced(request):
    
    keywords = Keyword.objects.all()
    for keyword in keywords:
        keyword = keyword.name
        if Trend.objects.filter(name=f"{keyword}", search_period='year'):
            keyword = Trend.objects.get(name=f"{keyword}", search_period="year")
            keyword.result += 1
            keyword.save()
            continue

        url = f"https://www.google.com/search?q={keyword}&sca_esv=8a14761ebfeca0aa&sxsrf=ADLYWIJB-ppj3Q4oW6WSIVJR2wgGUWUvKg:1728023310192&source=lnt&tbs=qdr:y&sa=X&ved=2ahUKEwjR8sS8jPSIAxUodfUHHSx9AEkQpwV6BAgCEAs&biw=1161&bih=950&dpr=1"
        driver = webdriver.Chrome()
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        result_stats = soup.select_one("div#result-stats")
        result =''
        for r in result_stats.text:
            if r.isdecimal():
                result += r
            elif r == "개":
                break
        result = int(result)
        Trend.objects.create(name=keyword, result=result, search_period="year")
    results = Trend.objects.filter(search_period="year")
    # 이미지 생성
    names = []
    values = []
    x = np.arange(len(results))
    for result in results:
        names.append(result.name)
        values.append(result.result)
    plt.clf()
    plt.bar(x, values)
    plt.xticks(x, names)
    plt.title('Keyword Search Result')
    plt.xlabel('Keyword')
    plt.ylabel('Result')

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    context = {
        'image' : f"data:image/png;base64, {image_base64}"
    }
    return render(request, 'trends/crawling_advanced.html', context)

