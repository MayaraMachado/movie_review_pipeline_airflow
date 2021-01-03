import os
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import datetime


def scraping_avaliacao_adoro_cinema(page = 1):
    URL = f"http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/?page={page}"
    
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []

    for dataBox in soup.find_all("div", class_="data_box"):
        titleObj = dataBox.find("a", class_="no_underline")
        imgObj = dataBox.find(class_="img_side_content").find_all(class_="acLnk")[0]
        sinopseObj = dataBox.find("div", class_="content").find_all("p")[0]
        dateObj = dataBox.find("div", class_="content").find("div", class_="oflow_a")
        movieLinkObj = dataBox.find(class_="img_side_content").find_all("a")[0]
        generoObj = dataBox.find("div", class_="content").find_all('li')[3].find('div',class_="oflow_a")
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']
       
        avaliacoesMeios = dataBox.find("div", class_="margin_10v").find_all('span', class_="acLnk")
        avaliacoesNotas = dataBox.find("div", class_="margin_10v").find_all('span', class_="note")

        # tratar a lista de avaliações
        avaliadores = [ elem.text.strip() for elem in avaliacoesMeios if elem.text.strip() != "" ]
        
        # vincular com notas
        avaliacoesValores = {"AdoroCinema" : None, "Leitores" : None, "Imprensa" : None}
        for index, avaliador in enumerate(avaliadores):
          avaliacoesValores[avaliador] = avaliacoesNotas[index].text.strip()     

        #Carregar a sinopse completa 
        htmldocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="content-txt")     
        fullImgObj = soupMovieDetail.find("meta",  property="og:image")   

        data.append({'titulo': titleObj.text.strip(),
                    'genero': generoObj.text.replace('\n','').strip(),
                    'poster' : fullImgObj["content"], 
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dateObj.text[0:11].strip(),
                    'link' : detailsLink,
                    'avaliacoes' : avaliacoesValores,
                    'sinopseFull': fullSinopse.text})
                
    return data

def write_csv(data, filepath='./dags/temp/'):

    filename = 'adorocinema_'+ datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.csv'
    filepath = filepath+filename 
    keys = data[0].keys()
    with open( filepath, 'w+', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        
def collect_adoro_cinema_data(quantidade_paginas):
    data =  []
    for i in range (0, quantidade_paginas):
        data += scraping_avaliacao_adoro_cinema(i)

    write_csv(data)
