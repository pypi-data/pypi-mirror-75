import os, webbrowser, time, multiprocessing


def run():
    os.environ["FLASK_APP"] = "satyrn_flask.satyrn_flask"
    os.environ["FLASK_ENV"] = "production"

    p = multiprocessing.Process(target=os.system,
                                args=("waitress-serve --call --host='127.0.0.1' --port=20787 "  # i^i
                                      "'satyrn_flask.satyrn_flask:create_app'",))
    p.start()
    time.sleep(3)

    webbrowser.open("http://localhost:20787/")


if __name__ == "__main__":
    run()
