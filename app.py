from website import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True)
