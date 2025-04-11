from flask import Flask, request, jsonify, render_template
import test1

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

@app.route('/run-python', methods=['POST'])
def run_python():
    try:
        # 调用 test1.py 中的函数
        url_or_file_path = "C:/Users/28440/Desktop/中大奖/中大奖/newpage.html"  # 这里可以动态获取路径
        page_text = test1.fetch_and_extract_text(url_or_file_path)

        if page_text:
            page_text_clean = test1.clean_sentence(page_text)
            existing_texts = [
                "您父亲今天在街上摔倒，我将他送到医院，需要住院费，急!赶紧转。",
                "您好!你的手机余额不足，为了不影响您的正常使用，请转款到xx缴费。",
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

            highest_similarity = 0
            highest_similarity_type = ""
            highest_related_text = ""

            for existing_text in existing_texts:
                existing_text_clean = test1.clean_sentence(existing_text)
                
                char_similarity, _ = test1.calculate_char_similarity(page_text_clean, existing_text_clean)
                if char_similarity > highest_similarity:
                    highest_similarity = char_similarity
                    highest_similarity_type = "字符"
                    highest_related_text = existing_text
                
                word_similarity, _ = test1.calculate_word_similarity(page_text_clean, existing_text_clean)
                if word_similarity > highest_similarity:
                    highest_similarity = word_similarity
                    highest_similarity_type = "词语"
                    highest_related_text = existing_text

            if highest_similarity > 0.1:
                return jsonify({
                    "message": f"警告！该网页存在高风险!",
                    "status": "warning"
                }), 200
            else:
                return jsonify({
                    "message": "网页内容正常。",
                    "status": "success"
                }), 200
        else:
            return jsonify({
                "message": "无法提取内容。",
                "status": "error"
            }), 500
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)  