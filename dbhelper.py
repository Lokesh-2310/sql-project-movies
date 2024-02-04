import mysql.connector
class MyDatabase:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="movies_project"
            )
        except Exception as e:
            print("Can't able to connect with the database")
        else:
            print('Connected successfully')
            self.mycursor=self.conn.cursor()

    def get_genre(self):
        self.mycursor.execute("""
            SELECT DISTINCT Genre FROM movies;
        """)
        data=self.mycursor.fetchall()
        genres=[]
        temp = []
        for i in data:
            temp.append(i[0])
        genres = []
        for i in temp:
            for j in (i.split(',')):
                genres.append(j.strip())

        return list(set(genres))

    def get_movie_list_by_genre(self,options):
        l = options
        if len(l) == 0:
            pass
        elif len(l) == 1:
            self.mycursor.execute("""SELECT Series_Title,Genre,Runtime FROM movies WHERE Genre LIKE '%{0}%';
            """.format(l[0]))
            data = self.mycursor.fetchall()
            movie_name = []
            genre = []
            runtime = []
            for i in data:
                movie_name.append(i[0])
                genre.append(i[1])
                runtime.append(i[2])

            list_name_genre = []
            for i in genre:
                name_genre = []
                for j in i.split(","):
                    for k in l:
                        if j.strip() == k.strip():
                            name_genre.append(j.strip())
                            continue
                list_name_genre.append(",".join(name_genre))

            return movie_name, list_name_genre, runtime

        elif len(l) == 2:
            self.mycursor.execute("""
            SELECT Series_Title,Genre,Runtime FROM (
            SELECT * FROM movies WHERE Genre LIKE '%{}%'
            UNION
            SELECT * FROM movies WHERE Genre LIKE '%{}%' ) t
            ORDER BY Series_Title;
            """.format(l[0], l[1]))
            data = self.mycursor.fetchall()
            movie_name = []
            genre = []
            runtime = []
            for i in data:
                movie_name.append(i[0])
                genre.append(i[1])
                runtime.append(i[2])
            list_name_genre = []
            for i in genre:
                name_genre = []
                for j in i.split(","):
                    for k in l:
                        if j.strip() == k.strip():
                            name_genre.append(j.strip())
                            continue
                list_name_genre.append(",".join(name_genre))

            return movie_name, list_name_genre, runtime
        else:
            self.mycursor.execute("""
            SELECT Series_Title,Genre,Runtime FROM (
            SELECT * FROM movies WHERE Genre LIKE '%{}%'
            UNION
            SELECT * FROM movies WHERE Genre LIKE '%{}%'
            UNION
            SELECT * FROM movies WHERE Genre LIKE '%{}%'
            ) t
            ORDER BY Series_Title;
            """.format(l[0], l[1], l[2]))
            data = self.mycursor.fetchall()
            movie_name = []
            genre = []
            runtime = []
            for i in data:
                movie_name.append(i[0])
                genre.append(i[1])
                runtime.append(i[2])
            list_name_genre = []
            for i in genre:
                name_genre = []
                for j in i.split(","):
                    for k in l:
                        if j.strip() == k.strip():
                            name_genre.append(j.strip())
                            continue
                list_name_genre.append(",".join(name_genre))

            return movie_name, list_name_genre, runtime

    def get_year(self):
        self.mycursor.execute("""
        SELECT DISTINCT Released_Year from movies ORDER BY Released_Year DESC;
        """)
        data=self.mycursor.fetchall()
        year_list = []
        for i in data:
            year_list.append(i[0])
        return year_list

    def get_year_genre_movie(self,genre,year):
        self.mycursor.execute(f"""
        SELECT Series_Title,Runtime FROM movies WHERE Genre LIKE "%{genre}%" AND Released_Year={year};
        """)
        data=self.mycursor.fetchall()
        name = []
        time=[]
        for i in data:
            name.append(i[0])
            time.append(i[1])
        return name,time

    def top_genre_movies(self,genre):
        self.mycursor.execute("""
        SELECT Series_Title,Released_Year ,Meta_score,No_of_Votes,Gross FROM movies WHERE Genre LIKE '%{}%';
        """.format(genre))
        data=self.mycursor.fetchall()
        name = []
        year = []
        score = []
        votes = []
        gross = []
        for i in data:
            name.append(i[0])
            year.append(i[1])
            score.append(i[2])
            votes.append(i[3])
            gross.append(i[4])
        return name,year,score,votes,gross

    def overall_top_movies(self):
        self.mycursor.execute("""SELECT Poster_Link,Series_Title,Released_Year ,Meta_score,No_of_Votes,Gross FROM movies;""")
        data = self.mycursor.fetchall()
        poster = []
        name = []
        year = []
        score = []
        votes = []
        gross = []
        for i in data:
            poster.append(i[0])
            name.append(i[1])
            year.append(i[2])
            score.append(i[3])
            votes.append(i[4])
            gross.append(i[5])

        return poster,name,year,score,votes,gross

    def movie_by_year(self,year):
        self.mycursor.execute("""
        SELECT Series_Title,Meta_score,Genre FROM movies Where Released_Year={}
        """.format(year))
        data=self.mycursor.fetchall()
        name = []
        score = []
        genre = []
        for i in data:
            name.append(i[0])
            score.append(i[1])
            genre.append(i[2])

        return name,score,genre


    def director_name(self):
        self.mycursor.execute("""
               SELECT DISTINCT Director FROM movies;
               """)
        data = self.mycursor.fetchall()

        dir_name=[]
        for i in data:
            dir_name.append(i[0])

        return sorted(dir_name)


    def get_movies_by_director_name(self,dirname):
        self.mycursor.execute("""
                       SELECT Series_Title,Released_Year,Runtime,Meta_score FROM movies WHERE Director="{}";
                       """.format(dirname))
        data = self.mycursor.fetchall()

        name = []
        year=[]
        time=[]
        score=[]
        for i in data:
            name.append(i[0])
            year.append(i[1])
            time.append(i[2])
            score.append(i[3])

        return name,year,time,score

    def top_director_movies(self):
        self.mycursor.execute(""" 
        WITH top_director as (
        SELECT Director FROM movies 
        GROUP BY Director
        HAVING COUNT(*) >5 AND AVG(Meta_score)>80
        )
        SELECT Series_Title,Released_Year,Runtime,Director FROM movies WHERE Director IN (
        SELECT * FROM top_director
        ) """)

        data=self.mycursor.fetchall()
        name = []
        year = []
        time = []
        dir=[]
        for i in data:
            name.append(i[0])
            year.append(i[1])
            time.append(i[2])
            dir.append(i[3])

        return name, year, time,dir