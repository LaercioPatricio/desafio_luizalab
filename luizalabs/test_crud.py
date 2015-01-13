# -*- coding: utf-8 -*-
import random
import unittest
from person.models import Person
import os
import logging
import core.utils as utils
import tornado.ioloop
import tornado.httpserver
import tornado.options
import person.models.personmodel as pmodel
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import settings
import sys
import shutil
from person.handlers import PersonHandler


class PersonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # duplica banco para teste
        duplicate_name = settings.DATABASE_STRING+'_dp.sqlite'
        shutil.copy2(settings.DATABASE_STRING, duplicate_name)
        settings.DATABASE_STRING = duplicate_name

    @classmethod
    def tearDownClass(cls):
        # remove duplicidade
        if settings.DATABASE_STRING.endswith('_dp.sqlite'):
            os.remove(settings.DATABASE_STRING)

    def clean_occurrence(self):
        for i in Person.all(
            self._data_access,
            facebookId=self.facebookId_unittest
            ):
            i.delete(self._data_access)

    def setUp(self):
        self.facebookId_unittest = 123456
        self.facebookId_unittest_invalid = '123456s'
        engine = create_engine(
            settings.config['database_path'],
            convert_unicode=True,
            echo=settings.config['debug']
            )
        pmodel.init_db(engine)
        self._data_access = scoped_session(sessionmaker(bind=engine))

    def test_insert(self):
        person = Person(
            name='ted',
            username='ted',
            gender='male',
            facebookId=self.facebookId_unittest
            )
        inserted_pk = person.save(self._data_access)
        self.assertGreater(inserted_pk, 0)

    def test_request_item(self):
        person = Person.one(
            self._data_access,
            facebookId=self.facebookId_unittest
            )
        self.assertEqual(
            person.name,
            'ted',
            'usuario ja inserido anteriormente'
            )

    def test_request_items(self):
        persons = Person.all(
            self._data_access,
            facebookId=self.facebookId_unittest
            )
        self.assertGreater(len(persons), 0)

    def test_request_items_count(self):
        persons_counter = Person.count(self._data_access)
        self.assertGreater(persons_counter, 0)

    def test_delete(self):
        person = Person.one(
            self._data_access,
            facebookId=self.facebookId_unittest)
        deleted = person.delete(self._data_access)
        self.assertTrue(
            deleted,
            'usuario nao estava na base conforme esperado'
            )

    def test_pagination(self):
        paginator = utils.Pagination(
            page=1,
            limit=20,
            total_count=100
            )
        self.assertEqual(paginator['pages'], 5)
        self.assertTrue(paginator['has_next'])
        self.assertFalse(paginator['has_preview'])

        paginator = utils.Pagination(
            page=5,
            limit=20,
            total_count=100
            )
        self.assertFalse(paginator['has_next'])
        self.assertTrue(paginator['has_preview'])

    def test_init(self):
        self.assertEqual('1', '1')


def suite_person():
    suite = unittest.TestSuite()
    suite.addTest(PersonTest('test_insert'))
    suite.addTest(PersonTest('test_request_item'))
    suite.addTest(PersonTest('test_request_items'))
    suite.addTest(PersonTest('test_request_items_count'))
    suite.addTest(PersonTest('test_delete'))
    suite.addTest(PersonTest('test_pagination'))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite_person())
