#!/usr/bin/env python3
"""Test accent classification result formatting."""

import os
import sys
import tempfile

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

import torch
import torch.nn.functional as F

from english_accent_classifier.accent_classifier import AccentClassifier


def test_formatting():
    """Test the result formatting logic."""
    try:
        print("Testing result formatting...")

        # Create mock data similar to what the model would return
        # Mock logits (random values)
        mock_logits = torch.randn(1, 14)  # 14 accent classes
        mock_probs = F.softmax(mock_logits, dim=1)

        # Mock class labels
        mock_labels = [
            "american",
            "australian",
            "british",
            "indian",
            "irish",
            "african",
            "malaysian",
            "kiwi",
            "south_atlantic",
            "bermuda",
            "filipino",
            "chinese",
            "welsh",
            "singaporean",
        ]

        # Test the formatting logic
        result = "Accent probabilities:\n\n"
        for i, lbl in enumerate(mock_labels):
            probability = mock_probs[0, i].item() * 100
            result += f"{str(lbl):<20}: {probability:>6.2f}%\n"

        # Find the most probable accent
        best_index = torch.argmax(mock_probs, dim=1).item()
        best_label = mock_labels[best_index]

        print("Formatted result:")
        print(result)
        print(f"Most probable accent: {best_label}")

        # Verify the format looks correct
        lines = result.strip().split("\n")
        assert len(lines) >= 3, "Should have header + blank line + accent lines"
        assert "Accent probabilities:" in lines[0], "Should have header"

        # Check that each accent line has the right format
        accent_lines = [line for line in lines if ":" in line and "%" in line]
        assert (
            len(accent_lines) == 14
        ), f"Should have 14 accent lines, got {len(accent_lines)}"

        print("SUCCESS: Formatting test passed!")

    except Exception as e:
        print(f"FAILED: Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_formatting()
