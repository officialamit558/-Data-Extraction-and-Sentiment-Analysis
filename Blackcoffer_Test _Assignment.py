
# # Import relevent Libraries

import pandas as pd
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
from nltk.corpus import cmudict
nltk.download('cmudict')

# # Data Extraction 

df = pd.read_excel('Input.xlsx')
df.shape
df['URL_ID'].unique()

for index, row in df.iterrows():
    url_id = row['URL_ID']
    
    url = row['URL']
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract article title and text
        
        article_title = soup.find('title').text
        article_text = ''
        
        article_elements = soup.select('article_element_selector')
        
        # Iterate through the selected elements and extract their text content
        for element in article_elements:
            article_text += element.get_text() + "\n"
        
        # Save article text to a text file
        with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(article_title + '\n')
            file.write(article_text)

# Read the extracted title_name and text 
            
article_text = file.read
article_text

print("URL_ID:", url_id )
print("Article Title:", article_title)
print('Artricle_text',article_text)

print(article_title , article_text )

# # Data Analysis

output_data = []

# List of personal pronouns
personal_pronouns = ['i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves']


def count_syllables(word):
    d = cmudict.dict()
    if word.lower() in d:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]])
    else:
        return 0

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    with open(f'{url_id}.txt', 'r', encoding='utf-8') as file:
        article_text = file.read()
        
        # Perform text analysis using TextBlob
        
        blob = TextBlob(article_text)
        
        # Calculate teh required variable
        
        sentences = blob.sentences
        words = blob.words
        sentiment = blob.sentiment
        
        positive_score = sentiment.polarity if sentiment.polarity > 0 else 0
        
        negative_score = -sentiment.polarity if sentiment.polarity < 0 else 0
        
        # Calculate Polarity Score and Subjectivity Score
        
        polarity_score = sentiment.polarity
        
        subjectivity_score = sentiment.subjectivity
        
        # Calculate Average Sentence Length
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Calculate Percentage of Complex Words
        
        complex_words = [word for word in words if len(word) > 2]
        percentage_complex_words = (len(complex_words) / len(words))*100
        
        # Calculate Fog Index
        
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
        
        # Calculate Average Number of Words Per Sentence
        
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Calculate Complex Word Count
        
        complex_word_count = len(complex_words)
        
        # Calculate Word Count
        
        word_count = len(words)
        
        # Calculate Syllable Per Word

        total_syllables = sum(count_syllables(word) for word in words)
        
        syllable_per_word = total_syllables / len(words)
        
        personal_pronouns_count = sum(1 for word in words if word.lower() in personal_pronouns)
        
        # Calculate Average Word Length
        
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        
        
        output_row = {
            'URL_ID': url_id,
            'URL': url,
            'Positive Score': positive_score,
            'Negative Score': negative_score,
            'Polarity Score': polarity_score,
            'Subjectivity Score': subjectivity_score,
            'AVG SENTENCE LENGTH': avg_sentence_length,
            'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
            'FOG INDEX': fog_index,
            'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
            'COMPLEX WORD COUNT': complex_word_count,
            'WORD COUNT': word_count,
            'SYLLABLE PER WORD': syllable_per_word,
            'PERSONAL PRONOUNS': personal_pronouns_count,
            'AVG WORD LENGTH': avg_word_length
        }
        
        output_data.append(output_row)


# # Store the output_data in csv file
# Convert output_data to a DataFrame
output_df = pd.DataFrame(output_data)

# Save the DataFrame as an Excel or CSV file
output_df.to_csv('output.csv', index=False) 

output_df = pd.read_csv('output.csv')
output_df.head()





