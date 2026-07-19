from datetime import time

import parse


def test_findall():
    s = "".join(
        r.fixed[0] for r in parse.findall(">{}<", "<p>some <b>bold</b> text</p>")
    )
    assert s == "some bold text"


def test_no_evaluate_result():
    s = "".join(
        m.evaluate_result().fixed[0]
        for m in parse.findall(
            ">{}<", "<p>some <b>bold</b> text</p>", evaluate_result=False
        )
    )
    assert s == "some bold text"


def test_case_sensitivity():
    l = [r.fixed[0] for r in parse.findall("x({})x", "X(hi)X")]
    assert l == ["hi"]

    l = [r.fixed[0] for r in parse.findall("x({})x", "X(hi)X", case_sensitive=True)]
    assert l == []


def test_findall_tt_skips_zero_width_matches():
    # Optional {:tt} can match "" ; findall must advance or it loops forever.
    assert list(parse.findall("{:tt}", "hello")) == []
    assert list(parse.findall("{:tt}", "")) == []
    assert list(parse.findall("{:tt}", "..")) == []
    times = [r.fixed[0] for r in parse.findall("{:tt}", "meet 10:30 or 14:00")]
    assert times == [time(10, 30), time(14, 0)]
