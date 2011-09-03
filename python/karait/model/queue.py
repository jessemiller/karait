import time
import pymongo
from karait.model.message import Message

class Queue(object):
    
    ALREADY_EXISTS_EXCEPTION_STRING = 'collection already exists'
    
    def __init__(
        self,
        host='localhost',
        port=27017,
        database='karait',
        queue='messages',
        average_message_size=8192,
        queue_size=4096
    ):
        self.host = host
        self.port = port
        self.database = database
        self.queue = queue
        self.average_message_size = average_message_size
        self.queue_size = queue_size
        self._create_mongo_connection()
        
    def _create_mongo_connection(self):
        self.connection = pymongo.Connection(
            self.host,
            self.port
        )
        self.queue_database = self.connection[self.database]
        self.queue_collection = self.queue_database[self.queue]
        self._create_capped_collection()
        
    def _create_capped_collection(self):
        try:
            pymongo.collection.Collection(
                self.connection[self.database],
                self.queue,
                size = (self.average_message_size * self.queue_size),
                capped = True,
                max = self.queue_size,
                create = True
            )
             
            self.queue_collection.create_index('_id')
            self.queue_collection.create_index('_meta.routing_key')
             
        except pymongo.errors.OperationFailure, operation_failure:
            if not self.ALREADY_EXISTS_EXCEPTION_STRING in str(operation_failure):
                raise operation_failure
    
    def write(self, message, routing_key=None, expire=-1.0):
        if type(message) == dict:
            message_dict = message
        else:
            message_dict = message.to_dictionary()
            
        message_dict['_meta'] = {}
        message_dict['_meta']['expired'] = False
        message_dict['_meta']['timestamp'] = time.time()
        message_dict['_meta']['expire'] = expire
        
        if routing_key:
            message_dict['_meta']['routing_key'] = routing_key
                
        self.queue_collection.insert(message_dict, safe=True)
    
    def read(self, routing_key=None, messages_read=10, visibility_timeout=-1.0):
        messages = []
        
        conditions = {
            '_meta.expired': False
        }
        
        if routing_key:
            conditions['_meta.routing_key'] = routing_key
        else:
            conditions['_meta.routing_key'] = {
                '$exists': False
            }
        
        try:
            
            for raw_message in self.queue_database.eval(self._generate_find_with_timeouts_code(
                conditions=conditions,
                messages_read=messages_read,
                visibility_timeout=visibility_timeout
            )):
                message = Message(dictionary=raw_message, queue_collection=self.queue_collection)
                messages.append(message)
        except pymongo.errors.OperationFailure:
            return self.read(routing_key, messages_read)
            
        return messages
    
    def delete_messages(self, messages):
        ids = []
        for message in messages:
            ids.append(message._source['_id'])
        
        self.queue_collection.update(
            {
                '_id': {
                    '$in': ids
                }
            },
            {
                '$set': {
                    '_meta.expired': True
                }
            },
            multi=True,
            safe=True
        )
    
    def _generate_find_with_timeouts_code(self, conditions={}, messages_read=10, visibility_timeout=-1.0):
        return pymongo.code.Code("""
            function() {
                var results = [];
                
                function expire(result) {
                    var currentTime = parseFloat(new Date().getTime()) / 1000.0;
                    if (result._meta.expire <= 0.0) {
                        return false;
                    } else if ( (currentTime - result._meta.timestamp) > result._meta.expire ) {
                        return true;
                    }
                }
            
                (function fetchResults() {
                    var cursor = db[collection].find(conditions).limit(limit);
                    cursor.forEach(function(result) {
                        if (!expire(result)) {
                            results.push(result);
                        }
                    });
                })();
            
                return results;
            }
        """,
        {
            'conditions': conditions,
            'limit': messages_read,
            'collection': self.queue
        })