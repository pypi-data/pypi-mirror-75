from cli.utils import get_base_file_path
from cli.constants import DATABASE_FILENAME
from tinydb import TinyDB, Query

class Database:

  def __init__(self, database_file_path=None):
    if not database_file_path:
      database_file_path = self.get_database_file_path()
    self.db = TinyDB(database_file_path)

  def get_database_file_path(self):
    file_path = get_base_file_path(DATABASE_FILENAME)
    return file_path

  def get_recording_id_from_name(self, name):
    id = None
    table_name = 'recordings'
    query = Query()
    table = self.db.table(table_name)
    response = table.search(query.live_stream_name == name)
    if response:
      id = response[0].get('recording_id', None)
    return id

  def get_live_stream_id_from_name(self, name):
    id = None
    table_name = 'live_streams'
    query = Query()
    table = self.db.table(table_name)
    response = table.search(query.live_stream_name == name)
    if response:
      id = response[0].get('live_stream_id', None)
    return id

  def recordings_table_exist(self):
    table_name = 'recordings'
    tables = self.db.tables()
    exist = table_name in tables
    return exist

  def live_streams_table_exist(self):
    table_name = 'live_streams'
    tables = self.db.tables()
    exist = table_name in tables
    return exist

  def insert_live_stream_mappings(self, document_batch):
    table_name = 'live_streams'
    self.db.drop_table(table_name)
    table = self.db.table(table_name)
    table.insert_multiple(document_batch)

  def insert_live_stream_mapping(self, document):
    table_name = 'live_streams'
    table = self.db.table(table_name)
    table.insert(document)

  def delete_live_stream_mapping(self, id):
    Spec = Query()
    table_name = 'live_streams'
    table = self.db.table(table_name)
    table.remove(Spec.live_stream_id.matches(id))

  def insert_recording_mappings(self, document_batch):
    table_name = 'recordings'
    self.db.drop_table(table_name)
    table = self.db.table(table_name)
    table.insert_multiple(document_batch)

  def insert_specification(self, specification):
    table_name = 'specifications'
    table = self.db.table(table_name)
    table.insert(specification)

  def delete_specification(self, id):
    Spec = Query()
    table_name = 'specifications'
    table = self.db.table(table_name)
    table.remove(Spec.id.matches(id))

  def update_specification(self, specification):
    Spec = Query()
    table_name = 'specifications'
    table = self.db.table(table_name)
    id = specification['id']
    table.update(specification, Spec.id.matches(id))

  def get_specification_by_name(self, name):
    Spec = Query()
    table_name = 'specifications'
    table = self.db.table(table_name)
    stored_specification = table.search(Spec.name.matches(name))

    if not stored_specification:
      return None
    else:
      return stored_specification[0] # convert list to single item

  def get_specification_by_id(self, id):
    Spec = Query()
    table_name = 'specifications'
    table = self.db.table(table_name)
    stored_specification = table.search(Spec.id.matches(id))
    return stored_specification
