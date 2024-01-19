from taipy.gui import notify, Markdown

from biz.auth import login_user

login_open = True
username = ''
password = ''


def login(state):
    if login_user(state.username, state.password):
        state.login_open = False
        notify(state, "success", f"恭喜 {state.username}, 登录成功！")
    else:
        notify(state, 'error', f'抱歉 {state.username}, 登录失败！ 请检查用户名、密码！')
    pass


nav_lov = [
    ("/playground", "机器人"),
    ("/vcustomers", "AI客户"),
    ("/vtrainers", "AI培训师"),
    # ("/scenes", "场景"),
    # ("/trainings", "课程")
]

root_md = Markdown("pages/root.md")
