import pytest
import requests

# 可以不加headers，这个网站不挡，但加一个保险
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


def test_get_single_user():
    # GET 查询用户id=2
    response = requests.get("https://jsonplaceholder.typicode.com/users/2", headers=headers)

    assert response.status_code == 200

    json_data = response.json()

    # 检查返回数据（id=2的用户叫Leanne Graham）
    assert json_data["id"] == 2
    assert json_data["name"] == "Ervin Howell"  # 注意：id=2是Ervin Howell（官网数据）
    assert json_data["email"] == "Shanna@melissa.tv"

    print("单个用户查询成功！")


def test_user_not_found():
    # GET 查询不存在的用户id=999
    response = requests.get("https://jsonplaceholder.typicode.com/users/999", headers=headers)

    # 现在不存在返回404
    assert response.status_code == 404

    # body应该是空的
    assert response.text == "" or response.json() == {}

    print("不存在用户，返回404正确！")


def test_create_post():
    # POST 创建新帖子
    payload = {
        "title": "我的测试帖子",
        "body": "这是自动化测试创建的内容",
        "userId": 1
    }

    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload, headers=headers)

    assert response.status_code == 201

    json_data = response.json()
    assert json_data["title"] == "我的测试帖子"
    assert json_data["body"] == "这是自动化测试创建的内容"
    assert json_data["userId"] == 1
    assert "id" in json_data  # 创建成功会返回新id（如101）

    print("创建帖子成功！")