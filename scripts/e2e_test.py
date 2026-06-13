import requests, json

def main():
    url = 'http://localhost:5000/events?city=Seattle'
    try:
        r = requests.get(url, timeout=10)
        print('status', r.status_code)
        try:
            data = r.json()
            print('count', data.get('count'))
            # print first 2 events
            for ev in data.get('events', [])[:2]:
                print(ev.get('name'), ev.get('date'), ev.get('venue'))
        except Exception as e:
            print('json error', e)
    except Exception as e:
        print('request error', e)

if __name__ == '__main__':
    main()
