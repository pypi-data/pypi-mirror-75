# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.mm_error_article import MMErrorArticle

class MMErrorArticleTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_call(self, MockArticle):

        fake_error = {
           "statusCode":"400",
           "message":"El documentType no es un valor válido: 2",
           "fields":"documentType"
        }
        expected_article_arguments = {
            "Subject": "Error desde Mas Móvil en la creació d'un/a Account",
            "Body": "El documentType no es un valor válido: 2",
            "ContentType": "text/plain; charset=utf8",
            "DynamicField": [
                {
                    "Name": "statusCode",
                    "Value": "400"
                },
                {
                    "Name": "fields",
                    "Value": "documentType"

                }
            ]
        }

        MMErrorArticle(fake_error, "Account").call()
        MockArticle.assert_called_once_with(expected_article_arguments)
