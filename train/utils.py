import pymongo

MONGODB_SERVER = "13.75.105.50"                                                                   
#MONGODB_SERVER = "localhost"                                                                   
MONGODB_PORT = 27018                                                                          
MONGODB_DB = "alphataibai"                                                                      
MONGODB_USER = "l*" # ask project owner to update this
MONGODB_PWD = "z*"  # ask project owner to update this                              
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
    tmp_one = shiwen.find_one()
    print shiwen.count()
    print tmp_one.keys()
    print tmp_one['title']
    print tmp_one['body']
    print tmp_one['author']
    print tmp_one['like']

if __name__ == "__main__":
    get_doc_count()
