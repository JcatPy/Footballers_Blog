from flaskblog import app

# This block checks if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Start the Flask development server
    # debug=True enables debug mode, which automatically restarts the server when code changes
    app.run(debug=True)