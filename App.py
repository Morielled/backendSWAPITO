from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)

#for cross origin resource sharing
cors = CORS(app, resources={r"/*": {"origins": "*"}})



###### DATABASE ######
######################

#firebase credentials
cred = credentials.Certificate ('firebase-key.json')

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
        ad = {
                'id': doc_ref.id,
                'type':response.get('type',''),
                'category':response.get('category',''),
                'name':response.get('name',''),
                'description':response.get('description',''),  
                'street':response.get('street',''),
                'city':response.get('city',''),
                'zipCode':response.get('zipCode',''),
                'exchange':response.get('exchange',''),
                'date_posted': 'October 20, 2020'
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


class User(Resource):

    def post(self):
        
        doc_ref = db.collection('users').document()
        response = request.get_json()
        user = {
                'userID':response.get('userID',''),
                'userName':response.get('userName',''),
                'userEmail':response.get('userEmail',''),
                'userPhoto':response.get('userPhoto',''),
              }
        doc_ref.set(user)
        return user



api.add_resource(Ads,'/ad')
api.add_resource(AllAds,'/ads')
api.add_resource(User,'/user')




if __name__ == '__main__':
    app.run(debug=True)


