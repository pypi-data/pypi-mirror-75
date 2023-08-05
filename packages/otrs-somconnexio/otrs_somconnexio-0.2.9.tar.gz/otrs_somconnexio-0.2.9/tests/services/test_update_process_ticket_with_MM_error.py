# coding: utf-8
import unittest

from mock import Mock, patch

from otrs_somconnexio.services.update_process_ticket_with_MM_error import UpdateProcessTicketWithMMError


class UpdateProcessTicketWithMMErrorTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_error.OTRSClient', return_value=Mock(spec=['update_ticket']),
           )
    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_error.MMErrorArticle')
    def test_run(self, MockMMErrorArticle, MockOTRSClient):

        ticket_id = '1111'
        object_str = "OrderItem"
        expected_error = {
            "statusCode":"400",
            "message":"El documentType no contiene un valor apto: 2",
            "fields":"documentType"
        }

        mock_MM_error_article = Mock(spec=['call'])
        MM_error_article = object()

        def mock_MM_error_article_side_effect(error, object):
            if error == expected_error and object_str == "OrderItem":
                mock_MM_error_article.call.return_value = MM_error_article
                return mock_MM_error_article

        MockMMErrorArticle.side_effect = mock_MM_error_article_side_effect

        UpdateProcessTicketWithMMError(ticket_id, expected_error, object_str).run()

        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            ticket_id,
            MM_error_article
        )
