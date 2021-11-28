from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

def index(request):
    return HttpResponse("Olá mundo! Este é o app notes de Tecnologias Web do Insper.")


@api_view(['GET'])
def api_driverStandings(request):
    #download f1 page
    f1Page = 'https://www.formula1.com/en.html'
    result = requests.get(f1Page)
    result.content

    # if successful parse the download into a BeautifulSoup object, which allows easy manipulation 
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")

    # find the object with HTML class wikitable sortable
    #print(soup)
    #const firstPlace = document.querySelector('.f1-podium--position.pos--1.d-none.d-md-inline-block')
    #const driverClass = firstPlace.querySelector('.driver-image')
    #const pictureFirstPlace = driverClass.querySelector('.lazy').getAttribute('data-src')
    classDriver1 = soup.find('a',{'class':'f1-podium--position pos--1 d-none d-md-inline-block'})
    classDriver1Img = classDriver1.find('picture',{'class':'driver-image'})
    pictureFirstPlace = classDriver1Img.find('img', {'class':'lazy'})['data-src']
    linkFirstPlaceImg = "https://www.formula1.com" + pictureFirstPlace 

    #---------------------------------------------------------------------------------------------

    classDriver2 = soup.find('a',{'class':'f1-podium--position pos--2 d-none d-md-inline-block'})
    classDriver2Img = classDriver2.find('picture',{'class':'driver-image'})
    pictureSecondPlace = classDriver2Img.find('img', {'class':'lazy'})['data-src']
    linkSecondPlaceImg = "https://www.formula1.com" + pictureSecondPlace

    #----------------------------------------------------------------------------------------------

    classDriver3 = soup.find('a',{'class':'f1-podium--position pos--3 d-none d-md-inline-block'})
    classDriver3Img = classDriver3.find('picture',{'class':'driver-image'})
    pictureThirdPlace = classDriver3Img.find('img', {'class':'lazy'})['data-src']
    linkThirdPlaceImg = "https://www.formula1.com" + pictureThirdPlace

    dictLinks = {"First":linkFirstPlaceImg, "Second": linkSecondPlaceImg, "Third":linkThirdPlaceImg}

    # jsonFrase = json.dumps(dictLinks, ensure_ascii=False)
    # print("ESSE É O DICT: ", jsonFrase)
    return JsonResponse(dictLinks)

@api_view(['GET'])
def api_constructorStandings(request):
    f1PageConstruc = 'https://www.formula1.com/en.html#constructors'
    result2 = requests.get(f1PageConstruc)
    result2.content

# if successful parse the download into a BeautifulSoup object, which allows easy manipulation 
    if result2.status_code == 200:
        soup2 = BeautifulSoup(result2.content, "html.parser")

    classConstruc1 = soup2.find('div',{'class':'f1-podium--top-positions constructors'})
    classPos1 = classConstruc1.find('a', {'class':'f1-podium--position pos--1 d-none d-md-inline-block'})
    classLogo1 = classPos1.find('img', {'class': 'lazy'})['data-src']
    LogoImg1 = "https://www.formula1.com" + classLogo1

    classCar = classPos1.find('picture', {'class': 'car-image'})
    classCarImg = classCar.find('img', {'class': 'lazy'})['data-src']
    linkCarImg1 = "https://www.formula1.com" + classCarImg

    listaConstruc1 = [LogoImg1,linkCarImg1]

    #-------------------------------------------------------------------------------------

    classConstruc2 = soup2.find('div',{'class':'f1-podium--top-positions constructors'})
    classPos2 = classConstruc2.find('a', {'class':'f1-podium--position pos--2 d-none d-md-inline-block'})
    classLogo2 = classPos2.find('img', {'class': 'lazy'})['data-src']
    LogoImg2 = "https://www.formula1.com" + classLogo2

    classCar2 = classPos2.find('picture', {'class': 'car-image'})
    classCarImg2 = classCar2.find('img', {'class': 'lazy'})['data-src']
    linkCarImg2 = "https://www.formula1.com" + classCarImg2

    listaConstruc2 = [LogoImg2,linkCarImg2]

    #---------------------------------------------------------------------------------------

    classConstruc3 = soup2.find('div',{'class':'f1-podium--top-positions constructors'})
    classPos3 = classConstruc3.find('a', {'class':'f1-podium--position pos--3 d-none d-md-inline-block'})
    classLogo3 = classPos3.find('img', {'class': 'lazy'})['data-src']
    LogoImg3 = "https://www.formula1.com" + classLogo3

    classCar3 = classPos3.find('picture', {'class': 'car-image'})
    classCarImg3 = classCar3.find('img', {'class': 'lazy'})['data-src']
    linkCarImg3 = "https://www.formula1.com" + classCarImg3

    listaConstruc3 = [LogoImg3,linkCarImg3]

    dictTeams = {"First": listaConstruc1, "Second": listaConstruc2, "Third": listaConstruc3}

    return JsonResponse(dictTeams)

@api_view(['GET'])        
def api_teamInfo(request, team):
    teamURL = f'https://www.formula1.com/en/teams/{team}.html'
    result = requests.get(teamURL)
    if result.status_code == 200:
        teamDic = {}
        driverNames = []
        driverNums = []
        driverImagesURL = []
        driverDic = {}
        statsDic = {}
        teamLogoURL = "https://www.formula1.com"
        
        soup = BeautifulSoup(result.content, "html.parser")
        teamInfo = soup.find('header', {'class':'team-details'})
        stats = teamInfo.find('tbody')

        teamLogoURL += teamInfo.find('img',{'class':'cq-dd-image'})['src']
        
        driverImages = teamInfo.find_all('div',{'class':'driver-image-crop-inner'})
        for image in driverImages:
            driverImagesURL.append("https://www.formula1.com"+image.find('img')['src'])
        for num in teamInfo.findAll('div', {'class': 'driver-number'}):
            driverNums.append(num.find('span').decode_contents())
        for name in teamInfo.findAll('h1', {'class':'driver-name'}):
            driverNames.append(name.decode_contents())
        for i in range(len(driverNames)):
            driverDic[f'driver{i}'] = {}
            driverDic[f'driver{i}']['name'] = driverNames[i]
            driverDic[f'driver{i}']['number'] = driverNums[i]  
            driverDic[f'driver{i}']['imageURL'] = driverImagesURL[i]          

        statsKeys = stats.find_all('span')
        statsValues = stats.find_all('td',{'class':'stat-value'})
        for i in range(len(statsKeys)):
            statsDic[statsKeys[i].decode_contents()] = statsValues[i].decode_contents()
        
        teamDic['drivers'] = driverDic
        teamDic['stats'] = statsDic
        teamDic['teamLogo'] = teamLogoURL 
        return JsonResponse(teamDic)

    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })