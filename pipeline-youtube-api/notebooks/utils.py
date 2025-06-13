# utils.py

import re
import requests
from googleapiclient.discovery import build

def get_id(url: str, api_key: str) -> str:
    """
    Retorna o channelId do YouTube a partir de uma URL de canal (customizada, @handle ou padrão).
    Usa a API do YouTube Data v3.

    Args:
        url (str): URL do canal no YouTube.
        api_key (str): Sua chave de API do YouTube.

    Returns:
        str: channelId (ex: 'UCXXXXXXXXXXXX')
    """
    # Verifica se é um @handle (ex: https://www.youtube.com/@piscagames24)
    match_handle = re.search(r'youtube\.com/@([a-zA-Z0-9_]+)', url)
    if match_handle:
        handle = match_handle.group(1)
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.search().list(
            q=f"@{handle}",
            type='channel',
            part='snippet',
            maxResults=1
        ).execute()
        items = response.get("items", [])
        if items:
            return items[0]['snippet']['channelId']
        else:
            raise ValueError("Canal não encontrado com esse handle.")

    # Verifica se é um URL personalizado (ex: youtube.com/c/nome)
    match_custom = re.search(r'youtube\.com/(c|user)/([a-zA-Z0-9_]+)', url)
    if match_custom:
        username = match_custom.group(2)
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.channels().list(
            forUsername=username,
            part='id'
        ).execute()
        items = response.get("items", [])
        if items:
            return items[0]['id']
        else:
            raise ValueError("Canal não encontrado com esse nome personalizado.")

    # Verifica se já é uma URL com channelId (ex: youtube.com/channel/UCxxx)
    match_id = re.search(r'youtube\.com/channel/(UC[a-zA-Z0-9_-]+)', url)
    if match_id:
        return match_id.group(1)

    raise ValueError("Formato de URL não reconhecido ou canal não encontrado.")

def get_videos(youtube, channel_id):
    """
    Puxa todos os vídeos públicos do canal usando a playlist de uploads.
    """
    uploads_playlist_id = 'UU' + channel_id[2:]
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        items = response.get('items', [])
        videos.extend(items)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def get_video_id(url):
    """Extrai o videoId da URL do YouTube"""
    try:
        parsed = urlparse(url)  # Parse the URL
        if 'youtube.com' in parsed.netloc:  # If the URL is from youtube.com
            return parse_qs(parsed.query)['v'][0]  # Return the videoId from the query string
        elif 'youtu.be' in parsed.netloc:  # If the URL is from youtu.be
            return parsed.path[1:]  # Return the videoId from the path
    except Exception:
        return None  # Return None if an exception occurs

def add_video(video_id):
    """Adiciona ou ignora um vídeo já presente"""
    hoje = datetime.utcnow().isoformat()
    
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        if video_id in df['video_id'].values:
            print(f"Vídeo {video_id} já está sendo monitorado.")
            return
    else:
        df = pd.DataFrame(columns=['video_id', 'data_inicio', 'status'])

    novo = pd.DataFrame([{
        'video_id': video_id,
        'data_inicio': hoje,
        'status': 'ativo'
    }])

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print(f"Vídeo {video_id} adicionado ao monitoramento.")