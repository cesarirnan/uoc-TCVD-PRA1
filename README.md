# Práctica 1: Web scraping

## Descripción

Esta práctica se ha realizado bajo el contexto de la asignatura Tipología y ciclo de vida de los datos, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de web scraping mediante el lenguaje de programación Python para extraer así datos de la web, específicamente de Amazon y generar un dataset con información actual de la categoría FUNKO POP, a esto se complementó con datos historicos de las ventas de estos articulos en el año 2020.

## Miembros del equipo

La actividad ha sido realizada de manera coordinada por César Irnán Sillero y Lissette Muñoz Guillén.

## Ficheros del código fuente

La práctica se compone de los siguientes ficheros:
  - main.py: Fichero del código fuente donde se ha desarrollado el scrape de la web de amazon para recuperar los id y demás información de los artículos y las llamadas a la API para obtener el histórico de precios
  - search_results_output.jsonl: Json de resultados, cada uno en una línea, de cada producto
  - search_results_urls: Listado de urls a analizar
  - search_results.yml: Archivo de configuración para montar los json de salida y los elementos a buscar dentro del html de la consulta web

## Recursos

Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
Mitchel, R. (2015). Web Scraping with Python: Collecting Data from the Modern Web. O'Reilly Media, Inc. Chapter 1. Your First Web Scraper.
