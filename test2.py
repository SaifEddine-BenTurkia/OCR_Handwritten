import requests

# Set up authentication
email_address = "benturkia44@gmail.com"  # Replace with your email
api_key = "w7qykwm0mholf141llfendua2vj0pg2nnpz59x8bkq"  # Replace with your actual API key
auth = (email_address, api_key)

# Test authentication
response = requests.get("https://api.algodocs.com/v1/me", auth=auth)
if response.status_code == 200:
    print("✅ Authentication Successful:", response.json())
else:
    print("❌ Authentication Failed:", response.text)
    exit()

# List available extractors
response = requests.get("https://api.algodocs.com/v1/extractors", auth=auth)
if response.status_code == 200:
    extractors = response.json()
    print("📝 Available Extractors:", extractors)
else:
    print("❌ Failed to retrieve extractors:", response.text)
    exit()

# Define extractor and folder IDs
extractor_id = "j31tjpam0xtl9fyz6cwtx9hy"  # Replace with actual Extractor ID
folder_id = "lp180fst1jyy"  # Replace with actual Folder ID
file_path = r"C:\Users\pc\Desktop\r.pdf"  # Path to your PDF file

# Upload the document
upload_url = f"https://api.algodocs.com/v1/document/upload_local/{extractor_id}/{folder_id}"
with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(upload_url, files=files, auth=auth)

if response.status_code == 200:
    upload_response = response.json()
    print("📄 Document Uploaded Successfully:", upload_response)

    # Extract document ID dynamically
    document_id = upload_response.get("document_id")  # ✅ Corrected retrieval
    if not document_id:
        print("❌ Document ID not found in response:", upload_response)
        exit()

    # Retrieve extracted data
    data_url = f"https://api.algodocs.com/v1/extracted_data/{document_id}"
    response = requests.get(data_url, auth=auth)

    if response.status_code == 200:
        print("📜 Extracted Data:", response.json())
    else:
        print("❌ Failed to retrieve extracted data:", response.text)
else:
    print("❌ Document Upload Failed:", response.text)
