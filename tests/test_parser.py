from alerta_chuva.parser.normalize_text import normalize_text


def test_normalize_text():
    # Teste com uma lista válida
    input_texts = ["Tue", "Oct", "31", "17:36:04", "2023"]
    expected_output = "Tue Oct 31 17:36:04 2023"
    result = normalize_text(input_texts)
    assert result == expected_output


def test_normalize_text_com_a_hora_quebrada():
    input_texts = ["Tue", "Oct", "31", "17", "36:04", "2023"]
    expected_output = "Tue Oct 31 17:36:04 2023"
    result = normalize_text(input_texts)
    assert result == expected_output
