app:
  description: OCR文档识别与分析工具
  icon: 📝
  icon_background: '#F0F7FF'
  mode: workflow
  name: OCR-验证码识别
  use_icon_as_answer_icon: false
dependencies:
- current_identifier: null
  type: marketplace
  value:
    marketplace_plugin_unique_identifier: langgenius/siliconflow:0.0.8@217f973bd7ced1b099c2f0c669f1356bdf4cc38b8372fd58d7874f9940b95de3
kind: app
version: 0.1.5
workflow:
  conversation_variables: []
  environment_variables: []
  features:
    file_upload:
      allowed_file_extensions: []
      allowed_file_types:
      - image
      allowed_file_upload_methods:
      - local_file
      - remote_url
      enabled: true
      fileUploadConfig:
        audio_file_size_limit: 50
        batch_count_limit: 5
        file_size_limit: 15
        image_file_size_limit: 10
        video_file_size_limit: 100
        workflow_file_upload_limit: 10
      image:
        enabled: false
        number_limits: 3
        transfer_methods:
        - local_file
        - remote_url
      number_limits: 3
    opening_statement: 欢迎使用验证码识别助手。请上传一张验证码图片，我将识别其中的内容。
    retriever_resource:
      enabled: false
    sensitive_word_avoidance:
      enabled: false
    speech_to_text:
      enabled: false
    suggested_questions:
    - 提取文档中的关键信息
    - 分析识别结果
    - 总结文档主要内容
    suggested_questions_after_answer:
      enabled: true
    text_to_speech:
      enabled: false
      language: ''
      voice: ''
  graph:
    edges:
    - data:
        isInIteration: false
        sourceType: start
        targetType: llm
      id: start-to-processor
      source: start-node
      sourceHandle: source
      target: processor-node
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        sourceType: llm
        targetType: end
      id: processor-to-end
      source: processor-node
      sourceHandle: source
      target: end-node
      targetHandle: target
      type: custom
    nodes:
    - data:
        desc: 上传验证码图片
        selected: false
        title: 开始
        type: start
        variables:
        - allowed_file_extensions:
          - .png
          - .jpg
          - .jpeg
          - .gif
          allowed_file_types:
          - image
          allowed_file_upload_methods:
          - local_file
          - remote_url
          label: 验证码图片
          max_length: 48
          options: []
          required: true
          type: file
          variable: captchaImage
      height: 118
      id: start-node
      position:
        x: 434.25199267217323
        y: 242.421417167448
      positionAbsolute:
        x: 434.25199267217323
        y: 242.421417167448
      selected: false
      type: custom
      width: 244
    - data:
        context:
          enabled: true
          variable_selector:
          - start-node
          - captchaImage
        desc: 识别验证码
        model:
          completion_params:
            max_tokens: 50
            temperature: 0
          mode: chat
          name: Qwen/Qwen2-VL-72B-Instruct
          provider: langgenius/siliconflow/siliconflow
        prompt_template:
        - id: system-prompt
          role: system
          text: '你是一个高精度的验证码识别工具。你需要准确识别图片中显示的所有字符，无论是数字、字母还是特殊符号。


            请记住:

            1. 只输出验证码文本，不要有任何解释或额外内容

            2. 仔细观察每个字符，区分相似的字符如"0"和"O"、"1"和"I"等

            3. 考虑所有可能的字符，包括大小写字母、数字和特殊符号

            4. 忽略任何水印、背景噪声或干扰线

            5. 如果验证码有特定格式(如分组)，请保留该/格式


            上下文文本内容：

            {{#start-node.captchaImage#}}


            不要猜测。如果某个字符完全无法识别，请用"?"代替。

            '
        - id: user-input
          role: user
          text: '请识别这张验证码图片中的内容。直接提供验证码文本，不要添加任何说明或解释。

            '
        retry_config:
          max_retries: 3
          retry_enabled: true
          retry_interval: 1000
        selected: true
        title: 验证码识别
        type: llm
        vision:
          configs:
            detail: high
            variable_selector:
            - start-node
            - captchaImage
          enabled: true
      height: 143
      id: processor-node
      position:
        x: 769.6483752801057
        y: 242.421417167448
      positionAbsolute:
        x: 769.6483752801057
        y: 242.421417167448
      selected: true
      type: custom
      width: 244
    - data:
        desc: 输出识别结果
        outputs:
        - value_selector:
          - processor-node
          - text
          variable: captchaResult
        selected: false
        title: 结束
        type: end
      height: 118
      id: end-node
      position:
        x: 1084.9174211142688
        y: 242.421417167448
      positionAbsolute:
        x: 1084.9174211142688
        y: 242.421417167448
      selected: false
      type: custom
      width: 244
    viewport:
      x: -154.19557006797743
      y: 76.14147066596661
      zoom: 0.6597539553864489

