import streamlit as st
from pathlib import Path
from rag_system import RagSystem

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

.main-header {
    font-size: 3rem;
    background: linear-gradient(135deg, #8B4513, #CD853F);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 700;
    font-family: 'Noto Serif SC', serif;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.subtitle {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-bottom: 2rem;
    font-family: 'Noto Serif SC', serif;
}

.chat-message {
    padding: 1.2rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease-in;
}

.chat-message:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.user-message {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    border-left: 4px solid #2196f3;
    margin-left: 2rem;
}

.assistant-message {
    background: linear-gradient(135deg, #fff8e1, #ffecb3);
    border-left: 4px solid #8B4513;
    margin-right: 2rem;
}

.source-info {
    background: linear-gradient(135deg, #f3e5f5, #e1bee7);
    padding: 0.8rem;
    border-radius: 0.8rem;
    margin-top: 0.8rem;
    font-size: 0.9rem;
    border: 1px solid #ce93d8;
    transition: all 0.3s ease;
}

.source-info:hover {
    background: linear-gradient(135deg, #e8eaf6, #c5cae9);
    border-color: #9c27b0;
}

.status-success {
    color: #2e7d32;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.status-error {
    color: #d32f2f;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.status-warning {
    color: #f57c00;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.example-button {
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    border: 1px solid #ffb74d;
    border-radius: 0.5rem;
    padding: 0.5rem;
    margin: 0.2rem 0;
    transition: all 0.3s ease;
    cursor: pointer;
}

.example-button:hover {
    background: linear-gradient(135deg, #ffe0b2, #ffcc80);
    transform: translateX(5px);
}

.sidebar-section {
    background: linear-gradient(135deg, #fafafa, #f5f5f5);
    padding: 1rem;
    border-radius: 0.8rem;
    margin-bottom: 1rem;
    border: 1px solid #e0e0e0;
}

.typing-indicator {
    display: inline-block;
    animation: typing 1.5s infinite;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes typing {
    0%, 60%, 100% { opacity: 1; }
    30% { opacity: 0.5; }
}

.metric-card {
    background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
    padding: 1rem;
    border-radius: 0.8rem;
    text-align: center;
    margin: 0.5rem 0;
    border: 1px solid #81c784;
}

.progress-bar {
    background: linear-gradient(90deg, #4caf50, #8bc34a);
    height: 4px;
    border-radius: 2px;
    animation: progress 2s ease-in-out;
}

@keyframes progress {
    from { width: 0%; }
    to { width: 100%; }
}
</style>
""", unsafe_allow_html=True)

def getEnvInfo(key):
    env_file = Path(".env")

    env_lines=[]
    env_res=None
    if env_file.exists():
        with open(env_file, "r",encoding='utf-8') as f:
            env_lines = f.readlines()

        #查找对应的配置项
        for i,line in enumerate(env_lines):
            if line.strip().startswith(f"{key}="):
               env_res = line.strip().split("=")[1]

    if env_res is None:
        raise ValueError(f"找不到环境变量 {key}，检查.env文件")
    return env_res

def init_session_state():
    #系统状态
    if 'system_init' not in st.session_state:
        st.session_state.system_init = False
    #deepseek_key
    if 'api_key' not in st.session_state:
        st.session_state.api_key = getEnvInfo('DEEPSEEK_API_KEY')

    #自动初始化
    rag = RagSystem()
    rag.initialize()
    st.session_state.rag_system = rag
    st.session_state.system_init = True

def check_cache_exists():
    cache_dir = Path("cache")
    vectors_cache = cache_dir / "doc_vectors.pkl"
    chunks_cache = cache_dir / "doc_chunks.pkl"
    return vectors_cache.exists() and chunks_cache.exists()

def main():
    init_session_state()
    st.markdown('<h1 class="main-header">📚图书智能检索系统</h1>',unsafe_allow_html=True)
    # print(getEnvInfo('DEEPSEEK_API_KEY'),'DEEPSEEK_API_KEY')

    #侧边栏
    with st.sidebar:
        st.header("⚙️ 系统配置")
        api_key_input = st.text_input(
            "🔑 Deepseek API密钥",
            type="password",
            value=st.session_state.api_key,
            help="请输入您的DeepSeek API密钥，如果已经保存到了配置文件，刷新页面后会自动加载。",
            placeholder="sk-xxxxxxxxxxxxx"
        )

        if api_key_input:
            st.session_state.api_key = api_key_input
        else:
            st.session_state.system_init = False

        st.header("📊 系统状态")
        if not st.session_state.system_init:
            st.markdown('<p class="status-warning">⚠️ 系统未初始化 </p>',unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-success">✅ 系统已就绪 </p>',unsafe_allow_html=True)
            if st.session_state.rag_system:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📄</h3>
                        <p>{len(st.session_state.rag_system.documents)}</p>
                        <small>文档数量</small>
                    </div>
                """,unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📝</h3>
                        <p>{len(st.session_state.rag_system.doc_chunks)}</p>
                        <small>文档块</small>
                    </div>
                """,unsafe_allow_html=True)

        #获取按钮状态
        cache_exists = check_cache_exists()
        if cache_exists and st.session_state.system_init:
            st.button("🔄 重新初始化系统",use_container_width=True)
        else:
            if st.button("🚀 加载缓存数据",use_container_width=True):
                init_session_state()



if __name__ == "__main__":
    main()