from contextlib import contextmanager

from bs4 import BeautifulSoup
from django.test import TestCase


class BaseTestCase(TestCase):
    @staticmethod
    def css_select_get_text(response, css_selector):
        soup = BeautifulSoup(response.content, features='html.parser')
        text_groups = []
        for element in soup.select(css_selector):
            text_groups.append(element.text.strip())
        return text_groups

    @staticmethod
    def css_select_get_attributes(response, css_selector, attributes):
        soup = BeautifulSoup(response.content, features='html.parser')
        result = []
        for element in soup.select(css_selector):
            attr_dict = {}
            for attribute in attributes:
                attr_dict[attribute] = element.attrs.get(attribute, None)
            result.append(attr_dict)
        return result

    @contextmanager
    def assert_num_objects_created(self, counts):
        before_counts = {}
        after_counts = {}
        for Model in counts:
            before_counts[Model] = Model.objects.count()
        yield
        for Model in counts:
            after_counts[Model] = Model.objects.count()
        for Model in counts:
            delta = after_counts[Model] - before_counts[Model]
            self.assertEqual(delta, counts[Model], Model)
