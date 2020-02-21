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

def respond(arg):
  arg = request.args.get(arg, '')
  response = Response(lookup_ddb(arg))
  response.headers['Access-Control-Allow-Origin'] = '*'
  return response

def lookup_ddb(key):
  ddb = boto3.client('dynamodb')
  response = ddb.query(
    TableName='music',
    KeyConditionExpression='PK = :v1',
    ExpressionAttributeValues={
      ':v1': {
        'S': key
      },
    }
  )
  return str(response)
