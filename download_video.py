import requests,time
from threading import Thread


class web_info(object):
    def __init__(self,url,headers):
        self.url = url
        self.headers = headers

    def get_m3u8_web_url(self,video_file):
        try:
            m3u8_list = []
            m3u8_data = requests.get(self.url,self.headers).text.split('\n')
            print(len(m3u8_data),m3u8_data)
            for i in m3u8_data:
                if '.ts' in i:
                    i = i.split('/')[-1]
                    m3u8_list.append(i)

            for ts in m3u8_list:
                web_url = self.url.replace(self.url.split('/')[-1],ts)
                web_info.download(self,web_url,video_file)

        except Exception as e:
            print(e)

    def download(self,web_url,video_file):
        try:
            video_data = requests.get(web_url,self.headers,timeout = 120)
            #print('开始下载')
            with open(video_file,mode='ab') as f:
                for content in video_data.iter_content(10240):
                    f.write(content)
            print('下载 %s 完成' %(web_url))
        except Exception as e:
            print(e)


def app_master(url,headers):
    start_list = []
    for u in url:
        web_info_list = web_info(u,headers)
        time.sleep(1)
        video_file = str(time.time()).replace('.', '_') + '.ts'
        print(video_file)
        t = Thread(target=web_info_list.get_m3u8_web_url, args=(video_file,))
        start_list.append(t)
    for t in start_list:
        t.start()
    for t in start_list:
        t.join()


if __name__ == '__main__':

    headers = {
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.3"
    }

    url = [
'm3u8_url'
        ]


    app_master(url,headers)









