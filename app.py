from flask import Flask, jsonify, Response
import boto3
import json

BUCKET_NAME = 'cs493-joneetha-music'

app = Flask(__name__)

@app.route('/')
def serve():
  resp = Response(json.dumps(get_music_obj()))
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp

def get_music_obj():
  session = boto3.Session()
  s3 = session.resource('s3')
  res = {}
  for o in s3.Bucket(BUCKET_NAME).objects.all():
    path = o.key.split('/')
    artist = path[0]
    album = path[1]
    title = path[2]
    presigned = boto3.client('s3').generate_presigned_url(
      'get_object',
      Params={'Bucket': BUCKET_NAME, 'Key': o.key},
      ExpiresIn=3600
    )
    if artist in res:
      if album in res[artist]:
        res[artist][album][title] = presigned
      else:
        res[artist][album] = { title: presigned }
    else:
      res[artist] = { album: { title: presigned } }
  return res
