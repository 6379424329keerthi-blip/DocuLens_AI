"""
Standalone test runner using Python standard library unittest.
Allows running the test suite without requiring pytest installed.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_all_tests():
    print("=" * 65)
    print("DOCULENS AI — RUNNING INTEGRATION & UNIT TESTS")
    print("=" * 65)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover and add test functions wrapped in TestCase or run directly
    from tests import test_pdf_processor, test_retriever, test_evidence, test_qa

    class TestPDFProcessor(unittest.TestCase):
        def test_chunk_text(self):
            test_pdf_processor.test_chunk_text_preserves_metadata()
            test_pdf_processor.test_chunk_text_empty()

        def test_sample_processing(self):
            test_pdf_processor.test_process_pdf_on_sample_doc()

    class TestRetriever(unittest.TestCase):
        def test_retriever_metadata(self):
            test_retriever.test_retriever_preserves_page_metadata()

        def test_unique_pages(self):
            test_retriever.test_unique_pages()

        def test_format_evidence(self):
            test_retriever.test_format_evidence_for_llm()

    class TestEvidence(unittest.TestCase):
        def test_grounding(self):
            test_evidence.test_grounding_score_high_evidence()
            test_evidence.test_grounding_score_empty()

        def test_labels(self):
            test_evidence.test_confidence_labels()
            test_evidence.test_evidence_type_icons()
            test_evidence.test_format_evidence_card()

    class TestQA(unittest.TestCase):
        def test_visual_detection(self):
            test_qa.test_needs_visual_analysis_detection()

        def test_anti_hallucination(self):
            test_qa.test_unsupported_question_refusal()

    suite.addTests(loader.loadTestsFromTestCase(TestPDFProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestRetriever))
    suite.addTests(loader.loadTestsFromTestCase(TestEvidence))
    suite.addTests(loader.loadTestsFromTestCase(TestQA))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 65)
    if result.wasSuccessful():
        print(f"ALL TESTS PASSED ({result.testsRun} tests)")
    else:
        print(f"FAILED ({len(result.failures)} failures, {len(result.errors)} errors)")
    print("=" * 65)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
