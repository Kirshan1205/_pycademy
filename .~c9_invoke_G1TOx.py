import pickle, json, pprint
pp= pprint.PrettyPrinter(indent=4)

with open('db.json') as f:
    print f
    webDb= json.load(f)
    
pp.p(webDb)



with open('webDb.pkl','wb') as f:
    pickle.dump(webDb, f , pickle.HIGHEST_PROTOCOL)