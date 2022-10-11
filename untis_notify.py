import requests, json
from datetime import datetime, timedelta
from time import sleep

def get_config() -> dict:
    try:
        with open("config.json", "r") as f:
            data = json.loads(f.read())
            return data
    except:
        with open("config.json", "w+") as f:
            data = {"class_id": 69420,
                    "webhook": "https://www.discordwebhookgoeshere.com",
                    "cookie": "schoolname cookie goes here"}

            f.write(json.dumps(data))

        input("please fill out your config.json file\nPress ENTER to exit")
        exit()


def get_data(class_id: int, cookie: str) -> dict:
    headers = {"Host": "kephiso.webuntis.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5",
               "Accept-Encoding": "gzip, deflate, br",
               "Connection": "keep-alive",
               "Upgrade-Insecure-Requests": "1",
               "Sec-Fetch-Dest": "document",
               "Sec-Fetch-Mode": "navigate",
               "Sec-Fetch-Site": "none",
               "Sec-Fetch-User": "?1"}

    cookies = {"schoolname": cookie}
    # much security, very wow
    # just the school name encoded in base64
    # example: "_BASE64ENCODEDSTRING"

    now = datetime.now()
    
    while now.weekday() > 4:
        now += timedelta(days=1)

    f_date = now.strftime("%Y-%m-%d")
    c_bypass = str(datetime.timestamp(now)).replace(".", "")
    # "bypassing" their chaching system might not even work and is quite possibly super unnecessary ¯\_(ツ)_/¯

    data = None

    try:
        r = requests.get(f"https://kephiso.webuntis.com/WebUntis/api/public/timetable/weekly/data?elementType=1&elementId={class_id}&date={f_date}&formatId=4&_={c_bypass}",
                        headers=headers,
                        cookies=cookies)

        if r.status_code == 200:
            data = r.json()
        else:
            #todo
            pass
    
    finally:
        return data


def main():
    config = get_config()
    print(config)

    current_data = None

    while True:
        latest_data = get_data(config["class_id"], config["cookie"])

        if latest_data == None:
            # this shouldn't really happen but it might.
            # todo: implement logging for this specific case
            sleep(900)
            continue

        if current_data == None:
            current_data = latest_data
            sleep(900)
            continue

        if current_data["data"]["result"]["timestamp"] == latest_data["data"]["result"]["timestamp"]:
            # no new updates
            sleep(900)
            continue


if __name__ == "__main__":
    main()

