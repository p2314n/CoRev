from routes import create_app   # assuming package name is project

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)