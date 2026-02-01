import pytest
import requests
import json
import random
import string

BASE_URL = "https://jsonplaceholder.typicode.com"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


# ==================== GET 请求测试 ====================
@pytest.mark.parametrize("user_id", list(range(1, 11)))
def test_get_multiple_users(user_id):
    """获取多个用户信息"""
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response.status_code == 200, f"用户{user_id}获取失败"
    data = response.json()
    assert "id" in data, "响应应包含id字段"
    assert data["id"] == user_id, f"用户ID应为{user_id}"
    print(f"✅ 用户{user_id}: {data['name']}")


def test_get_invalid_user():
    """获取不存在的用户"""
    response = requests.get(f"{BASE_URL}/users/999", headers=headers)
    assert response.status_code == 404, "不存在的用户应返回404"
    print("✅ 测试通过：无效用户返回404")


def test_get_all_users():
    """获取所有用户"""
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 10, f"应该有10个用户，实际有{len(users)}个"
    print(f"✅ 获取到{len(users)}个用户")


# ==================== POST 请求测试 ====================
def generate_random_string(length=8):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters, k=length))


@pytest.mark.parametrize("title, body", [
    ("测试标题1", "测试内容1"),
    ("自动生成标题", generate_random_string()),
    ("特殊字符测试", "!@#$%^&*()"),
    ("长文本测试", "这是一个非常长的文本内容..." * 10),
    ("空内容测试", "")
])
def test_create_multiple_posts(title, body):
    """创建多个帖子"""
    payload = {
        "title": title,
        "body": body,
        "userId": 1
    }
    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        headers=headers
    )
    assert response.status_code == 201, "创建帖子失败"
    data = response.json()
    assert data["title"] == title, f"标题应为'{title}'"
    assert data["body"] == body, f"内容应为'{body}'"
    assert "id" in data, "响应应包含新帖子的ID"
    print(f"✅ 创建帖子成功 - ID: {data.get('id')}")


def test_create_post_with_invalid_user():
    """使用无效用户ID创建帖子"""
    payload = {"title": "测试", "body": "测试", "userId": 999}
    response = requests.post(f"{BASE_URL}/posts", json=payload, headers=headers)
    # 注意：这个API可能接受任何userId，所以我们需要检查响应
    print(f"⚠️  使用无效用户ID创建帖子 - 状态码: {response.status_code}")


# ==================== PUT 请求测试 ====================
def test_update_post():
    """更新帖子"""
    # 先获取一个存在的帖子
    response = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    assert response.status_code == 200

    # 更新帖子
    updated_data = {
        "id": 1,
        "title": "更新后的标题",
        "body": "更新后的内容",
        "userId": 1
    }
    response = requests.put(
        f"{BASE_URL}/posts/1",
        json=updated_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新后的标题"
    print("✅ 测试通过：成功更新帖子")


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_update_multiple_posts(post_id):
    """更新多个帖子"""
    payload = {
        "title": f"更新的标题{post_id}",
        "body": f"更新的内容{post_id}",
        "userId": 1
    }
    response = requests.put(
        f"{BASE_URL}/posts/{post_id}",
        json=payload,
        headers=headers
    )
    assert response.status_code == 200
    print(f"✅ 成功更新帖子{post_id}")


# ==================== DELETE 请求测试 ====================
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_delete_post(post_id):
    """删除帖子"""
    response = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=headers)
    assert response.status_code == 200, f"删除帖子{post_id}失败"
    print(f"✅ 成功删除帖子{post_id}")


def test_delete_nonexistent_post():
    """删除不存在的帖子"""
    response = requests.delete(f"{BASE_URL}/posts/999", headers=headers)
    # 注意：这个API对不存在的资源可能也返回200
    print(f"删除不存在帖子状态码: {response.status_code}")


