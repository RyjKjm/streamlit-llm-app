from dotenv import load_dotenv
load_dotenv()

import streamlit as st


# Webアプリの概要・操作説明
st.title("専門家LLMチャットアプリ")
st.markdown("""
このアプリは、質問内容に応じて専門家の視点で回答するAIチャットです。\n
1. 下のラジオボタンで専門家の種類を選択してください。\n
2. 質問を入力し、送信ボタンを押すと、選択した専門家としてAIが回答します。\n
""")


# 専門家の種類をラジオボタンで選択
expert_type = st.radio(
	"専門家の種類を選択してください：",
	[
		"医療の専門家",
		"法律の専門家",
		"ITの専門家",
		"教育の専門家"
	]
)

# テキスト入力フォーム
user_input = st.text_input("質問を入力してください：")


# LLM呼び出し関数
def get_expert_answer(user_input: str, expert_type: str) -> str:
	from langchain.chat_models import ChatOpenAI
	from langchain.schema import SystemMessage, HumanMessage
	import os

	system_messages = {
		"医療の専門家": "あなたは医療分野の専門家です。医学的知識に基づいて、分かりやすく丁寧に回答してください。",
		"法律の専門家": "あなたは法律分野の専門家です。法的根拠や注意点を含めて、分かりやすく回答してください。",
		"ITの専門家": "あなたはIT分野の専門家です。技術的な観点から、分かりやすく回答してください。",
		"教育の専門家": "あなたは教育分野の専門家です。教育的な観点から、分かりやすく回答してください。"
	}

	openai_api_key = os.getenv("OPENAI_API_KEY")
	if not openai_api_key:
		return "OPENAI_API_KEYが設定されていません。環境変数または.envファイルを確認してください。"

	chat = ChatOpenAI(openai_api_key=openai_api_key)
	messages = [
		SystemMessage(content=system_messages.get(expert_type, "あなたは専門家です。分かりやすく回答してください。")),
		HumanMessage(content=user_input)
	]
	response = chat(messages)
	return response.content

# 送信ボタン
if st.button("送信"):
	st.write(f"入力された質問: {user_input}")
	st.write(f"選択された専門家: {expert_type}")
	answer = get_expert_answer(user_input, expert_type)
	st.markdown("### 回答")
	st.write(answer)

