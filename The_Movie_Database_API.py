import pandas as pd
from pprint import pprint
import requests
low_memory=False


# Read csv file 
csv_file = 'Resources/recentMovieTitles.csv'
movie_titles = pd.read_csv(csv_file)



movie_titles['genres'].value_counts()


# In[ ]:


# Get The Movie Database IDs For Each Movie
#movie_ids = []
movie_JSON = []
totalNumMovies = len(movie_titles)
setRequestCounter = 1
readCurrentIndexFile = open("Resources/currentIndex.txt", "r")
requestIndexCounter = int(readCurrentIndexFile.read())
foundCounter = 0
notFoundCounter = 0

while requestIndexCounter <= totalNumMovies:
    if setRequestCounter <= 500:
        if setRequestCounter == 100:
            print("SET: 100/500")
        elif setRequestCounter == 200:
            print("SET: 200/500")
        elif setRequestCounter == 300:
            print("SET: 300/500")
        elif setRequestCounter == 400:
            print("SET: 400/500")
        title = movie_titles['primaryTitle'].iloc[requestIndexCounter]
        year = movie_titles['startYear'].iloc[requestIndexCounter]
        i_url = f"https://api.themoviedb.org/3/search/movie?api_key=c1c6e406a72fd9e2c34c45bf23702c82&query={title}&year={year}"
        i_request = requests.get(i_url)
        i_requestJSON = i_request.json()
        #print(request)
        if i_request.status_code == 200:
            if i_requestJSON['total_results'] != 0:
                movie_id = i_requestJSON['results'][0]['id']
                m_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c1c6e406a72fd9e2c34c45bf23702c82&append_to_response=credits"
                m_request = requests.get(m_url)
                if m_request.status_code == 200:
                    m_requestJSON = m_request.json()
                    movie_JSON.append(m_requestJSON)
                    foundCounter += 1
                    print(f"FOUND: {title}")
                else:
                    print(f"FAILED ID LOOKUP: {m_request} - {m_url}") 
            else:
                notFoundCounter += 1
                print(f"NOT FOUND: {title}")
        else:
        	print(f"FAILED MOVIE LOOKUP: {i_request} - {i_url}")           

        requestIndexCounter += 1
        setRequestCounter += 1
    else:
        #movie_ids_df = pd.DataFrame(movie_ids)
        #movie_ids_df.to_csv('Resources/TMDBMovieIDS.csv', mode='a', header=False, index=False)
        writeCurrentIndexFile = open("Resources/currentIndex.txt", "w")
        writeCurrentIndexFile.write(str(requestIndexCounter))
        writeCurrentIndexFile.close()
        movie_json_df = pd.DataFrame(movie_JSON)
        movie_json_df.to_csv('Resources/TMDBMovieJSON.csv', mode='a', header=False, index=False)
        print(f"""--- SAVING PROGRESS TO CSV ---
        SET: {setRequestCounter-1}/500 | TOTAL: {requestIndexCounter}/{totalNumMovies}
        Found: {foundCounter}/{(foundCounter+notFoundCounter)} ({round(foundCounter/(foundCounter+notFoundCounter)*100,2)}%)
        """)
        foundCounter = 0
        notFoundCounter = 0
        setRequestCounter = 1
        movie_JSON = []
        #movie_ids = []


#PROCESS COMPLETE                                                                              
print('''---------------------------
DATA RETRIEVAL PROCESS COMPLETE!
---------------------------''')
