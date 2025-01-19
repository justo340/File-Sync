from src.main import main

def test_integration():
    try:
        main()
        assert True
    except Exception as e:
        assert False, f"Integration test failed: {e}"
