using System;
using System.Security.Authentication;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using System.Net;
using System.Drawing;
using System.IO;
using System.Drawing.Imaging;

using Newtonsoft.Json;
using Azure.Storage.Blobs;
using MongoDB.Driver;
using MongoDB.Bson;

using AlphaTaibai.Models;
using AlphaTaibai.Utilities;

namespace AlphaTaibai.ImageCrawler
{
    public static class GeneralImage2CrawlQueueTrigger
    {
        static IMongoCollection<SavedImageInfo> SavedImageCollection;
        static BlobContainerClient SavedImageBlobClient;
        static string ContainerName = "images";
        static string BlobFolder = "generic";
        static GeneralImage2CrawlQueueTrigger()
        {
            // initialize the collection needed for recording. 
            string dbName = "dev";
            string collectionName = "generic_crawled_image";
            string connectionString = GetEnvironmentVariable("MongoDBConnectionString");
            MongoClientSettings settings = MongoClientSettings.FromUrl(
                                            new MongoUrl(connectionString)
                                            );
            settings.SslSettings =
            new SslSettings() { EnabledSslProtocols = SslProtocols.Tls12 };
            var mongoClient = new MongoClient(settings);
            var database = mongoClient.GetDatabase(dbName);
            SavedImageCollection = database.GetCollection<SavedImageInfo>(collectionName);

            string BlobconnectionString = GetEnvironmentVariable("longriverstorage_STORAGE");
            SavedImageBlobClient = new BlobContainerClient(BlobconnectionString, ContainerName);
        }

        [Function("GeneralImage2CrawlQueueTrigger")]
        public static void Run([QueueTrigger("general-image-2-crawl", Connection = "AzureWebJobsStorage")] string myQueueItem,
            FunctionContext context)
        {
            var logger = context.GetLogger("ImageCrawlQueueTrigger");
            logger.LogInformation($"[Queue Trigger] function processed: {myQueueItem}");
            
            try{

                ImageToCrawlMsg msg = JsonConvert.DeserializeObject<ImageToCrawlMsg>(myQueueItem);
                // check if hit cache
                var cachedRes = SavedImageCollection.Find(x => x.ImageUrl == msg.ImageUrl);
                if (cachedRes.Any())
                {

                    logger.LogInformation($"hit the cache, skip crawling {msg.ImageUrl}");
                    return;
                }

                // start downloading the image
                using (WebClient client = new WebClient())
                {
                    byte[] ImageBytes;
                    Bitmap bmp;

                    // determine the image name
                    //string formatSuffix = (msg.ImageUrl.EndsWith("jpeg") || msg.ImageUrl.EndsWith("jpg")) ? ".jpg" : ".png";
                    string formatSuffix = (msg.ImageUrl.EndsWith("png")) ? ".png" : ".jpg";
                    string shortname = String.Format("{0:X}", msg.ImageUrl.GetHashCode());
                    string shortnameTH = String.Format("{0:X}_th", msg.ImageUrl.GetHashCode());

                    string blobname = BlobFolder + "/" +  DateTime.Now.Year + "/" + DateTime.Now.Month + "/" + shortname + formatSuffix;
                    string blobnameTH = BlobFolder + "/" +  DateTime.Now.Year + "/" + DateTime.Now.Month + "/" + shortnameTH + ".jpg";
                    
                    // process the original image
                    using (Stream stream = client.OpenRead(msg.ImageUrl))
                    {
                        using (MemoryStream ms = new MemoryStream())
                        {
                            stream.CopyTo(ms);
                            ImageBytes = ms.ToArray();
                            bmp = new Bitmap(ms);
                            ms.Position =0;
                            var res = SavedImageBlobClient.UploadBlob(blobname, ms);
                        }
                    }
                    // process the TH
                    Image thImage = Utilities.Helper.ResizeImage(bmp, new Size(150, 150));
                    if (thImage != null){
                        using (MemoryStream  ms = new MemoryStream())
                        {
                            thImage.Save(ms, ImageFormat.Jpeg);
                            ms.Position = 0;
                            var resTH = SavedImageBlobClient.UploadBlob(blobnameTH, ms);
                        }
                    }

                    var info = new SavedImageInfo()
                    {
                        Id = ObjectId.GenerateNewId(),
                        Container = ContainerName,
                        ImageUrl = msg.ImageUrl,
                        BlobPath = blobname,
                        ImageSize = ImageBytes.Length,
                        Width = bmp?.Width,
                        Height = bmp?.Height,
                        UploadTimeStamp = ((DateTimeOffset)DateTime.Now).ToUnixTimeSeconds(),
                        AddStringInfo = msg.AddStringInfo,
                        AddIntInfo = msg.AddIntInfo
                    };
                    // insert into db
                    SavedImageCollection.InsertOne(info);
                }
            }
            catch(JsonReaderException e ){
                logger.LogError($"ParseJsonError: {e.Message}");
                return;
            }
            catch(Exception e)
            {
                logger.LogError($"UnknownError {e.Message}");
                return;
            }
        }
        private static string GetEnvironmentVariable(string name)
        {
            return System.Environment.GetEnvironmentVariable(name, EnvironmentVariableTarget.Process);
        }            
    }
}
