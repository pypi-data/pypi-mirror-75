import unittest
from django.test import TestCase
from unittest.mock import Mock, patch, MagicMock
from xchk_regex_strategies.strats import RegexCheck
from xchk_core.models import SubmissionV2

class RegexCheckTest(TestCase):

    def setUp(self):
        self.txt_vs_regex_check = RegexCheck()

    def _model_and_student_mock(self,model,student):
        base_mock = MagicMock(name='mock for open')
        mock_context_manager_1 = MagicMock(name='mock for context manager 1')
        mock_context_manager_1.__enter__.return_value.read.return_value = model
        mock_context_manager_2 = MagicMock(name='mock for context manager 2')
        mock_context_manager_2.__enter__.return_value.read.return_value = student
        base_mock.side_effect=[mock_context_manager_1, mock_context_manager_2]
        return base_mock

# TODO: belongs in Git content app
    def test_non_dutch_language_link(self):
        # everything but two letters n and l is allowed by this regex
        link = r"""https://git\-scm\.com/book/([^n].+|n[^l].*|nl[^/].+)/v2"""
        text = r"""https://git-scm.com/book/en/v2"""
        base_mock = self._model_and_student_mock(link,text)
        submission = SubmissionV2()
        with patch('builtins.open',base_mock):
            outcome_analysis = self.txt_vs_regex_check.check_submission(submission,'/tmp/student','/tmp/model',True,1,False)
            self.assertTrue(outcome_analysis.outcome)

# TODO: belongs in Git content app
    def test_prohibited_dutch_language_link(self):
        # everything but two letters n and l is allowed by this regex
        link = r"""https://git\-scm\.com/book/([^n].+|n[^l].*|nl[^/].+)/v2"""
        text = r"""https://git-scm.com/book/nl/v2"""
        base_mock = self._model_and_student_mock(link,text)
        submission = SubmissionV2()
        with patch('builtins.open',base_mock):
            outcome_analysis = self.txt_vs_regex_check.check_submission(submission,'/tmp/student','/tmp/model',True,1,False)
            self.assertFalse(outcome_analysis.outcome)

# TODO: belongs in Git content app
    def test_non_link(self):
        # everything but two letters n and l is allowed by this regex
        link = r"""https://git\-scm\.com/book/([^n].+|n[^l].*|nl[^/].+)/v2"""
        text = r"""https://ubuntu.com"""
        base_mock = self._model_and_student_mock(link,text)
        submission = SubmissionV2()
        with patch('builtins.open',base_mock):
            outcome_analysis = self.txt_vs_regex_check.check_submission(submission,'/tmp/student','/tmp/model',True,1,False)
            self.assertFalse(outcome_analysis.outcome)

if __name__ == '__main__':
    unittest.main()
