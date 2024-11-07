import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_hanzi_components(character):
    # URL 编码字符
    encoded_character = quote(character)
    url = f"https://hanzicraft.com/character/{encoded_character}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 找到所有包含汉字组成部分的 div
            decompboxes = soup.find_all('div', class_='decompbox')

            # 硬编码要查找的 data-reactid
            react_ids = ['54', '70', '101']
            all_components = {}  # 用于存储各个ID对应的组件

            for react_id in react_ids:
                target_decompbox = None
                for decompbox in decompboxes:
                    if decompbox.get('data-reactid') == react_id:
                        target_decompbox = decompbox
                        break

                if target_decompbox:
                    components = []  # 使用列表来存储组件
                    # 使用集合来避免重复
                    seen_components = set()

                    if react_id in ['54', '70']:
                        # 处理 <a> 元素
                        a_elements = target_decompbox.find_all('a')
                        for a in a_elements:
                            component = a.text.strip()
                            if component and component not in seen_components:  # 确保组件不为空并且未记录
                                components.append(component)
                                seen_components.add(component)
                    elif react_id == '101':
                        # 处理 <span> 元素，提取所有 <span> 的值
                        span_elements = target_decompbox.find_all('span')
                        for span in span_elements:
                            # 提取文本并处理
                            for text in span.stripped_strings:  # 使用 stripped_strings 获取所有有效文本
                                if text not in seen_components:  # 确保未记录
                                    components.append(text)
                                    seen_components.add(text)  # 记录组件

                    # 将结果存储到字典中
                    all_components[react_id] = components
                else:
                    all_components[react_id] = []  # 如果未找到，添加空列表

            # 打印各个 ID 对应的组成部分，修改了输出格式
            for react_id, components in all_components.items():
                if react_id == '54':
                    print(f"data-reactid '{react_id}' 的组成部分：{components}")
                elif react_id == '70':
                    print(f"data-reactid '{react_id}' 的拆解部分：{components}")
                elif react_id == '101':
                    print(f"data-reactid '{react_id}' 的笔画：{components}")
                else:
                    print(f"未找到 data-reactid '{react_id}' 的组成部分。")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")

if __name__ == "__main__":
    character = "浩"  # 您可以替换为其他汉字
    get_hanzi_components(character)
