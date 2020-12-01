import lxml.html
import requests
import pandas as pd


def remove_special_chars(something):
    return "".join(something.split())


def extract_repositories_from_github(url):
    # fake a browser agent even though it is not required for IMDB
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
               'accept-language': 'en-GB,en;q=0.9,en-US'}

    response = requests.get(url, headers=headers)
    root = lxml.html.fromstring(response.content.decode('utf-8'))

    repositories_list = []
    repositories = root.xpath("//article[@class='Box-row']")
    for repository in repositories:
        name = remove_special_chars(repository.xpath(".//h1/a")[0].text_content())
        language = repository.xpath(".//span[@itemprop='programmingLanguage']/text()")
        language = "unspecified" if language is None or len(language) == 0 else language[0]
        stars = remove_special_chars(repository.xpath(".//div/a[@class='muted-link d-inline-block mr-3']")[0].text_content()).replace(",", "")
        forks = remove_special_chars(repository.xpath(".//div/a[@class='muted-link d-inline-block mr-3']")[1].text_content()).replace(",", "")

        repositories_list.append({
            "repository_name": name,
            "programming_language": language,
            "stars": stars,
            "forks": forks
        })

    repository_df = pd.DataFrame(repositories_list)
    repository_df.to_csv("./recent_popular_repository.csv", index=False)


if __name__ == "__main__":
    extract_repositories_from_github(url="https://github.com/trending")
