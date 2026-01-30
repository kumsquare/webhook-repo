from app import create_app

app = create_app()

if __name__ == '__main__': 
    try:
        app.run(debug=True)
    except KeboardInterrupt:
        print("\nServer stopped manually")
    
