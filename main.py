#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from ingredients import query_api
app = Flask(__name__)
@app.route('/')
def index():
    return render_template(
        'inputs.html',
        data=[{'name':'Toronto'}, {'name':'Montreal'}, {'name':'Calgary'},
        {'name':'Ottawa'}, {'name':'Edmonton'}, {'name':'Mississauga'},
        {'name':'Winnipeg'}, {'name':'Vancouver'}, {'name':'Brampton'}, 
        {'name':'Quebec'}])
@app.route("/result" , methods=['GET', 'POST'])
def result():
    error = None
    select = request.form.get('comp_select')
    data = query_api(select)
    return render_template(
        'result.html',
        tables=data,
        error=error,titles=['test1','test2'])
if __name__=='__main__':
    app.run(debug=True)