import sys

sys.path.insert(0, '/usr/local/lib/python3.9/site-packages')
import mysql.connector
from flask import Flask, render_template, request, redirect

new_new_id = 0

# 配置数据库连接
db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_name",
    password="your_mysql_password",
    database="your_database_name"
)

app = Flask(__name__)


# 登录路由
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # 在数据库中查询用户信息
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM username WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()

        # 检验是否有其他结果集
        while cursor.nextset():
            pass

        cursor.close()
        db.commit()
        # db.close()

        if user:
            # 登录成功，重定向到目标页面
            return redirect("https://www.baidu.com/")
        else:
            # 登录失败，返回错误消息
            return "用户名或密码错误,请检查后重新登陆"
    else:
        if request.args.get("register"):
            # 如果检测到 "去注册" 的链接被点击
            return redirect("/register")
        else:
            return render_template("login.html")


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


# 验证码路由
@app.route("/get_verification_code", methods=["POST"])
def get_verification_code():
    phone = request.form["phone"]

    cursor = db.cursor()
    cursor.execute("SELECT MAX(id) FROM username")
    max_id = int(cursor.fetchone()[0])
    # cursor.execute("SELECT phone from username")
    #
    # phones = cursor.fetchall()
    #
    # for iphone in phones:
    #     iphones = iphone[0]
    #     if iphones == phone:
    #         return "存在相同手机号，请联系管理员删除"
    new_id = max_id + 1
    global new_new_id
    new_new_id = new_id
    while cursor.nextset():
        pass
    cursor.execute("INSERT INTO username (id,  phone) VALUES (%s, %s)",
                   (new_id, phone))

    while cursor.nextset():
        pass

    db.commit()
    return "请联系客服获取验证码"


# 注册路由
@app.route("/register", methods=["POST"])
def register():
    phone = request.form["phone"]
    username = request.form['username']
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    verification_code = request.form["verification_code"]

    # 查询数据库判断用户名是否存在
    cursor = db.cursor()
    cursor.execute("SELECT * FROM username WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        # 用户名已存在,返回特殊代码到前端
        return '{"code": 1, "msg": "用户名已存在，请重新输"}'

    # 验证验证码
    # 验证码固定值
    if verification_code == "9909":
        # 验证密码是否一致
        if password == confirm_password:
            username = request.form['username']  # 从表单中获取用户名
            password = request.form['password']  # 从表单中获取密码
            phone = request.form['phone']  # 从表单中获取手机号

            # 执行插入语句
            cursor = db.cursor()
            cursor.execute("INSERT INTO username (id, username, password, phone) VALUES (%s, %s, %s, %s) \
                            ON DUPLICATE KEY UPDATE username = VALUES(username), password = VALUES(password), phone = VALUES(phone)",
                           (new_new_id, username, password, phone))
            db.commit()

            cursor.close()
            # db.close()

            # 注册成功，重定向到登录页面
            return redirect("/")
        else:
            # 密码不一致，返回错误消息
            return "密码不一致请重新输入"
    else:
        # 验证码不正确，返回错误消息
        return "验证码不正确,请输入正确的验证码"


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/blank_page")
def blank_page():
    return "Blank Page"


if __name__ == '__main__':
    app.run(host='服务器内网地址', port=5000)
