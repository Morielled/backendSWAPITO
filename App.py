from flask import Flask
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

'''
doc_ref = db.collection('inzeraty').document('inzerat1')

doc_ref.set(
            {
                'id': '1'
                'author': 'Misa Drapelova',
                'id': 'Stůl',
                'content': 'Stůl je málo používaný',
                'date_posted': 'October 20, 2020'
            }
          )


doc_ref = db.collection('inzeraty').document('inzerat2')

doc_ref.set(
            {
                'id': '2'
                'author': 'Tereza Modrá',
                'id': 'Židle',
                'content': 'Židle je krásná',
                'date_posted': 'October 22, 2020'
            }
          )
'''


###### API ######

api = Api(app)

ads = []

class Ads(Resource):

    def get(self, id):

        for ad in ads:
            if ad['id'] == id:
                return ad
        
        return {'id':None}, 404


    def post(self):

        doc_ref = db.collection('inzeraty').document()

        ad = {
                'id': doc_ref.id,
                'author': 'Misa Drapelova',
                'title': 'Stůl',
                'content': 'Stůl je málo používaný',
                'date_posted': 'October 20, 2020'
              }

        doc_ref.set(ad)

        return ad


    def delete(self, id):

        for ind,ad in enumerate(ads):
            if ad['id'] == id:
                deleted_ad = ads.pop(ind)
                return {'note': 'delete success'}


class AllAds(Resource):
    
    def get(self):  

        docs = db.collection(u'inzeraty').stream()

        ads = []

        for doc in docs:
          ads.append(doc.to_dict())

        return ads


api.add_resource(Ads,'/ad')
api.add_resource(AllAds, '/ads')




if __name__ == '__main__':
    app.run(debug=True)


