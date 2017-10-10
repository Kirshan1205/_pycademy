import pickle, json, pprint
pp= ppronm

with open('db.json') as f:
    print f
    webDb= json.load(f)
    
pp.pprint(webDb)



with open('webDb.pkl','wb') as f:
    pickle.dump(webDb, f , pickle.HIGHEST_PROTOCOL)