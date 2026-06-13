import numpy as np
from analyzer import (
    split_sentences,
    lambda_score,
    tau_score,
    rho_score,
    normalize,
    analyze_text,
    detect_twists,
)


def test_split_sentences():
    text = "First sentence. Second one! Third?"
    result = split_sentences(text)
    assert result == ["First sentence.", "Second one!", "Third?"]


def test_split_single_sentence():
    assert split_sentences("Only one.") == ["Only one."]


def test_lambda_score_with_logic_words():
    assert lambda_score("bo dlatego jednak") == 3


def test_lambda_score_no_match():
    assert lambda_score("zwykly tekst bez slow logicznych") == 0


def test_tau_score_with_time_words():
    assert tau_score("potem nastepnie pozniej") == 3


def test_tau_score_no_match():
    assert tau_score("zwykly tekst") == 0


def test_rho_score_long_words():
    assert rho_score("krotkie a dlugiewyrazenie bardzodlugiewyrazenie") == 2


def test_rho_score_short_words():
    assert rho_score("a b c d e") == 0


def test_normalize_basic():
    result = normalize([0, 5, 10])
    np.testing.assert_array_almost_equal(result, [0.0, 0.5, 1.0])


def test_normalize_all_zeros():
    result = normalize([0, 0, 0])
    np.testing.assert_array_almost_equal(result, [0.0, 0.0, 0.0])


def test_analyze_text_returns_correct_count():
    text = "Pierwsze zdanie. Drugie zdanie. Trzecie zdanie."
    results = analyze_text(text)
    assert len(results) == 3


def test_analyze_text_attributes():
    text = "Jedno zdanie."
    results = analyze_text(text)
    r = results[0]
    assert r.sentence == "Jedno zdanie."
    assert isinstance(r.lam, (float, np.floating))
    assert isinstance(r.tau, (float, np.floating))
    assert isinstance(r.rho, (float, np.floating))


def test_detect_twists_no_twist():
    text = "Ala ma kota. Ala ma psa."
    analyses = analyze_text(text)
    twists = detect_twists(analyses, threshold=10.0)
    assert twists == []


def test_detect_twists_with_twist():
    text = "Zwykly tekst. Bo dlatego jednak potem nastepnie bardzodlugiewyrazenie superdlugiewyrazenie."
    analyses = analyze_text(text)
    twists = detect_twists(analyses, threshold=0.1)
    assert len(twists) > 0
    assert all(isinstance(t, int) for t in twists)


def test_detect_twists_indices_in_range():
    text = "A. B. C. D. E."
    analyses = analyze_text(text)
    twists = detect_twists(analyses, threshold=0.0)
    for t in twists:
        assert 1 <= t < len(analyses)


