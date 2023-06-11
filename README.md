# Movies Dataset

Analyzing movies data, including extracting information about title, release year, director, genres, and rating, as well as calculating various statistics such as average ratings and top-rated movies.

`movie_dataset` can perform the following operations:

1. Load the dataset from a CSV file.

2. Print the number of unique movies in the dataset.

3. Print the average rating of all the movies.

4. Print the top 5 highest rated movies.

5. Print the number of movies released each year.

6. Print the number of movies in each genre.

7. Save the dataset to a JSON file.

- [Data](#data)
  - [Full data](#fulldata)
  - [Sample data](#sampledata)
- [Installation](#installation)
- [Usage](#usage)
  - [MovieDataset](#moviedataset)
  - [DirectorExtractor](#directorextractor)
  - [GenreExtractor](#genreextractor)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Data

The dataset files are available in CSV format and can be downloaded from the following link:

[https://www.kaggle.com/rounakbanik/the-movies-dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)

### Full data files

Full data files downloaded from the above link are saved in the `data` directory

### Sample data files

Sample data files are used for exploration and testing:

- `ratings_small.csv` is located in `data`
- `sample_metadata.csv` and `sample_credits.csv` are located in the `data\sample_data` subdirectory.

## Installation

Download the repository

Download the data files from [https://www.kaggle.com/rounakbanik/the-movies-dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)

Place the data files within the `data` directory.

Install the required dependencies

```bash
pip install -r requirements.txt
```

Install the `movie_dataset` package

```bash
pip install .
```

## Usage

### MovieDataset

The `MovieDataset` class is used to load and analyze movie data from CSV files. It requires three CSV files as input: metadata, ratings, and credits.

Example usage:

```python
from movie_dataset import MovieDataset

metadata_file = "path/to/metadata.csv"
ratings_file = "path/to/ratings.csv"
credits_file = "path/to/credits.csv"
movies_json_file = "path/to/movies_dataset.json"

dataset = MovieDataset(metadata_file, ratings_file, credits_file)

print(f"Unique movies: {dataset.unique_movies():,}")
print(f"Average rating: {dataset.average_rating():.1f}")
print("Top 5 highest rated movies:")
print(dataset.top_rated_movies())
print("Number of movies released each year:")
print(dataset.movies_per_year())
print("Number of movies in each genre:")
print(dataset.movies_per_genre())
dataset.save_to_json(movies_json_file)
```

Example output

```
Unique movies: 2,830

Average rating: 3.3

Top 5 highest rated movies:
      id                     title release_year  rating
120  183                The Wizard         1989     5.0
215  301                 Rio Bravo         1959     5.0
221  309           The Celebration         1998     5.0
375  559              Spider-Man 3         2007     5.0
463  702  A Streetcar Named Desire         1951     5.0

Number of movies released each year:
release_year
1896     1
1900     3
1902     3
1903     1
1910     2
        ..
2011    97
2012    57
2013     8
2014     2
2015     2
Name: title, Length: 104, dtype: int64

Number of movies in each genre:
Drama              1535
Comedy              846
Thriller            683
Action              539
Romance             534
Crime               435
Adventure           357
Science Fiction     323
Horror              279
Fantasy             224
Mystery             216
Family              145
History             131
Documentary         106
Music               101
War                  87
Foreign              81
Animation            73
Western              60
TV Movie             23
Name: genre, dtype: int64
```

## Example movies_dataset,json

```
[{
"id":949,
"title":"Heat",
"release_year":"1995",
"director":"Michael Mann",
"genre":"Action",
"rating":3.6},

{
"id":949,
"title":"Heat",
"release_year":"1995",
"director":"Michael Mann",
"genre":"Crime",
"rating":3.6
},

...

{
"id":710,
"title":"GoldenEye",
"release_year":"1995",
"director":"Martin Campbell",
"genre":"Adventure",
"rating":1.5},

...

}]
```

### DirectorExtractor

The `DirectorExtractor` class is used to extract director information from a JSON string.

Example usage:

```python
from director_extractor import DirectorExtractor

extractor = DirectorExtractor()
crew_data = '[{"credit_id": "52fe4284c3a36847f8024f49", "department": "Directing", "gender": 2, "id": 7879, "job": "Director", "name": "John Lasseter", "profile_path": "/7EdqiNbr4FRjIhKHyPPdFfEEEFG.jpg"}]'
director = extractor.extract_director(crew_data)
print(director)  # Output: "John Lasseter"
```

### GenreExtractor

The `GenreExtractor` class is used to extract genre information from a JSON string.

Example usage:

```python
from genre_extractor import GenreExtractor

extractor = GenreExtractor()
sample_genre_data = '[{"id": 18, "name": "Drama"}, {"id": 35, "name": "Comedy"}, {"id": 10749, "name": "Romance"}]'
genres = extractor.extract_genre(sample_genre_data)
print(genres)  # Output: ['Drama', 'Comedy', 'Romance']
```

## Testing

To run the test suite, execute the following command:

```bash
python -m unittest discover
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your fork.
4. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
