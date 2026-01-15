def test_app_import():
    from src.ui.app import create_app
    app = create_app()
    assert app is not None
