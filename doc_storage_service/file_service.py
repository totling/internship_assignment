from database import save_file_to_gridfs, save_file_metadata


async def handle_file(file_message: dict):
    user_id = file_message['user_id']
    file_name = file_message['filename']
    file_data = file_message['file_content'].encode('latin-1')

    file_id = await save_file_to_gridfs(file_data, file_name)

    await save_file_metadata(user_id, file_id, file_name)

    print(f"File saved with GridFS ID: {file_id} for user {user_id}")
