import lxml.html
import requests
import pandas as pd


def extract_movie_from_imdb(url):
    # fake a browser agent even though it is not required for IMDB
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
               'accept-language': 'en-GB,en;q=0.9,en-US'}

    response = requests.get(url, headers=headers)
    root = lxml.html.fromstring(response.content.decode('utf-8'))

    movie_list = []
    movies = root.xpath("//tbody[@class='lister-list']/tr")
    for movie in movies:
        movie_name = movie.xpath(".//td[@class='titleColumn']/a/text()")[0].replace(",", " ")
        movie_year = movie.xpath(".//td[@class='titleColumn']/span/text()")[0].strip("()")
        movie_rating = movie.xpath(".//td[@class='ratingColumn imdbRating']/strong/text()")[0]

        movie_list.append({
            "movie_name": movie_name,
            "movie_year": movie_year,
            "movie_rating": movie_rating
        })

    movie_df = pd.DataFrame(movie_list)
    movie_df.to_csv("./imdb_top_movie.csv", index=False)


if __name__ == "__main__":
    extract_movie_from_imdb(url="https://www.imdb.com/chart/top/?ref_=nv_mv_250")
