#Import from website package
from website import create_app

# * Run Flask App
app = create_app()
# ? Condition below is true only if main.py in run directly
if __name__ == '__main__':
    # * Start web sever
    app.run('0.0.0.0', port=8090)
    # ? debug=True to keep rerunning coding when we change code
    # ! host='0.0.0.0' in production
