from bs4 import BeautifulSoup
from google.cloud import bigtable
from google.cloud.bigtable import row_filters


class BigTable(object):
    def __init__(self, project, instance_id, table_id):
        self.project = project
        self.instance_id = instance_id
        self.table_id = table_id
        self.table = None
        self._instantiate_table()

    def _instantiate_table(self):
        if not self.table:
            # Create a Cloud Bigtable client.
            client = bigtable.Client(project=self.project)
            # Connect to an existing Cloud Bigtable instance.
            instance = client.instance(instance_id=self.instance_id)
            # Open an existing table.
            self.table = instance.table(table_id=self.table_id)
        return self.table


class DocumentBigTable(BigTable):
    def __init__(self, project, instance_id, table_id, column_family_id, column_qualifier):
        super().__init__(project, instance_id, table_id)
        self.column_family_id = column_family_id
        self.column_qualifier = column_qualifier

    def fetch_document_content(self, document_id, organization_id):
        # Create a filter to only retrieve the most recent version of the cell for each column accross entire row.
        row_filter = row_filters.CellsColumnLimitFilter(1)

        row_key = str(document_id)[::-1] + '_' + str(organization_id)
        row = self._instantiate_table().read_row(row_key.encode('utf-8'), row_filter)

        if row:
            column_id = self.column_qualifier.encode('utf-8')
            return row.cells[self.column_family_id][column_id][0].value.decode('utf-8')
        else:
            return None

    def fetch_document_text(self, document_id, organization_id):
        content_html = self.fetch_document_content(document_id, organization_id)
        if content_html:
            # strip html code
            soup = BeautifulSoup(content_html, 'lxml')
            return soup.get_text(' ', True)
        else:
            return None
