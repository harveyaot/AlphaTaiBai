using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Bson;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace AlphaTaibai.Models{

    public class ImageToCrawlMsg {
        [JsonProperty("image_url")]
        public string ImageUrl {get; set;}
        [JsonProperty("add_string_info")]
        public Dictionary<string, string> AddStringInfo {get; set;}
        [JsonProperty("add_int_info")]
        public Dictionary<string, int> AddIntInfo {get; set;}
    }
    public class SavedImageInfo
    {
        [BsonId]
        public ObjectId Id { get; set; }
        public string Container { get; set; }
        public string BlobPath { get; set; }
        public string ImageUrl { get; set; }
        public long ImageSize { get; set; }
        public int? Width {get; set;}
        public int? Height {get; set;}
        public Dictionary<string, string> AddStringInfo {get; set;}
        // include sourceurl, sourcecode, wpmediakd, width
        public Dictionary<string, int> AddIntInfo {get; set;}
        public Dictionary<string, List<int>> AddEmbInfo {get; set;}
        public long UploadTimeStamp { get; set; }
    }
}