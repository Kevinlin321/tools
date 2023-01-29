import streamlit as st
import plotly.express as px
import statsmodels.api as sm

# import streamlit_nested_layout
# from decimal import Decimal

st.set_page_config(layout='wide')
st.header("回归工具箱")


# 处理输入的数据
def modify_input_data(data_list):
    x = []
    y = []
    for pair in data_list:
        if len(pair) > 0 and ("," or "，" in pair):
            pair = pair.replace("，", ",")
            x_ = float(pair.strip().split(",")[0])
            y_ = float(pair.strip().split(",")[1])
            x.append(x_)
            y.append(y_)
    return x, y


tab1, tab2 = st.tabs(["线性回归", "解方程"])

with tab1:
    with st.form("仿真仪菜单栏", ):
        st.write("请输入X和Y，用逗号分割，例如 2.4,3.5")
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            pair1 = st.text_input("第一对数据", "1.0,2.0")
            pair2 = st.text_input("第二对数据", "3.0,6.0")
            pair3 = st.text_input("第三对数据", "5.0,9.0")

        with col2:
            pair4 = st.text_input("第四对数据")
            pair5 = st.text_input("第五对数据")
            pair6 = st.text_input("第六对数据")

        with col3:
            title = st.text_input("请输入表格标题", "标题")
            x_label = st.text_input("请输入横坐标标题", "横坐标")
            y_label = st.text_input("请输入纵坐标标题", "纵坐标")
            # # Every form must have a submit button.
        submitted = st.form_submit_button("开始计算")

    if submitted:
        x, y = modify_input_data([pair1, pair2, pair3, pair4, pair5])
        text = ["(%g,%g)" % (x_, y_) for (x_, y_) in zip(x, y)]
        # st.info(text)
        fig = px.scatter(x=x, y=y, text=text, trendline="ols", )
        fig.update_layout({"title": {"text": title, "x": 0},
                           "xaxis": {"title": {"text": x_label}},
                           "yaxis": {"title": {"text": y_label}},
                           "legend": {"title": {"text": ""}, "orientation": "h", "yanchor": "top", "y": 1.1}})
        fig.update_traces(textposition="bottom left")

        model = px.get_trendline_results(fig)
        alpha = round(model.iloc[0]["px_fit_results"].params[0], 6)
        beta = round(model.iloc[0]["px_fit_results"].params[1], 6)
        r2 = round(px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared, 6)
        st.info("回归公式为 y = %f * x + %f; R2 = %f" % (beta, alpha, r2))
        st.plotly_chart(fig, use_column_width=True)

with tab2:
    st.info("回归方程 Y = 系数项 * X + 截距项")
    col1, col2, _ = st.columns([1, 1, 8])
    alpha = float(col1.text_input("输入系数项", "0.0").strip())
    beta = float(col2.text_input("输入截距项", "0.0").strip())

    st.write("差值计算")
    st.write("1. 已知X求Y")
    x_input = st.text_input("输入X").strip()
    if len(x_input) > 0:
        x_input = float(x_input)
        y_out = x_input * alpha + beta
        st.info("Y为：%f" % y_out)

    st.write("2. 已知Y求X")
    y_input = st.text_input("输入Y").strip()
    if len(y_input) > 0:
        y_input = float(y_input)
        x_out = (y_input - beta) / alpha
        st.info("X为：%f" % x_out)
