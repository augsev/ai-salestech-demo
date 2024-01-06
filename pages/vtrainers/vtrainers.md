<|{vo_create_show}|dialog|title=新建AI培训师|width=30%|labels=取消;新建|on_action=action_create

<|{vo_tname}|input|label=名称|class_name=fullwidth|>

<|{vo_notes}|input|label=描述|class_name=fullwidth|>
|>

<|{vo_confirm_show}|dialog|title=确认重新练习|width=30%|labels=取消;确认|on_action=action_renew_chat
#### **您确认清除现有聊天记录，重新开始练习吗？**{: .h6}
|>

<|2 9|layout|
<sidebar|sidebar|
<|{vo_bvt}|selector|lov={vo_bvts}|type=BoVTrainer|adapter={lambda v: (str(v.id), v.tname)}|on_change=action_select|>
<|新建 +|button|on_action=action_open_create_dialog|class_name=fullwidth plain|>
|sidebar>

<|part|render=True|class_name=align-item-bottom table|
<|{vo_conversation}|table|style=style_conv|show_all|width=100%|selected={vo_selected_row}|rebuild|>
<|part|class_name=card mt1|
<|9 1|layout|
<|{vo_current_message}|input|active={vo_current_message_active}|label=输入内容|multiline=True|lines_shown=2|on_action=action_send_message|on_change=message_changed|class_name=fullwidth message_input|>

<|{vo_icon_history}|button|hover_text=复制聊天记录|on_action=action_copy_conversation|>
|>
|>
|>
|>

<|{vo_detail_show}|pane|anchor=right|width=800px|
<|container container-bg|

#### **属性编辑**{: .color-primary .h5}

<|1 1|layout|gap=1rem|class_name=m-half|
<|{vo_bvt.tname}|input|label=名称|class_name=fullwidth|>

<|{vo_bvt.notes}|input|label=描述||class_name=fullwidth|>
|>

#### **配置编辑**{: .color-primary .h5}

<|1|layout|class_name=m-half|
<|{vo_bvt.config.assistant_id}|input|label=AssistantID|active=False|class_name=fullwidth|>
|>

<|1|layout|class_name=m-half|
<|{vo_instructions}|input|label=说明|multiline=True|lines_shown=10|class_name=fullwidth|>
|>

<|保存|button|on_action=action_update|class_name=plain|>
<|重新练习|button|on_action=action_open_confirm_dialog|>
|>
|>
