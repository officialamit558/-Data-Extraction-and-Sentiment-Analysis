# Data-Extraction-and-Sentiment-Analysis

This repository contains code for extracting data from URLs and performing sentiment analysis on the extracted text. The analysis includes calculating various metrics such as sentiment scores, average sentence length, percentage of complex words, and more.

# Table of Contents
1) Installation
2) Usage
3) Data Extraction
4) Data Analysis
5) Output
# Installation
To run the code in this repository, you need to have Python installed along with the required libraries. You can install the necessary libraries using pip:
'''
pip install pandas beautifulsoup4 textblob nltk
'''
# Usage
1) Clone this repository to your local machine:
'''
git clone https://github.com/officialamit558/-Data-Extraction-and-Sentiment-Analysis.git
'''
2) Navigate to the cloned directory:
'''
cd -Data-Extraction-and-Sentiment-Analysis
'''
3) Run the Python script main.py:
'''
python main.py

'''
# Data Extraction

The script extracts data from a provided Excel file (Input.xlsx) containing URLs. It retrieves the HTML content from each URL, extracts the article title and text using BeautifulSoup, and saves the extracted text to separate text files.

# Data Analysis

After extracting the text, the script performs sentiment analysis using TextBlob. It calculates various metrics such as positive and negative scores, polarity score, subjectivity score, average sentence length, percentage of complex words, Fog index, average number of words per sentence, complex word count, word count, syllable per word, personal pronouns count, and average word length.

# Output
The analysis results are stored in a CSV file named output.csv. This file contains the calculated metrics for each URL along with their corresponding URL IDs.
