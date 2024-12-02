#1. url para generar el token
#https://business.facebook.com/business/loginpage/?next=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2F924465935080009%2F
#2. debe existir un a app o crearla
#bussiness

# creo qeu son todos los permisos
# instagram_basic, 
# instagram_manage_comments, 
# pages_show_list, y 
# pages_read_engagement. 

#3. con esta peticion se genera un token de 60 dias
#  https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=572856578543044&client_secret=c20ba3cdffd2ab69763c21bb7d1641cd&fb_exchange_token=EAAIJApDfDcQBO8giZBJeEhbo4iUZAqCeAeUwhN7vQyTzn1ZC7qf8URxBU4GwfFwUGFeKU0C2brYJLHyo7PSRE7ikkAWMUygP1oZB861DfF4JElQGbTSRJK8TkydXyP4Bc3MpR19m3AIKHhZC0OdQbX8ZABZCyFkusNz6IjgcMpZCGsHV1sW9DZCSigrIZB07k1akouZCPSpZCIWfZCIpnRT4oZAAgBNk66qrY8nMZA66AZDZD


# {
#   "access_token": "EAAIJApDfDcQBO4nNgzctCqYNnMoRiwCwMZB2oxvZAw3XyBbiZCRvyugnQz015JB9lzr99NZAgaT9hq8NvuHHRLzpMen2LJPQ6rkdaOV8lIPFvOh5Lx9qfJHUDtFWKMH2lpbPZBVpMx8ghvtvHQt9lxLZCE49A6T1SCP0O5x0iZBrn0fpEZCwbB8n3lYcqYOJLyXBOZBIafsxa",
#   "token_type": "bearer",
#   "expires_in": 5184000
# }

from pymongo import MongoClient, UpdateOne
import requests
import time


ACCESS_TOKEN = "EAAIJApDfDcQBO4nNgzctCqYNnMoRiwCwMZB2oxvZAw3XyBbiZCRvyugnQz015JB9lzr99NZAgaT9hq8NvuHHRLzpMen2LJPQ6rkdaOV8lIPFvOh5Lx9qfJHUDtFWKMH2lpbPZBVpMx8ghvtvHQt9lxLZCE49A6T1SCP0O5x0iZBrn0fpEZCwbB8n3lYcqYOJLyXBOZBIafsxa"
CONNECTION = "mongodb+srv://instagram_comments_user:Dsf9dn0mRkVbPSbt@arkia-qa.by3jvcu.mongodb.net/instagram_comments"
DATABASE = "instagram_comments"

def main():
    get_instagram_data(ACCESS_TOKEN, handle_media_comments)

def handle_media_comments(media, comments):
    client = MongoClient(CONNECTION)
    db = client[DATABASE]
    comments_collection = db['media_comments']
    media_collection = db['media']

    media_filter = {'id': media['id']}
    media_update = {
        "$set": {
            'id': media['id'],
            'media_url': media.get('media_url',""),
            'like_count': media['like_count'],
            'comments_count': media['comments_count']
        }
    }

    session = client.start_session()
    session.start_transaction()
    try:
        # Usar bulk para actualizar o insertar el documento de media
        media_collection.bulk_write([UpdateOne(media_filter, media_update, upsert=True)])
        print(f"media: {media['id']} likes: {media['like_count']} comments: {media['comments_count']}")

        # Preparar las operaciones de bulk para los comentarios
        comment_operations = []
        for c in comments:
            comments_filter = {'id': c['id']}
            comments_update = {
                "$set": {
                    'timestamp': c['timestamp'],
                    'media': c['media'],
                    'text': c['text'],
                    'replies': c.get('replies', []),
                    'username': c['username']
                }
            }
            comment_operations.append(UpdateOne(comments_filter, comments_update, upsert=True))
            print(f"comment: {c['id']} text: {c['text']} replies: {len(c.get('replies', {}).get('data', []))}")

        # Ejecutar en lotes de 500 operaciones
        for i in range(0, len(comment_operations), 500):
            batch = comment_operations[i:i + 500]
            comments_collection.bulk_write(batch)

        session.commit_transaction()
    except Exception as ex:
        print(ex)
        session.abort_transaction()
    finally:
        session.end_session()
    client.close()


def get_instagram_data(access_token, action):
    url_media = f"https://graph.facebook.com/v21.0/17841401105622933?fields=name,media{{comments_count,like_count,media_url}}&limit=100&access_token={access_token}"
    media_data, next_page = get_media(url_media, access_token)
    print(f"{len(media_data)} media found")
    while media_data:
        for batch in [media_data[i:i+50] for i in range(0, len(media_data), 50)]:
            print(f"Processing batch of {len(batch)} media")
            for data in batch:
                process_media(data, access_token, action)

        if not next_page:
            break
        media_data, next_page = get_media(next_page, "")


def process_media(data, access_token, action):
    comments_media = []
    comments, next_page = get_comments(data['id'], access_token)

    while comments:
        comments_media.extend(comments)
        if not next_page:
            break
        comments, next_page = get_comments(next_page, "")
    print(f"Media: {data['id']} comments: {len(comments_media)}")
    action(data, comments_media)

def get_media(url, access_token):
    # if access_token:
    #     url = url.replace("@@access_token", access_token)
    response = retry(lambda: get_request(url), 3)
    media = response.get('media', [])

    if(len(media)==0):
        if(len(response.get('data', []))>0):
            return response.get('data', []), response.get('paging', {}).get('next', "")
        else:
            print("No hay datos")
            return [], ""
    return media.get('data', []), media.get('paging', {}).get('next', "")

def get_comments(media_id, access_token):
    if(media_id.startswith("https")):
        url=media_id
    else:
        url = f"https://graph.facebook.com/v21.0/{media_id}/comments?fields=text,media,timestamp,username,replies{{text,timestamp,username}}&access_token={access_token}"
    response = retry(lambda: get_request(url), 3)
    return response.get('data', []), response.get('paging', {}).get('next', "")

def retry(action, retry_count=3):
    attempt = 0
    while attempt < retry_count:
        try:
            return action()
        except Exception as ex:
            print(f"Attempt {attempt + 1} failed: {ex}")
            attempt += 1
            if attempt >= retry_count:
                raise
            time.sleep(2 ** attempt)

def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"fail request {url} Error: {response.status_code}, {response.reason}")
        raise Exception(f"Error: {response.status_code}, {response.reason}")

if __name__ == "__main__":
    main()
