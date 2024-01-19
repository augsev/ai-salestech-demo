<|{vo_create_show}|dialog|title=新建机器人|width=30%|labels=取消;新建|on_action=action_create

<|{vo_name}|input|label=名称|class_name=fullwidth|>

<|{vo_notes}|input|label=备注|class_name=fullwidth|>
|>

<|{vo_confirm_show}|dialog|title=确认重新练习|width=30%|labels=取消;确认|on_action=action_renew_chat
#### **您确认清除现有聊天记录，重新开始练习吗？**{: .h6}
|>

<|2 9|layout|
<sidebar|sidebar|
<|{vo_bot}|selector|lov={vo_bots}|type=Bot|adapter={lambda v: (str(v.id), v.name)}|on_change=action_select|>

<|1 1|layout|gap=1rem|class_name=m-half|
<|新建 +|button|on_action=action_open_create_dialog|class_name=fullwidth plain|>

<|刷新|button|on_action=action_reload_selection|class_name=fullwidth|>
|>
|sidebar>

<|part|render=True|class_name=align-item-bottom table|
<|{vo_conversation}|table|style=style_conv|show_all|width=100%|selected={vo_selected_row}|rebuild|>
<|part|class_name=card mt1|
<|9 1 1|layout|
<|{vo_current_message}|input|active={vo_current_message_active}|label=输入内容|multiline=True|lines_shown=2|class_name=fullwidth message_input|>

<|发送|button|on_action=action_send_message|active={vo_current_message_active}|class_name=plain|>

<|{None}|file_download|label=下载对话|on_action=action_download_history|active={vo_current_message_active}|>
<|重新练习|button|on_action=action_open_confirm_dialog|active={vo_current_message_active}|>
|>
|>
|>
|>

<|{vo_detail_show}|pane|anchor=right|width=800px|
<|container container-bg|

#### **属性编辑**{: .color-primary .h5}

<|1 1|layout|gap=1rem|class_name=m-half|
<|{vo_bot.name}|input|label=名称|class_name=fullwidth|>

<|{vo_bot.notes}|input|label=备注||class_name=fullwidth|>
|>

#### **配置编辑**{: .color-primary .h5}
<|1|layout|class_name=m-half|
<|{vo_bot.prompts}|input|label=提示词|multiline=True|lines_shown=10|class_name=fullwidth|>
|>

<|保存|button|on_action=action_update|class_name=plain|>
|>
|>
