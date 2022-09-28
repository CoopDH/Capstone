from website import create_app

app = create_app()

#limits the launching of the server only if main.py is ran 
if __name__ == '__main__':
    app.run(debug=True)