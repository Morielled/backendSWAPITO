from flask import Flask, request, abort, json
from flask_restful import Resource, Api
from flask_cors import CORS
import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)

#for cross origin resource sharing
cors = CORS(app, resources={r"/*": {"origins": "*"}})



###### DATABASE ######
######################

#firebase credentials

json_data = os.environ.get('FIREBASE_KEY')

if json_data is None:
    cred = credentials.Certificate ('firebase-key.json')
else:
    var = json.loads(json_data)
    cred = credentials.Certificate (var)

#initialize app
firebase_admin.initialize_app(cred)

db = firestore.client ()

###### API ######

api = Api(app)

ads = []

class Ads(Resource):

    def get(self):  

        id = request.args.get('id')
        doc_ref = db.collection(u'advertisements').document(id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            abort(404)

    def post(self):
        
        doc_ref = db.collection('advertisements').document()
        response = request.get_json()
        now = datetime.now()
        ad = {
                'type':response.get('type',''),
                'userID':response.get('userID',''),
                'category':response.get('category',[]),
                'name':response.get('name',''),
                'description':response.get('description',''),
                'exchange':response.get('exchange',''),
                'picture':response.get('picture',''),
                'date_posted':str(now)
              }
        doc_ref.set(ad)
        return ad

'''
    def delete(self):
        
        for id,ad_del in enumerate(ads):
            if ad_del['id'] == id:
                deleted_ad = ads.pop(id)
                return {'note': 'delete success'}

        id = request.args.get('id')
        ad_del = db.collection(u'inzeraty').document(id).delete()
        ad = ad_del.get()
        if doc.exists:
            return doc.to_dict()
        else:
            abort(404)
'''

class AllAds(Resource):
    
    def get(self):  

        docs = db.collection(u'advertisements').stream()
        ads = []
        for doc in docs:
          ads.append(doc.to_dict())
        return ads


class Users(Resource):

    def post(self):
        
        response = request.get_json()
        doc_ref = db.collection('users').document(response.get('userID'))
        user = {
                'userName':response.get('userName',''),
                'userEmail':response.get('userEmail',''),
                'userPhoto':response.get('userPhoto',''),
                'location':response.get('location',''),
                'searches':response.get('searches',''),
                'offers':response.get('offers','')
              }
        doc_ref.set(user)
        return user


class User(Resource):

    def put(self,userID):
        
        response = request.get_json()
        doc_ref = db.collection('users').document(userID)
        doc = doc_ref.get()

        if not doc.exists:
            abort(404) 
 
        user = {
                'location':response.get('location',''),
                'searches':response.get('searches',''),
                'offers':response.get('offers','')
            }
        doc_ref.update(user)
        return doc_ref.get().to_dict()

    def get(self,userID):  

        doc_ref = db.collection(u'users').document(userID)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            abort(404)
       



api.add_resource(Ads,'/ad')
api.add_resource(AllAds,'/ads')
api.add_resource(Users,'/user')
api.add_resource(User,'/user/<string:userID>')


if __name__ == '__main__':
    app.run(debug=True)


