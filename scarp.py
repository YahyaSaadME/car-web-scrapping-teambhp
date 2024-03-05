
from bs4 import BeautifulSoup
import json
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
def scrap():
    link = input("Enter link:")
    file = input("Enter filename:")
    s = requests.Session()
    soup= BeautifulSoup(s.get(link).text, 'html.parser')
    page = soup.find("div",class_="pagenav").find("td",class_="vbmenu_control").text
    page = int(page[page.find("of")+2:])

    with open(f'./nissan/{file}.json', 'w') as json_file:
        data = {"datas":[]}
        json.dump(data,json_file)

    link = link[:link.index(".html")]
    print("1 of "+str(page)+" pages")
    for i in range(1,int(page)+1):
        try:
            print("i:",i)
            soup= BeautifulSoup(s.get(f"{link}-{i}.html").text, 'html.parser')
            all = soup.find("div",id="posts").find_all("div",style="margin: 0 auto")
            for one in all:
                trs = one.find_next("div").find_next("div").find_next("div").find_next("table",class_="mod2022-radius-all")
                posts = []
                for i in  trs.find_all("div"):
                    if i.get("id"):
                        posts.append(i)
                
                time = trs.find_all("tr")[0].find("td").text.split(",")[-1]
                time = time.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","")
                date = trs.find_all("tr")[0].find("td").text.split(",")[0]
                date = date.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","")
                print(date)
                name = trs.find_all("tr")[1].find("td").find("div").text
                name = name.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","")
                brand = trs.find_all("tr")[1].find("td").find_all("div")[1].text
                brand = brand.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","")
                extra = trs.find_all("tr")[1].find("td").find_all("div")[2].text.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","")
                if extra.replace(" ","") == "":
                    extra = trs.find_all("tr")[1].find("td").find_all("div")[3].text.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","")
                    if extra.replace(" ","") == "":
                        extra = trs.find_all("tr")[1].find("td").find_all("div")[4].text.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","")
                parts = extra.split()
                info_dict = {
                    'Location': parts[parts.index("Location:")+1],
                    'Posts': parts[parts.index("Posts:")+1],
                    'Thanked': parts[parts.index("Thanked:")+1]
                }
                with open(f'./nissan/{file}.json', 'r') as json_file:
                    data = json.load(json_file)
                    with open(f'./nissan/{file}.json', 'w') as json_file:
                        data['datas'].append({"name":name,"time":time,"brand":brand,"extra":info_dict,"post":posts[-1].text,"date":date})
                        json.dump(data, json_file, indent=4) 
                        print("Added")
        except Exception as e:
            print("skipped")