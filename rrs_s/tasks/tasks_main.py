import xml.etree.ElementTree as et
import requests

url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCgaIawRRpTlFJnXJ1HZ4trg'


def get_data(url=url):
    root = et.fromstring(requests.get(url).content.decode('utf-8'))
    exp_data = []

    for page in root.findall('{http://www.w3.org/2005/Atom}entry'):
        data = {
            'link': 'https://www.youtube.com/watch?v=' + page.find('{http://www.w3.org/2005/Atom}id').text.replace('yt:video:', ''),
            'title': page.find('{http://www.w3.org/2005/Atom}title').text,
            'desc': page.find('{http://search.yahoo.com/mrss/}group').find('{http://search.yahoo.com/mrss/}description').text,
            'published': page.find('{http://www.w3.org/2005/Atom}published').text, }
        exp_data.append(data)

    return exp_data


