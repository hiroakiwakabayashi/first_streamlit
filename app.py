import streamlit as st
st.write("クラウド版テストページ")
st.title("streamlit入門")
st.subheader("課題1-1")
st.caption("キャプションテスト")
st.code('''
#1から10までの整数を足し算するプログラム
sum=0
for i in range(11):
  sum+=i 
print(sum)''')
st.divider()
if st.button("ｺﾝﾆﾁﾊ"):
  st.write('ボタンが押されました')
num1=st.number_input('1st number',step=1)
num2=st.number_input('2nd number',step=1)
ans=num1+num2
st.write(str(num1),"+",str(num2),"=",str(ans))
radioans=st.radio("何の計算する？",["足し算","掛け算","引き算"])
if radioans=="足し算":
  ans=num1+num2
  st.write(str(num1),"+",str(num2),"=",str(ans))
elif radioans=="掛け算":
  ans=num1*num2
  st.write(str(num1),"*",str(num2),"=",str(ans))
else:
  ans=num1-num2
  st.write(str(num1),"-",str(num2),"=",str(ans))

st.write('まとめての方')
choise1=st.checkbox('掛け算')
choise2=st.checkbox('足し算')
choise3=st.checkbox('引き算')
if choise1:
  ans=num1*num2
  st.write(str(num1),"*",str(num2),"=",str(ans))
if choise2:
  ans=num1+num2
  st.write(str(num1),"+",str(num2),"=",str(ans))
if choise3:
  ans=num1-num2
  st.write(str(num1),"-",str(num2),"=",str(ans))