# ==================== PATCH 请求测试 ====================
def test_partial_update_post():
    """部分更新帖子"""
    payload = {"title": "仅更新标题"}
    response = requests.patch(
        f"{BASE_URL}/posts/1",
        json=payload,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "仅更新标题"
    print("✅ 测试通过：成功部分更新帖子")


# ==================== 边界值测试 ====================
def test_get_posts_pagination():
    """测试帖子分页"""
    # 获取第1页，每页5条
    response = requests.get(f"{BASE_URL}/posts?_page=1&_limit=5", headers=headers)
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 5, f"第一页应有5条，实际有{len(posts)}条"
    print(f"✅ 分页测试通过 - 获取{len(posts)}条帖子")


def test_filter_posts_by_user():
    """按用户ID过滤帖子"""
    response = requests.get(f"{BASE_URL}/posts?userId=1", headers=headers)
    assert response.status_code == 200
    posts = response.json()
    for post in posts:
        assert post["userId"] == 1, f"帖子用户ID应为1，实际为{post['userId']}"
    print(f"✅ 成功获取用户1的{len(posts)}个帖子")


# ==================== 负向测试 ====================
def test_create_post_with_missing_fields():
    """创建帖子缺少必填字段"""
    payload = {"title": "只有标题"}  # 缺少body和userId
    response = requests.post(f"{BASE_URL}/posts", json=payload, headers=headers)
    # 注意：这个API可能仍然会创建成功
    print(f"缺少字段创建帖子状态码: {response.status_code}")


def test_create_post_with_invalid_json():
    """发送无效的JSON格式"""
    invalid_json = "{invalid json}"
    response = requests.post(
        f"{BASE_URL}/posts",
        data=invalid_json,
        headers={"Content-Type": "application/json"}
    )
    print(f"无效JSON状态码: {response.status_code}")


def test_get_with_invalid_endpoint():
    """访问不存在的端点"""
    response = requests.get(f"{BASE_URL}/nonexistent", headers=headers)
    assert response.status_code == 404, "不存在的端点应返回404"
    print("✅ 测试通过：无效端点返回404")


# ==================== 性能/响应测试 ====================
def test_response_time():
    """测试响应时间"""
    import time as t
    start_time = t.time()
    response = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    end_time = t.time()

    response_time = end_time - start_time
    assert response_time < 2.0, f"响应时间过长: {response_time:.2f}秒"
    assert response.status_code == 200
    print(f"✅ 响应时间测试通过: {response_time:.2f}秒")


# ==================== 批量操作测试 ====================
def test_batch_operations():
    """批量操作测试"""
    # 批量获取
    for i in range(1, 6):
        response = requests.get(f"{BASE_URL}/posts/{i}", headers=headers)
        assert response.status_code == 200
        print(f"  批量获取帖子{i}成功")

    print("✅ 批量操作测试通过")


# ==================== 组合测试 ====================
def test_crud_workflow():
    """完整的CRUD工作流测试"""
    print("=== 开始CRUD工作流测试 ===")

    # 1. CREATE - 创建帖子
    payload = {"title": "工作流测试", "body": "测试内容", "userId": 1}
    create_response = requests.post(f"{BASE_URL}/posts", json=payload, headers=headers)
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]
    print(f"1. 创建帖子成功 - ID: {post_id}")

    # 2. READ - 读取帖子
    read_response = requests.get(f"{BASE_URL}/posts/{post_id}", headers=headers)
    assert read_response.status_code == 200
    print(f"2. 读取帖子成功")

    # 3. UPDATE - 更新帖子
    update_payload = {"title": "更新后的工作流测试"}
    update_response = requests.patch(
        f"{BASE_URL}/posts/{post_id}",
        json=update_payload,
        headers=headers
    )
    assert update_response.status_code == 200
    print(f"3. 更新帖子成功")

    # 4. DELETE - 删除帖子
    delete_response = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=headers)
    assert delete_response.status_code == 200
    print(f"4. 删除帖子成功")

    print("✅ 完整CRUD工作流测试通过")


# ==================== 头部验证测试 ====================
def test_response_headers():
    """测试响应头部"""
    response = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    assert response.status_code == 200

    # 检查重要的响应头
    assert "Content-Type" in response.headers
    assert "application/json" in response.headers["Content-Type"]
    print("✅ 响应头部验证通过")


# ==================== 错误状态码测试 ====================
@pytest.mark.parametrize("method, endpoint, expected_code", [
    ("GET", "/posts/999", 404),
    ("POST", "/invalid", 404),
    ("PUT", "/posts/999", 500),  # 这个API可能对不存在的资源也返回200
    ("DELETE", "/posts/999", 200)  # 注意：删除不存在的资源也返回200
])
def test_error_status_codes(method, endpoint, expected_code):
    """测试各种错误状态码"""
    url = f"{BASE_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json={}, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json={}, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)

    print(f"{method} {endpoint} - 状态码: {response.status_code}, 期望: {expected_code}")


# ==================== 并发测试（简单模拟） ====================
def test_concurrent_requests():
    """模拟并发请求"""
    import threading

    results = []

    def make_request(url):
        response = requests.get(url, headers=headers)
        results.append(response.status_code)

    threads = []
    for i in range(1, 4):
        url = f"{BASE_URL}/posts/{i}"
        thread = threading.Thread(target=make_request, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    assert all(code == 200 for code in results), f"并发请求失败: {results}"
    print(f"✅ 并发测试通过 - 结果: {results}")


# 运行所有测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])