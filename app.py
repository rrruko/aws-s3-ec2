from flask import Flask, jsonify, Response, request
import boto3
import json

app = Flask(__name__)

@app.route('/songs/for/album')
def songs_for_album():
  return respond('album')

@app.route('/albums/for/artist')
def albums_for_artist():
  return respond('artist')

@app.route('/artists/for/genre')
def artists_for_genre():
  return respond('genre')

@app.route('/song')
def song():
  return respond('song')

@app.route('/genres')
def genres():
  response = Response(lookup_ddb('genre'))
  response.headers['Access-Control-Allow-Origin'] = '*'
  return response

@app.route('/add-user', methods=['POST'])
def add_user():
  ddb = boto3.resource('dynamodb', region_name='us-east-1').Table('music')
  print('request data: ' + request.get_data())
  j = json.loads(request.get_data())
  try:
    item = {
      'id': j['id'],
      'email': j['email'],
      'name': j['name']
    }
    print(item)
    ddb.put_item(TableName='users', Item=item)
    return ""
  except LookupError:
    return "Need an id, email, and name", 400

def respond(arg):
  arg = request.args.get(arg, '')
  response = Response(lookup_ddb(arg))
  response.headers['Access-Control-Allow-Origin'] = '*'
  return response

def lookup_ddb(key):
  ddb = boto3.client('dynamodb', region_name='us-east-1')
  response = ddb.query(
    TableName='music',
    KeyConditionExpression='PK = :v1',
    ExpressionAttributeValues={
      ':v1': {
        'S': key
      },
    }
  )
  response = [item['SK']['S'] for item in response['Items']]
  return json.dumps(response)
