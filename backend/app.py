from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv('TICKETMASTER_API_KEY')


@app.route('/events')
def events():
    city = (request.args.get('city') or '').strip()
    if not city:
        return jsonify({'error': 'city parameter is required'}), 400

    if not API_KEY:
        app.logger.error('TICKETMASTER_API_KEY not set')
        return jsonify({'error': 'Server configuration error'}), 500

    params = {
        'apikey': API_KEY,
        'city': city,
        'size': 20,
    }

    try:
        resp = requests.get('https://app.ticketmaster.com/discovery/v2/events.json', params=params, timeout=5)
        resp.raise_for_status()
    except Exception:
        app.logger.exception('Ticketmaster request failed')
        return jsonify({'error': 'Upstream API error'}), 502

    data = resp.json()
    events = []
    embedded = data.get('_embedded', {})
    for ev in embedded.get('events', []):
        ev_id = ev.get('id')
        name = ev.get('name')
        date = None
        dates = ev.get('dates', {})
        start = dates.get('start', {})
        date = start.get('dateTime') or start.get('localDate')

        venue = None
        try:
            venues = ev.get('_embedded', {}).get('venues', [])
            if venues:
                venue = venues[0].get('name')
        except Exception:
            venue = None

        url = ev.get('url')
        image = None
        images = ev.get('images', [])
        if images:
            image = images[0].get('url')

        events.append({
            'id': ev_id,
            'name': name,
            'date': date,
            'venue': venue,
            'url': url,
            'image': image,
        })

    return jsonify({'events': events, 'count': len(events)})


if __name__ == '__main__':
    # Default development port
    app.run(host='0.0.0.0', port=5000, debug=True)
