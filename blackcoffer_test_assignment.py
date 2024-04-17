
#Import necessary pacakages

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import re

# Read the Excel file into the pandas DataFrame
df = pd.read_excel('Input.xlsx')

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']

    # Make a request to the URL
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url_id}: {e}")
        continue

    # Create a BeautifulSoup object
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error creating BeautifulSoup object for {url_id}: {e}")
        continue

    # Find title
    try:
        title = soup.find('h1').get_text()
    except AttributeError:
        print(f"No title found for {url_id}")
        title = ""

    # Find text
    article = ""
    try:
        for p in soup.find_all('p'):
            article += p.get_text() + "\n"
    except Exception as e:
        print(f"Error getting text for {url_id}: {e}")

    # Write title and text to the file
    file_name = f'C:\\Users\\amit7\\Blackcoffer Assignment\\TitleText\\{url_id}.txt'
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(title + '\n' + article)
        print(f"File saved: {file_name}")
    except Exception as e:
        print(f"Error writing to file {file_name}: {e}")


# Set Directories
text_dir = r"C:\Users\amit7\Blackcoffer Assignment\TitleText"
stopwords_dir = r"C:\Users\amit7\Blackcoffer Assignment\StopWords"
sentment_dir = r"C:\Users\amit7\Blackcoffer Assignment\MasterDictionary"

# load all stop words from the stopwords directory and store in the set variable

stop_words = set()
for files in os.listdir(stopwords_dir):
  with open(os.path.join(stopwords_dir,files),'r',encoding='ISO-8859-1') as f:
    stop_words.update(set(f.read().splitlines()))

# load all text files  from the  directory and store in a list(docs)

docs = []
for text_file in os.listdir(text_dir):
  with open(os.path.join(text_dir,text_file),'r' , encoding='ISO-8859-1') as f:
    text = f.read()
#tokenize the given text file

    words = word_tokenize(text)

# remove the stop words from the tokens

    filtered_text = [word for word in words if word.lower() not in stop_words]

# add each filtered tokens of each file into a list
    docs.append(filtered_text)



# store positive, Negative words from the directory
pos=set()
neg=set()

for files in os.listdir(sentment_dir):
  if files =='positive-words.txt':
    with open(os.path.join(sentment_dir,files),'r',encoding='ISO-8859-1') as f:
      pos.update(f.read().splitlines())
  else:
    with open(os.path.join(sentment_dir,files),'r',encoding='ISO-8859-1') as f:
      neg.update(f.read().splitlines())

# now collect the positive  and negative words from each file
# calculate the scores from the positive and negative words 

positive_words = []
Negative_words =[]
positive_score = []
negative_score = []
polarity_score = []
subjectivity_score = []

#iterate through the list of docs

for i in range(len(docs)):
  positive_words.append([word for word in docs[i] if word.lower() in pos])
  Negative_words.append([word for word in docs[i] if word.lower() in neg])
  positive_score.append(len(positive_words[i]))
  negative_score.append(len(Negative_words[i]))
  polarity_score.append((positive_score[i] - negative_score[i]) / ((positive_score[i] + negative_score[i]) + 0.000001))
  subjectivity_score.append((positive_score[i] + negative_score[i]) / ((len(docs[i])) + 0.000001))


import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Directories
text_dir = r"C:\Users\amit7\Blackcoffer Assignment\TitleText"
stopwords_dir = r"C:\Users\amit7\Blackcoffer Assignment\StopWords"
sentiment_dir = r"C:\Users\amit7\Blackcoffer Assignment\MasterDictionary"


# Initialize lists to store calculated metrics
avg_sentence_length = []
Percentage_of_Complex_words = []
Fog_Index = []
complex_word_count = []
avg_syllable_word_count = []

# Load all stop words from the stopwords directory and store in the set variable

stop_words_set = set(stopwords.words('english'))

