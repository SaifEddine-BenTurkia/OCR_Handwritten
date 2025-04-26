import algodocs

# Initialize the client
email_address = "benturkia44@gmail.com"
api_key = "w7qykwm0mholf141llfendua2vj0pg2nnpz59x8bkq"
client = algodocs.AlgoDocsClient(email_address, api_key)

# Test authentication
user_info = client.me()
print(user_info)

# List available extractors
extractors = client.getExtractors()
print(extractors)

# Upload a document
extractor_id = "j31tjpam0xtl9fyz6cwtx9hy"  # Replace with actual extractor ID
folder_id = "lp180fst1jyy"        # Replace with actual folder ID
file_path = "root/Résumé crypto chap 1 et 2.pdf"
upload_response = client.uploadDocumentLocal(extractor_id, folder_id, file_path)
print(upload_response)

# Retrieve extracted data
document_id = upload_response['id']
extracted_data = client.getExtractedDataByDocumentID(document_id)
print(extracted_data) 
