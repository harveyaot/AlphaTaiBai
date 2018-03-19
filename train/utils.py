import pymongo

MONGODB_SERVER = "13.75.105.50"                                                                   
#MONGODB_SERVER = "localhost"                                                                   
MONGODB_PORT = 27018                                                                          
MONGODB_DB = "alphataibai"                                                                      
MONGODB_USER = "" # ask project owner for this
MONGODB_PWD = ""  # ask project owner for his                              
MONGODB_COLLECTION_AUTHOR = "author"   
MONGODB_COLLECTION_SHIWEN = "shiwen"   


def get_mongodb():
    client = pymongo.MongoClient(host=MONGODB_SERVER,\
                                port=MONGODB_PORT,\
                                username=MONGODB_USER,\
                                password=MONGODB_PWD,\
                                authSource=MONGODB_DB\
                                )

    db = client[MONGODB_DB]
    return db

def get_doc_count():
    db = get_mongodb()
    shiwen = db[MONGODB_COLLECTION_SHIWEN]
    print shiwen.count()

if __name__ == "__main__":
    get_doc_count()
