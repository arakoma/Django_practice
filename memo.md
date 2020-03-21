# 環境
- python 3.7  
- Django==2.2.4  
- venv  

# project作成
フォルダで  
- linux  
  `django-admin startproject mysite .`  
- windows  
  `django-admin.exe startproject mysite .`
  
を実行。（"mysite"は任意の名前）  
すると、フォルダ内にmysiteフォルダとpyファイルが作られる。  
  
# 設定変更  
mysite/setting.pyが設定のファイル。ちょっと変更する。  
- タイムゾーン  
  `TIME_ZONE = 'Asia/Tokyo'`  
- 言語  
  `LANGUAGE_CODE = 'ja'`  
- 静的ファイルのpath  
  `STATIC_URL = '/static/'`
  `STATIC_ROOT = os.path.join(BASE_DIR, 'static') #追加`  
- pythonanywhereにデプロイする場合、ホストネーム追加  
  `ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']`  
  空リストの時は['localhost', '127.0.0.1', '[::1]']に対してチェックが行われる。  


# データベースのセットアップ  
Djangoデフォルトのsqlite3を使う。  
(設定はmysite/setting.pyにあるDATABASES)  
  
`python manage.py migrate`を実行でセットアップok  

# webサーバ起動！！！  
`python manage.py runserver`を実行でwebサーバ起動。  
ブラウザで`http://127.0.0.1:8000/`を開くとページ出るはず。  
  

# ブログポストの機能をつくっていく  
Djangoモデルとして作る。  
(Djangoのモデルはデータベースに格納される。)  

## project内にアプリケーションを作る  
`python manage.py startapp blog`を実行("blog"は任意の名前)  
するとディレクトリが作られる。 

アプリ作ったらDjangoにそれを設定する。  
mysite/setting.py の INSTALLED_APPES に`'blog.apps.BlogConfig'`を追加する。  

## ブログポストモデルの作成  
blog/models.py でModelオブジェクトを全て定義する。  
(今回はPostクラスを作成)  

## 新しいモデルをデータベースに追加  
モデルの変更(作成)をDjangoに追加。  
`python manage.py makemigrations blog`を実行。  
(nnnn_initial.py が作成される。)  

作成された移行ファイルをデータベースに追加する。 
`python manage.py migrate blog`を実行。  
(コンソールに…okとかでればok。モデルがデータベースに入った。)  


# Django admin を使う  
今追加した機能を見ていく！！！  
そのためにadminで入っていきましょう。

blog/admin.py を変更する。  
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```
(これでadminでのレジができる。)  
  
webサーバ立てて(`python manage.py runserver`)  
ブラウザでhttp://127.0.0.1:8000/admin/ にアクセス。    
するとDjango administration の画面が出るはず。  

ログインするためにsuperuser(管理ユーザー)を作る。  
`python manage.py createsuperuser`を実行。  
ユーザー名、メールアドレス、パスワード、を入力。  
これでログインできるようになる。  

webに戻ってログイン、Postもできるはず。  

とりあえずこれで初めてのDjangoモデルできた！！！！！！！  
  

# デプロイ！！！  
一旦略  

# Django URL  
mysite/urls.py にadminのURLは書かれてる。  
admin でURLを追加していくよ！  
ただ、このファイルは簡潔にしておきたいのでblog.urlsへリダイレクトさせる。  
  
blogフォルダ内にurls.pyファイルを作る。  
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
]
```
'post_list'という名前のviewをルートURLに割り当ててる。  
('http://127.0.0.1:8000/' の部分は省略されてる)  
(ここでやったのは、ルートURLにアクセスしたらviews.post_list('post_list'という名前のview)に飛ばす設定)  
  
この状態でrunserverするとエラーでます。  
(viewsにpost_listなんてもんはねえyo！って言われる。作ってないし…)  

じゃあviewsを作っていきましょう～！  

# Django view
viewはview.pyに書く。  
blog/view.pyに関数として書いていけばおーけー。  
```python
def post_list(request):
    return render(request, 'blog/post_list.html', {})
```
'blog/post_list.html'というテンプレートをrender関数にいれて返す。  
  
ここでrunserverすると、テンプレートねえyoって言われる。  
  
じゃあテンプレートつくっていきましょう～！  
  
# テンプレート (HTML)
blog/templates/blog/post_list.html にhtmlで書く。  
  
# Django ORM, クエリセット
Djangoのデータベース、データの格納についてやっていく！  
## クエリセット？
クエリセット：モデルのオブジェクトのリストのこと。これを使ってデータベースからデータ読んだり抽出したり並べ替えたりできる。  
よくわからんので動かしてみましょう～！  
## Django Shell
コンソールで`python manage.py shell`実行でDjangeのインタラクティブコンソール入れる。  
- オブジェクトの表示  
- オブジェクトの作成  
- オブジェクトの抽出  
- オブジェクトの並び替え  
- メソッドチェーンで複雑なクエリ  
  

# テンプレート内の動的データ  
post_list.htmlではPostされた記事をリストで表示したい。  
けど、htmlに毎回自分で加えるわけにはいかないでしょ…？  
なので、動的にテンプレートが変わるようにしたいです。  
  
## views.py に書き加える
views.py の post_list() で、記事をクエリセットとして変数に入れてテンプレートに渡す。  
(views.pyの変更みて)  

## Djangoテンプレート
Djangoテンプレートタグを使うと、__htmlにpythonコードを埋め込める！！！！！__  
Djangoテンプレートでは、  
- 変数  
  {{}}でくくる。`{{ post }}`  
- ループ  
  ```
  {%for post in posts%}
      {{ post }}
  {% endfor %}
  ```
こんな感じで書けるよ！！！  
post_list.html をこれで書いてみる。  
```html
{% for post in posts%}
      <div>
            <h2><a href="">{{ post.title }}</a></h2>
            <p>published: {{ post.published_date }}</p>
            <p>{{ post.text|linebreaksbr }}</p>
      </div>
{% endfor %}
```
  
# CSS
htmlだけだとシンプル杉って感じ。  
CSSで見た目をおしゃれにしましょうか。  
  
## Bootstrap
Bootstrap: htmlとcssのフレームワーク  

## Djangoの静的ファイル
Djangoはアプリ内で"static"という名前のフォルダを探し、その中のを静的ファイルとして使う。  
blog/static/css/blog.css を作る。  
いろいろいじる、たのしい！！！！！！！！  

# テンプレート拡張
htmlの共通部分を拡張としてつかえる。  
base.htmlを元として、そのなかのblockを書いたものをpost_list.htmlとする。baseがさき、post_listがあと。  

拡張としたい部分を　　
```
{% block content %}
{% endblock %}
```
で囲む。  
(拡張先のこれ書いた部分が、拡張元のこの部分になる。)  
拡張元ファイルの先頭に  
`{% extends 'blog/base.html' %}`  
これで参照される。  

# アプリ追加しよう
ここまででおわり！！！(モデル、URL、ビュー、テンプレート、)  
もうなんでもつくれるよ！！！  
