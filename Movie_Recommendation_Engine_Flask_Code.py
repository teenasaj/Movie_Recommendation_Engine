from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('page1.html')

#Defining the funtion 
def recommend(title):
    import pandas as pd
    #from rake_nltk import Rake
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import CountVectorizer
    
    df = pd.read_csv('C:\\Users\\91965\\Documents\\BDA SEM II\\Multivariate Statistics\\Python Project II\\movie_data_final.csv')
    
    df = df[['Title','Genre','Director','Actors','Language']]
    df.head()
    
    # discarding the commas between the actors' full names and getting only the first three names
    df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
    
    # putting the genres in a list of words
    df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))
    
    df['Director'] = df['Director'].map(lambda x: x.split(' '))
    
    # merging together first and last name for each actor and director, so it's considered as one word 
    # and there is no mix up between people sharing a first name
    for index, row in df.iterrows():
        row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]
        row['Director'] = ''.join(row['Director']).lower()
    
    df.set_index('Title', inplace = True)
    df.head()    
    df['bag_of_words'] = ''
    columns = df.columns
    for index, row in df.iterrows():
        words = ''
        for col in columns:
            if col != 'Director':
                words = words + ' '.join(row[col])+ ' '
            else:
                words = words + row[col]+ ' '
        row['bag_of_words'] = words
        
    df.drop(columns = [col for col in df.columns if col!= 'bag_of_words'], inplace = True)
    
    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])
    
    # creating a Series for the movie titles so they are associated to an ordered numerical
    # list I will use later to match the indexes
    indices = pd.Series(df.index)
    indices[:5]
    
    
    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    cosine_sim
    
    recommended_movies = []
    
    # gettin the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i])
        
    return recommended_movies
    #function done and recommended movies will be returned


#for calling the defined function
@app.route('/recommend')
def my_form():
	return render_template('page2.html')

@app.route('/recommend',methods=['POST'])
def my_form_post():
	usermovie=request.form['um']
	movie_list=recommend(usermovie)
	return movie_list
#calling ends and output processed

@app.route('/output',methods=['POST','GET'])
def output():
	x=my_form_post()
	return render_template('page3.html',x=x)
#for calling the about the app page
@app.route('/about')
def about():
	return render_template('page4.html')

if __name__ == '__main__':
	app.run(debug=True)
