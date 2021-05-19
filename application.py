import random

from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response
from functools import wraps
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import flask
import string


app = Flask(__name__)

# here we just create a random value for the dash path
n = 200
num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
dash_value = f'/{num}/'


app_dash = dash.Dash(__name__, server=app, url_base_pathname=dash_value)


# dash app logic
app_dash.layout = html.Div([
    html.Div(html.H1('This is a very simple dash app page'), style={'text-align': 'center'}),

    html.Div(html.Button(id='set', n_clicks=0, children='1. Set default cookie'), style={'text-align': 'center'}),
    html.Div(id="set_cookies"),

    html.Div(html.Button(id='delete', n_clicks=0, children='2. Delete cookie'), style={'text-align': 'center'}),
    html.Div(id="delete_cookies"),

    html.Div(html.Button(id='cookie_page', n_clicks=0, children='3. Set your own cookie username'),
             style={'text-align': 'center'}),

    html.Div(id="cookie_page_redirect"),
    html.Div(html.Button(id='get', n_clicks=0, children='3. Extract user from cookie'), style={'text-align': 'center'}),
    html.Div(id="get_page_redirect"),

    html.Div(html.Button(id='logout', n_clicks=0, children='4. Log out'), style={'text-align': 'center'}),
    html.Div(id="logout_page_redirect")
])


# this segment of code is responsible for setting the users cookies
@app_dash.callback(Output('set_cookies', 'children'),
                   Input('set', 'n_clicks'))
def logout(n_clicks):
    if n_clicks:
        value = dash.callback_context.response.set_cookie(
            'userID', 'mr.Robinson')

        return value

    else:
        return []


# this segment of code is responsible for deleting the users cookies (important for the sign out part)
@app_dash.callback(Output('delete_cookies', 'children'),
                   Input('delete', 'n_clicks'))
def delete(n_clicks):
    if n_clicks:
        value = dash.callback_context.response.set_cookie(
            'userID', expires=0)

        return value

    else:
        return []


# this segment of code redirects the user to the cookie form page
@app_dash.callback(Output('cookie_page_redirect', 'children'),
                   Input('cookie_page', 'n_clicks'))
def logout(n_clicks):
    if n_clicks:
        return dcc.Location(pathname="/cookie", id="id1")

    else:
        return []


# this segment of code redirects the user to a page where he can see the userID extracted from the cookie
@app_dash.callback(Output('get_page_redirect', 'children'),
                   Input('get', 'n_clicks'))
def logout(n_clicks):
    if n_clicks:
        return dcc.Location(pathname="/getcookie", id="id2")

    else:
        return []


# this segment of code logs the user out and redirects him to the login page
@app_dash.callback(Output('logout_page_redirect', 'children'),
                   Input('logout', 'n_clicks'))
def logout(n_clicks):
    if n_clicks:
        return dcc.Location(pathname="/logout", id="id3")

    else:
        return []


# login logic
app.secret_key = 'the answer to the meaning of life, the universe, and everything is 42'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'user' or request.form['password'] != 'test':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('dashboard_main'))
    return render_template('login.html', error=error)


@app.route('/redirect')
@login_required
def dashboard_main():
    return redirect(url_for('dashboard_alpha'))


@app.route('/main')  # the dash path isn't actually secured, because dash overwrites the flask path
@login_required
def dashboard_alpha():
    return flask.redirect(dash_value)


@app.route('/cookie')
@login_required
def index():
   return render_template('cookie.html')


@app.route('/setcookie', methods=['POST', 'GET'])
@login_required
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']

    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)

    return resp


@app.route('/getcookie')
@login_required
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome  ' + name + '</h1>'


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
