from bs4 import BeautifulSoup, NavigableString
from dataclasses import dataclass
import concurrent.futures as cf
import regex as re
import requests
import time


@dataclass
class pInfo:
    rating: float
    price: float
    bm_index: int
    rating_qty: int
    title: str


def inp(ques, ans=None, int_only=False, yn=False, rep_msg=None, rep=False, no_ans=False):
    if ans:
        ans = [an.lower() for an in ans]
    if rep:
        print(rep_msg)
    res = input(ques).lower()
    if no_ans and not res:
        return False
    if int_only:
        try:
            return str(int(res))
        except:
            inp(ques, int_only=True, rep_msg=rep_msg, rep=True)
    return res if not yn and not ans or yn and res in ['yes', 'no'] or ans and res in ans else inp(ques, ans=ans, yn=yn,
                                                                                                   rep_msg=rep_msg,
                                                                                                   rep=True,
                                                                                                   no_ans=no_ans)


def fan_input():
    print('\n-----[INPUT SECTION]-----')
    brand = inp('Would you like a specific brand of fan (input nothing if you are indifferent)? ', no_ans=True)
    type_ = inp('What kind of fan would you like (table, handheld, tower, box, ceiling)? ',
                ans=['table', 'handheld', 'tower', 'box', 'ceiling'], rep_msg='Please enter a valid input.')
    star_min = inp('What is the minimum average star rating you would purchase a fan with (1-4): ',
                   ans=['1', '2', '3', '4', '5'], rep_msg='Please enter a number from 1 to 4.')
    rev_min = inp(
        'What is the minimum amount of reviews you would purchase a fan with (input nothing if you are indifferent)? ',
        int_only=True, rep_msg='Please enter a number.', no_ans=True)
    allow_used = inp('Are you okay with purchasing used and refurbished products? ', yn=True,
                     rep_msg='Please enter either yes or no.')
    return brand, type_, star_min, rev_min, allow_used


def scrape(brand, type_, star_min, rev_min, allow_used):
    start = time.perf_counter()
    print('\n-----[SCRAPING]-----\n>>> Sending request to eBay...')
    condurl = '&rt=nc&LH_ItemCondition=1000' if allow_used == 'yes' else '&rt=nc' if allow_used == 'no' else False
    if not condurl:
        raise Exception
    markup = requests.get(
        url=f'https://www.ebay.com/sch/i.html?_nkw={brand}+{type_}+fan{condurl}&_sop=12&rt=nc&LH_BIN=1').content
    soup = BeautifulSoup(markup, 'html.parser')
    print('>>> Parsing page for hyperlinks...')
    links = [link.a.get('href') for link in [soup.select('li.s-item')][0]]
    items = []
    print('>>> Loading product pages to be scraped...')
    with cf.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url=link) for link in links]
    for i in zip(futures, [n for n in range(len(links))]):
        if (i[1] + 1) % 25 == 0 or i[1] == 0:
            print(f'>>> Scraping products {i[1] + 1}-{min([i[1] + 25, len(links)])} (of {len(links)} products)...')
        markup = i[0].result().content
        soup = BeautifulSoup(markup, 'html.parser')
        if soup.find(id="prcIsum"):
            if soup.find(class_='reviews-star-rating') and int(
                    ''.join([c for c in soup.find(class_='review-ratings-cntr').attrs['aria-label'][15:] if
                             c in '1234567890'])) > 0:
                if int(
                        ''.join([c for c in soup.find(class_='review-ratings-cntr').attrs['aria-label'][15:] if
                                 c in '1234567890'])) < int(rev_min) or float(
                    soup.find(class_="reviews-star-rating").attrs['title'][:3]) < int(star_min):
                    items.append(False)
                else:
                    items.append(pInfo(float(soup.find(class_="reviews-star-rating").attrs['title'][:3]),
                                       float(soup.find(id="prcIsum").attrs['content']), i[1], int(''.join(
                            [c for c in soup.find(class_='review-ratings-cntr').attrs['aria-label'][15:] if
                             c in '1234567890'])), soup.find('meta', attrs={'name': 'twitter:title'}).attrs['content']))
            elif int(star_min) or int(rev_min):
                items.append(False)
            else:
                items.append(pInfo(0, float(soup.find(id="prcIsum").attrs['content']), i[1], 0,
                                   soup.find('meta', attrs={'name': 'twitter:title'}).attrs['content']))
        else:
            items.append(False)
    print(f'>>> Filtering processes completed in {round(time.perf_counter() - start, 2)} seconds.')
    item_links = list(zip(items, links))
    for index in [ind for ind, il in enumerate(item_links) if False in il][::-1]:
        del item_links[index]
    return item_links


def main():
    a, b, c, d, e = fan_input()
    items = scrape(a, b, c, d, e)
    res = min(
        [int(inp('\n-----[RESULTS]-----\nHow many results would you like (see the top "x" results )? ', int_only=True,
                 rep_msg='Please enter a number')), len(items)])
    print(f'• Top {res} results sorted by best match : ')
    for itm in sorted(items, key=lambda itm: itm[0].bm_index)[:res]:
        print(f'    ◦ ITEM NAME : {itm[0].title}, LINK : {itm[1]}')
    print(f'• Top {res} results sorted by rating : ')
    for itm in sorted(items, key=lambda itm: itm[0].rating, reverse=True)[:res]:
        print(f'    ◦ ITEM NAME : {itm[0].title}, RATING : {itm[0].rating}/5.0, LINK : {itm[1]}')
    print(f'• Top {res} results sorted by price : ')
    for itm in sorted(items, key=lambda itm: itm[0].price)[:res]:
        print(f'    ◦ ITEM NAME : {itm[0].title}, RATING : ${itm[0].price}, LINK : {itm[1]}')


if __name__ == '__main__':
    main()
