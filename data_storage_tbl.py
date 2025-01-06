from azure.data.tables import TableServiceClient
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
connection_string = os.getenv("TABLE_STORAGE_CONN_STRING")

class DataStorage:
    def __init__(self, connection_string, table_name):
        self.connection_string = connection_string
        self.table_name = table_name
        self.table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        self.ensure_table_exists()

    def ensure_table_exists(self):
        try:
            self.table_service_client.create_table(self.table_name)
            print(f"Table '{self.table_name}' created.")
        except Exception as e:
            if "TableAlreadyExists" in str(e):
                print(f"Table '{self.table_name}' already exists.")
            else:
                raise

    def upload_session_data(self, dictionary):
        table_client = self.table_service_client.get_table_client(self.table_name)
        session_id = str(uuid.uuid4())
        
        # Create an entity with the Session ID as RowKey and the dictionary values as properties
        entity = {
            "PartitionKey": "SessionDataPartition",  # Can be constant or dynamic based on your needs
            "RowKey": session_id,  # Session ID as RowKey (unique identifier)
        }
        
        # Add the dictionary values as properties in the entity
        entity.update(dictionary)

        # Insert or update the entity in the table
        table_client.upsert_entity(entity=entity)

    def download_all_sessions_data(self):
        table_client = self.table_service_client.get_table_client(self.table_name)
        
        # Query to get all entities in the table
        entities = table_client.query_entities("PartitionKey eq 'SessionDataPartition'")
        
        # Prepare the result list by removing metadata keys and returning only the dictionary values
        all_session_data = []
        for entity in entities:
            session_data = {key: value for key, value in entity.items() if key not in ("PartitionKey", "RowKey", "odata.metadata")}
            all_session_data.append(session_data)
        
        print(f"All session data retrieved.")
        return all_session_data

