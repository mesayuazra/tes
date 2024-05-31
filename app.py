import requests
from bs4 import BeautifulSoup
from http import client
from pymongo import MongoClient
from flask import Flask,redirect,url_for,render_template,request,jsonify
from bson import ObjectId

client = MongoClient('mongodb+srv://test:sparta@cluster0.ljefanz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbproject1

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
  return render_template('index.html')

@app.route('/books',methods=['POST'])
def books_post():
  url_receive = request.form['url_give']
  rating_receive = request.form['rating_give']
  comment_receive = request.form['comment_give']
  
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
  data = requests.get(url_receive,headers=headers)

  soup = BeautifulSoup(data.text, 'html.parser')

  og_image = soup.select_one('meta[property="og:image"]')
  og_title = soup.select_one('meta[property="og:title"]')

  image = og_image['content']
  title = og_title['content']
  
  doc = {
    'image': image,
    'title': title,
    'rating': rating_receive,
    'comment': comment_receive,
  }
  
  db.books.insert_one(doc)
  
  return jsonify({'msg': 'Book Posted!'})

@app.route('/books',methods=['GET'])
def books_get():
  books_list = list(db.books.find({},{'_id': False})) 
  return jsonify({'books': books_list})

@app.route('/update/books',methods=['GET','POST'])
def books_update():
  return render_template('detail.html')

@app.route('/delete/books',methods=['POST'])
def books_delete():
  id_receive = request.form['id']
  db.books.delete_one({'_id': ObjectId(id_receive)})
  return jsonify({'msg': 'This book is deleted!'},
                 {'id': id_receive})
  
@app.route('/pembagian',methods=['POST'])
def pembagian():
  num1 = int(request.form['num1'])
  num2 = int(request.form['num2'])
  result = num1/num2
  return jsonify({'result': result})

@app.route('/pembagian',methods=['GET'])
def pembagian_get():
  num1 = request.args.get(num1)
  num2 = request.args.get(num2)
  result = request.args.get(num2)
  return jsonify({'msg': 'hasil dari pembagian tersebut adalah '})

@app.route('/gender',methods=['GET','POST'])
def gender(gen):
  if gen == 'female':
    return jsonify({'msg': 'wanita ges'})
  else:
    return jsonify({'msg': 'laki2'})

if __name__ == '__main__':
  #DEBUG is SET to TRUE. CHANGE FOR PROD
  app.run('0.0.0.0',port=5000,debug=True)