# coding: utf-8
from otrs_somconnexio.otrs_models.abstract_article import AbstractArticle


class MMErrorArticle(AbstractArticle):
    """
    Creates an article with the MM error data.

    error -> dictionary comming from the MM API with the error description
    object -> String that indicates which object failed: creation of account, order-item or asset
    """
    def __init__(self, error, object):
        self.error = error
        self.object = object
        self.subject = "Error desde Mas Móvil en la creació d'un/a {}".format(self.object)
        self.body = self.error['message']
        self.df = [
            {
                "Name": 'statusCode',
                "Value": self.error['statusCode']
            },
            {
                "Name": 'fields',
                "Value": self.error['fields']
            }
        ]
