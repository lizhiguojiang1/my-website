import os
import re
import requests
from bs4 import BeautifulSoup
import jieba
import tkinter as tk
from tkinter import messagebox

def is_url(path):
    """
    判断输入是否是 URL
    """
    return re.match(r'^(http|https)://', path) is not None

def fetch_and_extract_text(path):
    """
    从网页或本地 HTML 文件提取文字内容
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }
    try:
        if is_url(path):  # 如果是 URL
            response = requests.get(path, headers=headers)
            response.raise_for_status()
            html_content = response.text
        elif os.path.exists(path):  # 如果是本地文件
            with open(path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        else:
            print("输入既不是有效的 URL，也不是有效的本地文件路径。")
            return None
        
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception as e:
        print(f"Error processing the input: {e}")
        return None

def clean_sentence(sentence):
    """
    清理句子：移除标点和特殊字符
    """
    return re.sub(r'[^\w\s]', '', sentence)

def calculate_char_similarity(sentence1, sentence2):
    """
    计算两句话之间相同字的相似度。
    相似度 = (共同字数) / (两句总字数的平均值)
    """
    set1 = set(sentence1)
    set2 = set(sentence2)
    common_chars = set1.intersection(set2)
    common_count = len(common_chars)
    avg_length = (len(set1) + len(set2)) / 2
    similarity = common_count / avg_length if avg_length > 0 else 0
    return similarity, common_chars

def calculate_word_similarity(sentence1, sentence2):
    """
    计算两句话之间相同词的相似度。
    相似度 = (共同词数) / (两句总词数的平均值)
    """
    words1 = set(jieba.cut(sentence1))
    words2 = set(jieba.cut(sentence2))
    common_words = words1.intersection(words2)
    common_count = len(common_words)
    avg_length = (len(words1) + len(words2)) / 2
    similarity = common_count / avg_length if avg_length > 0 else 0
    return similarity, common_words

def show_popup(similarity, similarity_type, related_text):
    """
    显示弹窗，提示最高相似度的结果
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    if similarity > 0.1:
        message = (f"警告！该网页存在高风险。\n")
        messagebox.showwarning("高风险警告", message)

    root.quit()  # 退出 tkinter 主循环

# 直接指定 URL 或本地 HTML 文件路径
url_or_file_path = "C:/Users/28440/Desktop/中大奖/中大奖/newpage.html"  # 修改为本地文件路径或 URL

# 提取网页文字
page_text = fetch_and_extract_text(url_or_file_path)

if page_text:
    # 清理提取的网页内容
    page_text_clean = clean_sentence(page_text)
    print("网页提取的文字内容（清理后）:\n")
    print(page_text_clean[:10000])  # 只打印前10000个字符

    # 已有的文字列表
    existing_texts = [
          "您父亲今天在街上摔倒，我将他送到医院，需要住院费，急!赶紧转。",
        "您好!你的手机余额不足，为了不影响您的正常使用，请转款到xx缴费。",
        "您在外地开办的有线电视欠费，请于今天内缴纳!",
        "您在本网站购买的刘冰冰同款长裙缺货，请留下卡号等信息，为您退款。",
        "您好!由于相关税收政策调整，您购买的宝马x5最新款可办理退税......",
        "不好意思，由于系统故障，需要您重新输入个人信息。",
        "海外代购二手电脑，九成新，三折低价，手慢无。",
        "xx行全球通，多币种信用卡，快捷安全!",
        "您好!您的个人信息已泄露，需将资金转到安全账户。",
        "中国海关查到你的包裹藏有毒品，请转账到xx并配合调查。",
        "喂，我是宇宙风快递的啊，您的包裹查不到具体地址，麻烦您再发一下。",
        "您好，我是人社局的，您的社保卡有问题，麻烦提供点信息。",
        "请问是xx同学家长吗?您申请的补助已经到账，需要您提供下银行卡号。",
        "您好，请汇款到xx行，账号xxxx。",
        "推荐股票，稳赚不赔！",
        "给你推荐的股票不涨？诈骗分子会告诉你继续交会费，要升级到高级会员才能给你推荐收益高的。",
        "现在股票不好炒，但我有内幕消息，只需给我10%回扣，跟着我买就能赚到钱。",
        "我有一款高收益理财产品，只需充值成为会员即可。",
        "由于系统正在维护，暂时无法提现。",
        "你只需转账到此账户，即可充值到在你投资平台的个人账户里。",
        "有一个外汇交易平台，平台里面有一个专业操作手，只要给回扣，操作手就会在规定的时间内投资那种项目。",
        "我知道有个赌博平台有漏洞，跟着我买，保证赚钱。",
        "区块链应用场景落地，XX币躺着也能赚大钱。"
    ]

    # 初始化最高相似度相关变量
    highest_similarity = 0
    highest_similarity_type = ""
    highest_related_text = ""

    # 计算字符相似度和词语相似度
    for existing_text in existing_texts:
        existing_text_clean = clean_sentence(existing_text)
        
        # 基于字符的相似度
        char_similarity, _ = calculate_char_similarity(page_text_clean, existing_text_clean)
        if char_similarity > highest_similarity:
            highest_similarity = char_similarity
            highest_similarity_type = "字符"
            highest_related_text = existing_text
        
        # 基于词语的相似度
        word_similarity, _ = calculate_word_similarity(page_text_clean, existing_text_clean)
        if word_similarity > highest_similarity:
            highest_similarity = word_similarity
            highest_similarity_type = "词语"
            highest_related_text = existing_text

    # 显示最高相似度的弹窗
    if highest_similarity > 0.1:
        show_popup(highest_similarity, highest_similarity_type, highest_related_text)
else:
    print("无法提取内容。")