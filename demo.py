
from flask import Flask, request, jsonify, Response,render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/flaskapp'
CORS(app)
db = SQLAlchemy(app)


# the class Movie will inherit the db.Model of SQLAlchemy
class Movie(db.Model):
    __tablename__ = 'movies'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    # nullable is false so the column can't be empty
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
       
       
    def json(self):
        return {'id': self.id, 'title': self.title,
                'year': self.year, 'genre': self.genre}
        # this method we are defining will convert our output to json

    def add_movie(_title, _year, _genre):
        '''function to add movie to database using _title, _year, _genre
        as parameters'''
        # creating an instance of our Movie constructor
     
        new_movie = Movie(title=_title, year=_year, genre=_genre)
        db_data = db.session.add(new_movie)
        print(db_data)  # add new movie to database session
        db.session.commit()  # commit changes to session
        return new_movie.id

    def get_all_movies():
        '''function to get all movies in our database'''
        return [Movie.json(movie) for movie in Movie.query.all()]

    def get_movie(_id):
        '''function to get movie using the id of the movie as parameter'''
        return [Movie.json(Movie.query.filter_by(id=_id).first())]
        # Movie.json() coverts our output to the json format defined earlier
        # the filter_by method filters the query by the id
        # since our id is unique we will only get one result
        # the .first() method will get that first value returned


    def update_movie(_id, _title, _year, _genre):
        '''function to update the details of a movie using the id, title,
        year and genre as parameters'''
        movie_to_update = Movie.query.filter_by(id=_id).first()
        movie_to_update.title = _title
        movie_to_update.year = _year
        movie_to_update.genre = _genre
        db.session.commit()
    def delete_movie(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Movie.query.filter_by(id=_id).delete()
        # filter movie by id and delete
        db.session.commit()  # commiting the new change to our database
db.create_all()

# route to get all movies

    


# route to get all movies
@app.route('/movies', methods=['GET'])

def get_movies():
    '''Function to get all the movies in the database'''
    return jsonify({'Movies': Movie.get_all_movies()})
    
# route to get movie by ids
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie_by_id(id):
    return_value = Movie.get_movie(id)
    return jsonify(return_value)
# route to add new movie
@app.route('/postmovies', methods=['POST'])
# route to add new movie
@app.route('/movies', methods=['POST'])
def add_movie():
    '''Function to add new movie to our database'''
    request_data = request.get_json()  # getting data from client
    movie_id = Movie.add_movie(request_data["title"], request_data["year"],
                    request_data["genre"])
    data = Movie.get_movie(movie_id)
    result = {
        "status": "success",
        "code": 201,
        "results": data,
        "msg": "Added Successfully"
    }
    return jsonify(result)
# route to update movie with PUT method
@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    '''Function to edit movie in our database using movie id'''
    request_data = request.get_json()
    Movie.update_movie(id, request_data['title'], request_data['year'],request_data['genre'])
    response = Response("Movie Updated", status=200, mimetype='application/json')
    return response
# route to delete movie using the DELETE method
@app.route('/movies/<int:id>', methods=['DELETE'])
def remove_movie(id):
    '''Function to delete movie from our database'''
    Movie.delete_movie(id)
    response = Response("Movie Deleted", status=200, mimetype='application/json')
    return response

if __name__ == "__main__":
    app.run(debug=True)