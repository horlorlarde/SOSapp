try:
    from app import create_app
    print("App imported successfully")
    
    app, socketio = create_app()
    print("App created successfully")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()