def measure(file):
    with open(os.path.join(text_dir, file), 'r', encoding='ISO-8859-1') as f:
        text = f.read()
        # Remove punctuations 
        text = re.sub(r'[^\w\s.]', '', text)
        # Split the given text file into sentences
        sentences = text.split('.')
        # Total number of sentences in a file
        num_sentences = len(sentences)
        # Total words in the file
        words = [word for word in word_tokenize(text) if word.lower() not in stop_words_set]
        num_words = len(words)

        # Complex words having syllable count greater than 2
        # Complex words are words in the text that contain more than two syllables.
        complex_words = [word for word in words if len(re.findall(r'[aeiouAEIOU]+', word)) > 2]

        # Syllable Count Per Word
        # We count the number of syllables in each word of the text by counting the vowels present in each word.
        # We also handle some exceptions like words ending with "es", "ed" by not counting them as a syllable.

        syllable_count = sum(len(re.findall(r'[aeiouAEIOU]+', word)) for word in words)
        syllable_words = [word for word in words if not word.endswith(('es', 'ed'))]

        avg_sentence_len = num_words / num_sentences
        avg_syllable_word_count = syllable_count / len(syllable_words)
        Percent_Complex_words = len(complex_words) / num_words
        Fog_Index = 0.4 * (avg_sentence_len + Percent_Complex_words)

        return avg_sentence_len, Percent_Complex_words, Fog_Index, len(complex_words), avg_syllable_word_count

# Iterate through each file or doc
for file in os.listdir(text_dir):
    x, y, z, a, b = measure(file)
    avg_sentence_length.append(x)
    Percentage_of_Complex_words.append(y)
    Fog_Index.append(z)
    complex_word_count.append(a)
    avg_syllable_word_count.append(b)

# Word Count and Average Word Length Sum of the total number of characters in each word/Total number of words
# We count the total cleaned words present in the text by 
# removing the stop words (using stopwords class of nltk package).
# removing any punctuations like ? ! , . from the word before counting.

import os
import re
from nltk.corpus import stopwords

# Directories
text_dir = r"C:\Users\amit7\Blackcoffer Assignment\TitleText"
stopwords_dir = r"C:\Users\amit7\Blackcoffer Assignment\StopWords"

# Load stopwords from NLTK corpus
stop_words = set(stopwords.words('english'))

# Word Count and Average Word Length: Sum of the total number of characters in each word/Total number of words
def cleaned_words(file):
    with open(os.path.join(text_dir, file), 'r' , encoding='ISO-8859-1') as f:
        text = f.read()
        text = re.sub(r'[^\w\s]', '', text)
        words = [word for word in text.split() if word.lower() not in stop_words]
        length = sum(len(word) for word in words)
        average_word_length = length / len(words)
    return len(words), average_word_length

word_count = []
average_word_length = []

for file in os.listdir(text_dir):
    x, y = cleaned_words(file)
    word_count.append(x)
    average_word_length.append(y)


# Count Personal Pronouns mentioned in the text
def count_personal_pronouns(file):
    with open(os.path.join(text_dir, file), 'r' , encoding='ISO-8859-1') as f:
        text = f.read()
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        count = 0
        for pronoun in personal_pronouns:
            count += len(re.findall(r"\b" + pronoun + r"\b", text))  # \b is used to match word boundaries
    return count

pp_count = []

for file in os.listdir(text_dir):
    x = count_personal_pronouns(file)
    pp_count.append(x)


# Time for merge the all feature in Output Data Structure
output_store = pd.read_excel('Output Data Structure.xlsx')

# Drop the two rows like 35 and 48 which produced 404 error

output_store.drop(index=[35,48] ,  inplace=True)

variables = [positive_score,
            negative_score,
            polarity_score,
            subjectivity_score,
            avg_sentence_length,
            Percentage_of_Complex_words,
            Fog_Index,
            avg_sentence_length,
            complex_word_count,
            word_count,
            avg_syllable_word_count,
            pp_count,
            average_word_length]

# write the values to the dataframe

for i, var in enumerate(variables):
  output_store.iloc[:,i+2] = var

#Now save the dataframe to the disk
output_store.to_csv('Output_Data.csv')

output = pd.read_csv('Output_Data.csv')
output.head()