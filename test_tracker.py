"""
Unit tests for tracker.py
Verifies query construction, issue fetching, fallback handling, and Copilot prompt generation.
"""

import unittest
from tracker import build_search_query, fetch_issues, generate_copilot_prompt, track_user_prs


class TestTracker(unittest.TestCase):

    def test_build_search_query_defaults(self):
        """Verify default search query includes hacktoberfest and good first issue."""
        query = build_search_query()
        self.assertIn("state:open", query)
        self.assertIn("label:hacktoberfest", query)
        self.assertIn('label:"good first issue"', query)

    def test_build_search_query_with_language_and_custom_label(self):
        """Verify language and custom label parameters."""
        query = build_search_query(language="python", label="documentation", query="fastapi")
        self.assertIn("language:python", query)
        self.assertIn('label:"documentation"', query)
        self.assertIn("fastapi", query)

    def test_fetch_issues_returns_valid_structure(self):
        """Verify fetched issues have required keys."""
        issues, source = fetch_issues(limit=3)
        self.assertIsInstance(issues, list)
        self.assertTrue(len(issues) > 0)
        first = issues[0]
        self.assertIn("title", first)
        self.assertIn("repo", first)
        self.assertIn("url", first)
        self.assertIn("labels", first)

    def test_generate_copilot_prompt(self):
        """Verify Copilot prompt format contains key prompt engineering elements."""
        sample_issue = {
            "title": "Fix authentication header parsing error",
            "repo": "example/project",
            "url": "https://github.com/example/project/issues/42",
        }
        prompt = generate_copilot_prompt(sample_issue)
        self.assertIn("GitHub Copilot Chat Prompt", prompt)
        self.assertIn("Fix authentication header parsing error", prompt)
        self.assertIn("example/project", prompt)
        self.assertIn("Arrange-Act-Assert", prompt)

    def test_track_user_prs_farhan(self):
        """Verify Farhan's milestone tracking."""
        count, prs = track_user_prs("farhanmallik05")
        self.assertGreaterEqual(count, 3)
        self.assertTrue(any("getting-started-with-github-copilot" in pr["html_url"] for pr in prs))


if __name__ == "__main__":
    unittest.main()
