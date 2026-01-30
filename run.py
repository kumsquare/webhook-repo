from app import create_app

app = create_app()

if __name__ == '__main__': 
    try:
        app.run(debug=True)
    #Gracefully handle manual shutdown (Ctrl+C) to suppress server thread traceback
    except KeyboardInterrupt:
        print("\nServer stopped manually")
    
