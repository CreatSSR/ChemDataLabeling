import os
from flask import Flask, request, jsonify
import openai
import fitz  # PyMuPDF
import json
import tempfile

app = Flask(__name__)

client = openai(
    api_key="sk-bvbdBmqnEUq0SCYArmNNoFPyv6kTy7GWZTB027W15sltWLn6",  # 替换成你的 DMXapi 令牌key
    base_url="https://www.dmxapi.com/v1",  # 需要改成DMXAPI的中转 https://www.dmxapi.com/v1 ，这是已经改好的。
)


# 定义GPT-4接口来提取化学反应
def extract_reaction_info(text):
    prompt = f"Extract and format the chemical reactions in this text into a structured table:\n{text}"
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].text.strip()

# 处理上传的PDF文档
@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    if file:
        # 保存PDF文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)

        # 使用PyMuPDF提取PDF文本
        doc = fitz.open(temp_file.name)
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text()

        # 提取化学反应信息
        reactions = extract_reaction_info(full_text)

        # 将文献中的相关反应标注返回
        highlighted_pdf = highlight_pdf(doc, reactions)

        # 保存标注后的PDF并返回文件路径
        highlighted_pdf_path = "/tmp/highlighted_document.pdf"
        highlighted_pdf.save(highlighted_pdf_path)

        return jsonify({"message": "File processed successfully", "pdf_path": highlighted_pdf_path})

# PDF高亮标注
def highlight_pdf(doc, reactions):
    highlighted_doc = doc.copy()

    # 解析反应并将关键内容高亮
    for reaction in reactions.split("\n"):
        for page_num in range(len(doc)):
            page = highlighted_doc.load_page(page_num)
            found_text_instances = page.search_for(reaction)
            for inst in found_text_instances:
                page.add_highlight_annot(inst)

    return highlighted_doc

if __name__ == "__main__":
    app.run(debug=True)