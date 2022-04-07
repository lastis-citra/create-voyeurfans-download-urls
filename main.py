import requests
from bs4 import BeautifulSoup


# safedl.netはリダイレクトが入るので，リダイレクト先のURLを知りたい
def get_safedl_redirect_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    a_tags = soup.select('a')
    for a in a_tags:
        url = a['href']
        print(url)


# 検索結果ページから次の検索結果ページを取得する
def get_next_page(soup):
    a_tags = soup.select('a[rel=next]')

    if len(a_tags) > 0:
        a = a_tags[0]
        url = a['href']
        # print(url)
        return f'https://voyeurfans.net/forum/{url}'
    else:
        return None


# 検索結果ページを取得する
def get_search_result_urls(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')

    a_tags = soup.select('blockquote a')
    for a in a_tags:
        url = a['href']
        if 'safedl.net' in url or 'ul.to' in url:
            if 'safedl.net' in url:
                get_safedl_redirect_url(url)
            else:
                print(url)
    next_url = get_next_page(soup)
    # print(next_url)

    # 次のページが存在するなら，再帰的に実行
    if next_url is not None:
        get_search_result_urls(next_url)


if __name__ == '__main__':
    file_name = './input_url_list.txt'
    with open(file_name, 'r', errors='replace', encoding="utf_8") as file:
        line_list = file.readlines()

    line_count = 0

    for line in line_list:
        line_count += 1
        input_url = line.split(',')[0]
        print(line_count, '/', len(line_list))
        # print('input_url: ' + input_url)
        get_search_result_urls(input_url)
