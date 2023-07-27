from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import db, string, random



app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    # ログイン判定
    if db.login(user_name, password):
        session['user'] = True      # session にキー：'user', バリュー:True を追加
        session.permanent = True    # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=10)   # session の有効期限を 1 分に設定
        return redirect(url_for('top'))
    else :
        error = 'ユーザ名またはパスワードが違います。'
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/top', methods=['GET'])
def top():
    # session にキー：'user' があるか判定
    if 'user' in session:
        return render_template('top.html') 
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト

@app.route('/logout')
def logout():
    session.pop('user', None)   # session の破棄
    return redirect(url_for('index'))   # ログイン画面にリダイレクト

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, user_name=user_name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)
    

# 図書登録
@app.route('/book_register')
def book_register():
    return render_template('book_register.html')

@app.route('/book_registr_exe', methods=['POST'])
def book_register_exe():
    name = request.form.get('name')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    
    if name == '':
        error = 'タイトルが未入力です。'
        return render_template('book_register.html', error=error, name=name)
    if author == '':
        error = '作者が未入力です。'
        return render_template('book_register.html', error=error, author=author)
    if publisher == '':
        error = '出版社が未入力です。'
        return render_template('book_register.html', error=error, publisher=publisher)
    
    count = db.insert_book(name,author,publisher)
    
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('top', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('book_register.html', error=error)
        
#図書一覧
@app.route('/book_list')
def book_list():
    book_list = db.book_list()
    return render_template('book_list.html', books=book_list)

# 図書削除
@app.route('/book_delete')
def book_delete():
    return render_template('book_delete.html')

@app.route('/book_delete_exe', methods=['POST'])
def book_delete_exe():
    name = request.form.get('name')
    db.book_delete(name)
    return render_template('top.html')


# 図書検索
@app.route('/book_search')
def book_search():
    return render_template('book_search.html')

@app.route('/book_search_exe', methods=['POST'])
def book_search_exe():
    name = request.form.get('name')
    
    book_search = db.book_search(name)
    return render_template('book_search_result.html', books=book_search, name=name)

if __name__ == '__main__':
    app.run(debug=True) 