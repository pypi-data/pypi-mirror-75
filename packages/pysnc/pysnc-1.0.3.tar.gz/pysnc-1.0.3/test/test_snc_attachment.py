from unittest import TestCase

from pysnc import ServiceNowClient
from constants import Constants
from utils import TempTestRecord


class TestAttachment(TestCase):
    c = Constants()

    def _deleteOrCreateTestRecord(self):
        client = ServiceNowClient(self.c.server, self.c.credentials)
        gr = client.GlideRecord('problem')
        gr.add_query('short_description', 'Unit Test - Attachments')
        gr.query()
        if gr.next():
            return gr
        gr.initialize()
        gr.short_description = "Unit Test - Attachments"
        gr.description = "Second Field"
        gr.insert()
        return gr

    def _getOrCreateEmptyTestRecord(self):
        client = ServiceNowClient(self.c.server, self.c.credentials)
        gr = client.GlideRecord('problem')
        gr.add_query('short_description', 'Unit Test - Attachments - Empty')
        gr.query()
        if gr.next():
            return gr
        gr.initialize()
        gr.short_description = "Unit Test - Attachments - Empty"
        gr.description = "Second Field"
        gr.insert()
        return gr


    def test_attachments_for(self):
        gr = self._getOrCreateEmptyTestRecord()
        attachments = gr.get_attachments()
        print(attachments)
        self.assertNotEquals(attachments, None)
        self.assertEquals(len(attachments), 0)

    def test_add_delete(self):
        client = ServiceNowClient(self.c.server, self.c.credentials)
        with TempTestRecord(client, 'problem') as gr:
            attachments = gr.get_attachments()
            self.assertNotEquals(attachments, None)
            self.assertEquals(len(attachments), 0)

            content = "this is a sample attachment"
            gr.add_attachment('test.txt', content)

            attachments = gr.get_attachments()
            self.assertEquals(len(attachments), 1)

            for a in attachments:
                self.assertEquals(a.file_name, 'test.txt')
                f = a.getAsFile()
                self.assertEquals(f.read(), content.encode('utf-8'))
                a.delete()

