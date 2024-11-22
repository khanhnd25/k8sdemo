import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId
from rb_queue import get_rabbitmq_channel

server = Flask(__name__)

mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

# connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", heartbeat=30))
# channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    print("validate")
    access, err = validate.token(request)
    print("validate successfull")
    if err:
        return err

    access = json.loads(access)
    print("access: ", access)
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            print("------------1------------")
            return "exactly 1 file required", 400
        
        connection, channel = get_rabbitmq_channel()
        for _, f in request.files.items():
            print("----------------------")
            err = util.upload(f, fs_videos, channel, access)
            print("NOOOOOOOOO")
            if err:
                return err
        # Đóng kết nối
        channel.close()
        connection.close()
        return "success!", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)