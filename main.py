#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from output_generator import output

app = Flask(__name__)
@app.route('/')
def index():
    return render_template(
        'inputs.html',
        mouths=[1,2,3,4,5],percentages = ['0%','25%','50%','75%','100%'],yesno = ['yes','no'])
@app.route("/result" , methods=['GET', 'POST'])
def result():
    error = None
    inputs = {}
    inputs['s_mouths'] = request.form.get('mouths')
    inputs['s_lunch_p'] = request.form.get('lunch_p')
    inputs['s_dinner_p'] = request.form.get('dinner_p')
    inputs['s_veg'] = request.form.get('veg')
    inputs['s_gf'] = request.form.get('gf')
    data = output(inputs)
    return render_template(
        'result.html',
        tables=data,
        error=error,titles=['test1','test2'])
if __name__=='__main__':
    app.run(debug=True)