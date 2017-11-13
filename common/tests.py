from django.test import TestCase

from .db import sql, page


class SQLTestCase(TestCase):
    fixtures = ('users.json',)

    users = (
        (1, 'admin'),
        (2, 'staff'),
        (3, 'test1'),
        (4, 'test2'),
        (5, 'test3'),
    )

    def test_single(self):
        result = sql('SELECT id FROM auth_user')
        data = {'data': tuple((d[0],) for d in self.users)}
        self.assertEqual(result, data)

    def test_multi(self):
        result = sql('SELECT id, username FROM auth_user')
        data = {'data': self.users}
        self.assertEqual(result, data)

    def test_param(self):
        result = sql('SELECT username FROM auth_user WHERE id = %s', 1)
        data = {'data': (('admin',),)}
        self.assertEqual(result, data)


class SQLPageTestCase(TestCase):

    def test_page_default(self):
        self.assertEqual(page(), ' LIMIT 20 OFFSET 0')

    def test_page_three(self):
        self.assertEqual(page(page=3), ' LIMIT 20 OFFSET 40')

    def test_page_unlimited(self):
        self.assertEqual(page(per_page=0), '')

    def test_page_sort(self):
        self.assertEqual(page(per_page=0, sort=('id',)), ' ORDER BY id')

    def test_page_sort_reverse(self):
        self.assertEqual(page(per_page=0, sort=('-id',)), ' ORDER BY id DESC')

    def test_page_sort_default(self):
        self.assertEqual(page(sort=('id',)), ' ORDER BY id LIMIT 20 OFFSET 0')
