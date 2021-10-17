import requests, time, traceback

while True:
    try:
        requests.post('https://api.vk.com/method/wall.createComment?v=5.103&access_token=' +
        token + '&lang=ru',
        data = {'owner_id': -174105461, 'post_id': 6713149, 'message': 'Ферма'})
        time.sleep(14500)
    except:
        print(f'Ошибка!\n\n{traceback.format_exc()}')
        time.sleep(10)
        
        
