"""Tests for the phonemes module."""

from unittest import TestCase, skip

import spacy
from spacy.tokens import Doc, Span, Token

from dphon.phonemes import Phonemes


class TestPhonemes(TestCase):
    """Test the phonemes spaCy pipeline component."""

    px: Phonemes

    def setUp(self) -> None:
        """Create a blank spaCy pipeline and sound table to use in tests."""
        self.nlp = spacy.blank("en")
        self.sound_table = {
            "1": ("w", "ʌn"),
            "2": ("t", "uː"),
            "3": ("θ", "riː"),
            "one": ("w", "ʌn"),
            "two": ("t", "uː"),
            "three": ("θ", "riː"),
            "to": ("t", "uː"),
            "too": ("t", "uː"),
        }

    def tearDown(self) -> None:
        """Unregister the component to prevent name collisions."""
        if hasattr(self, "px"):
            self.px.teardown()

    @skip("todo")
    def test_defaults(self) -> None:
        """should populate name and attr by default"""
        pass
        #  self.px = Phonemes(self.nlp, )

    def test_are_graphic_variants(self) -> None:
        """should correctly detect if a set of tokens are graphic variants"""
        self.px = Phonemes(self.nlp, self.sound_table)
        doc1 = self.nlp.make_doc("that's two now!")
        doc2 = self.nlp.make_doc("2 too many")
        doc3 = self.nlp.make_doc("one to remember")
        # "two" and "too" rhyme, so (theoretically) could be variants
        self.assertTrue(self.px.are_graphic_variants(doc1[2], doc2[1]))
        # "two", "too", "to", and "2" could all be variants
        self.assertTrue(self.px.are_graphic_variants(doc1[2], doc2[1], doc2[0], doc3[1]))
        # "too" and "too" aren't variants because they're the same word
        self.assertFalse(self.px.are_graphic_variants(doc2[1], doc2[1]))
        # "one" isn't a variant of the above because it sounds different
        self.assertFalse(self.px.are_graphic_variants(doc1[2], doc2[1], doc3[0]))
        # "!" isn't voiced, so it can't be a variant
        self.assertFalse(self.px.are_graphic_variants(doc1[2], doc2[1], doc1[4]))
        # "remember" isn't in our table, so it can't be a variant
        self.assertFalse(self.px.are_graphic_variants(doc1[2], doc2[1], doc3[2]))