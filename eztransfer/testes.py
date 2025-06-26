import tidalapi
import webbrowser as web

session:tidalapi.Session = tidalapi.Session()
login, future = session.login_oauth()
print('Você será redirecionado à página de login do Tidal para começar.')
web.open(login.verification_uri_complete)

while not future.result():
    continue

playlist = session.