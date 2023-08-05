# legaltechtools

![Platform](https://img.shields.io/badge/platform-python-green.svg?style=flat&logo=appveyor)

*An open source library that can be used to scrape and perform data analysis on legal tech companies*


## Contents

1. [About](#about)
2. [Installation](#installation)
3. [Authors](#authors)

## About

The library consists of two different classes, one intended for scraping and one intended for data analysis.

#### Scraping

The scraping class can be used obtain information on legal tech companies including  company urls, social media urls, and the subsets of legal-tech that a particular company falls into.
Additionally, existing information can be verified by calling `ScrapingTools.verify_url()`

#### Data Analysis

The data analysis class can be used to uncover insights about data that has already been collected. Some of the metrics that can be found include determining the distribution of companies by country, the average success of a legal-tech company in a particular region, countries where new legal-tech companies are being founded, and the number of legal-tech companies founded per year. 

## Installation

The library can easily be installed via pip:

`pip install legaltechtools`

## Authors

This library was written by Neel Kandlikar, Neeraj Rattehalli, and David Fletcher under the mentorship of Dr. Pieter Gunst. 

