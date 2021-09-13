

Schema ={
    
  
   "type": "object",
	
   "properties": {
	
    
		
      "file_name": {
         "description": "Name of the product",
         "type": "string"
      },
		
      "position": {
         "type": "array",
         "items":{
             "type":"integer"
         },
         "minimum": 0,
         "maxItems":4,
         "minItems":4

      }
   },
	
   "required": ["file_name","position"]
}
