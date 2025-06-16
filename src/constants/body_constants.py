headers = {
        'Links' : 'movieId,imdbId,tmdbId',
        'Movies' : 'movieId,title,genres',
        'Ratings' : 'userId,movieId,rating,timestamp',
        'Tags' : 'userId,movieId,tag,timestamp'
    }

columns = {
    'Links' : ['movieId','imdbId','tmdbId'],
    'Movies' : ['movieId','title','genres'],
    'Ratings' : ['userId','movieId','rating','timestamp'],
    'Tags' : ['userId','movieId','tag','timestamp']
}

body_types = {
    'Links' : ['int', 'int', 'int'],
    'Movies' : ['int', 'str', 'str'],
    'Ratings' : ['int', 'int', 'float', 'int'],
    'Tags' : ['int', 'int', 'str', 'int']
}
