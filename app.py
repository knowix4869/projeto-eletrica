import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Projeto Elétrica", page_icon="⚡", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "componentes.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    COMPONENTES = json.load(f)

st.markdown("""
<style>
.stApp { background: #0b1220; color: #e5e7eb; }
[data-testid="stSidebar"] { background: #111b2e; }
.block-container { padding-top: 2rem; max-width: 1250px; }
.hero { padding: 1.5rem 1.7rem; border: 1px solid #26364f; border-radius: 18px;
        background: linear-gradient(120deg,#14243b,#101827); margin-bottom: 1rem; }
.hero h1 { margin: 0; color: #f8fafc; font-size: 2.1rem; }
.hero p { color: #a9bad0; margin: .4rem 0 0 0; }
.tag { display:inline-block; padding: .25rem .6rem; border-radius: 20px;
       background:#183b43; color:#67e8d0; font-size:.78rem; margin-bottom:.5rem; }
.panel { background:#111b2e; border:1px solid #26364f; padding:1rem 1.1rem;
         border-radius:14px; margin:.5rem 0; }
.small-muted { color:#9caec5; font-size:.9rem; }
div[data-testid="stMetric"] { background:#111b2e; border:1px solid #26364f; padding:1rem; border-radius:14px; }
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "Início"
if "selecionado" not in st.session_state:
    st.session_state.selecionado = None

with st.sidebar:
    st.markdown("## ⚡ Projeto Elétrica")
    st.caption("Aprenda elétrica do básico ao avançado")
    paginas = ["Início", "Biblioteca", "Quiz", "Sobre"]
    pagina = st.radio("Navegação", paginas, index=paginas.index(st.session_state.pagina))
    st.session_state.pagina = pagina
    st.divider()
    st.caption(f"Biblioteca com {len(COMPONENTES)} conteúdos • Versão 0.2")
    st.caption("Nome provisório — pode ser alterado depois.")

if pagina == "Início":
    st.markdown("""
    <div class="hero">
      <span class="tag">GUIA DE ESTUDOS • VERSÃO 0.1</span>
      <h1>⚡ Aprenda como a eletricidade funciona.</h1>
      <p>Pesquise componentes, entenda suas funções e estude com explicações diretas.</p>
    </div>
    """, unsafe_allow_html=True)
    query = st.text_input("🔎 O que você quer aprender?", placeholder="Ex.: disjuntor, contator, tensão, relé térmico...")
    if query:
        encontrados = [c for c in COMPONENTES if query.lower() in json.dumps(c, ensure_ascii=False).lower()]
        st.subheader(f"Resultados ({len(encontrados)})")
        if encontrados:
            for c in encontrados:
                with st.container(border=True):
                    st.markdown(f"### {c['icone']} {c['nome']}")
                    st.caption(c["categoria"])
                    st.write(c["resumo"])
                    if st.button("Ver explicação", key=f"home_{c['id']}"):
                        st.session_state.selecionado = c["id"]
                        st.session_state.pagina = "Biblioteca"
                        st.rerun()
        else:
            st.info("Nenhum resultado. Tente outro termo ou acesse a Biblioteca.")
    st.subheader("Explore por categoria")
    categorias = sorted(set(c["categoria"] for c in COMPONENTES))
    cols = st.columns(3)
    for i, cat in enumerate(categorias):
        with cols[i % 3]:
            qtd = sum(1 for c in COMPONENTES if c["categoria"] == cat)
            st.markdown(f"<div class='panel'><h3>{cat}</h3><span class='small-muted'>{qtd} conteúdos disponíveis</span></div>", unsafe_allow_html=True)
    st.subheader("Comece por aqui")
    cols = st.columns(3)
    for col, c in zip(cols, COMPONENTES[:3]):
        with col:
            st.markdown(f"### {c['icone']} {c['nome']}")
            st.write(c["resumo"])
            if st.button("Estudar", key=f"start_{c['id']}"):
                st.session_state.selecionado = c["id"]
                st.session_state.pagina = "Biblioteca"
                st.rerun()

elif pagina == "Biblioteca":
    st.markdown("## 📚 Biblioteca elétrica")
    cats = ["Todas"] + sorted(set(c["categoria"] for c in COMPONENTES))
    filtro = st.selectbox("Filtrar por categoria", cats)
    busca = st.text_input("Pesquisar conteúdo", placeholder="Digite o nome ou uma palavra-chave")
    lista = [c for c in COMPONENTES if filtro == "Todas" or c["categoria"] == filtro]
    if busca:
        lista = [c for c in lista if busca.lower() in json.dumps(c, ensure_ascii=False).lower()]
    escolhido = next((c for c in COMPONENTES if c["id"] == st.session_state.selecionado), None) if st.session_state.selecionado else None
    if escolhido:
        if st.button("← Voltar para a lista"):
            st.session_state.selecionado = None
            st.rerun()
        st.markdown(f"# {escolhido['icone']} {escolhido['nome']}")
        st.caption(f"{escolhido['categoria']} • {escolhido['nivel']}")
        st.markdown(f"<div class='panel'>{escolhido['resumo']}</div>", unsafe_allow_html=True)
        st.markdown("### 📘 Entenda o componente")
        for titulo, chave in [
            ("O que é?", "o_que_e"), ("Para que serve?", "para_que_serve"),
            ("Como funciona internamente?", "como_funciona"), ("Onde é utilizado?", "onde_utilizado"),
            ("Exemplo prático", "exemplo")
        ]:
            st.markdown(f"#### {titulo}")
            st.write(escolhido[chave])
        st.markdown("### 🔎 Identificação técnica")
        for titulo, chave in [
            ("Como identificar fisicamente", "aparencia"), ("Terminais e suas funções", "terminais"),
            ("Símbolo em diagramas", "simbolo"), ("Defeitos e diagnóstico inicial", "diagnostico")
        ]:
            if escolhido.get(chave):
                st.markdown(f"#### {titulo}")
                st.write(escolhido[chave])
        st.markdown("### 🦺 Cuidados importantes")
        st.write(escolhido["cuidados"])
        if escolhido.get("aliases"):
            st.caption("Também conhecido como: " + ", ".join(escolhido["aliases"]))
        st.info("Conteúdo educativo. Antes de intervir em instalações ou equipamentos, desenergize, bloqueie e confirme a ausência de tensão. Serviços elétricos devem seguir as normas aplicáveis e ser executados por pessoa qualificada.")
    else:
        st.caption(f"{len(lista)} conteúdo(s) encontrados em uma biblioteca de {len(COMPONENTES)} itens")
        for c in lista:
            with st.container(border=True):
                a, b = st.columns([5, 1])
                with a:
                    st.markdown(f"### {c['icone']} {c['nome']}")
                    st.caption(f"{c['categoria']} • {c['nivel']}")
                    st.write(c["resumo"])
                with b:
                    if st.button("Abrir", key=f"lib_{c['id']}"):
                        st.session_state.selecionado = c["id"]
                        st.rerun()

elif pagina == "Quiz":
    st.markdown("## 🧠 Teste seus conhecimentos")
    perguntas = [
      {"q":"Qual é a função principal de um disjuntor termomagnético?","op":["Medir energia consumida","Interromper o circuito em condições de sobrecorrente","Aumentar a tensão","Armazenar carga elétrica"],"a":1,"exp":"Ele protege o circuito contra sobrecargas e curtos-circuitos, conforme sua curva e capacidade."},
      {"q":"O que um contator faz?","op":["Comanda a abertura e o fechamento de um circuito por acionamento eletromagnético","Converte CA em CC","Mede resistência","Protege exclusivamente contra fuga à terra"],"a":0,"exp":"A bobina cria um campo magnético que movimenta os contatos."},
      {"q":"Qual grandeza é medida em volts (V)?","op":["Corrente","Potência","Tensão elétrica","Resistência"],"a":2,"exp":"A tensão elétrica é medida em volts."},
      {"q":"Para que serve o relé térmico em um conjunto de partida de motor?","op":["Proteger o motor contra sobrecarga","Aumentar rotação","Corrigir fator de potência sozinho","Substituir o aterramento"],"a":0,"exp":"O relé térmico detecta sobrecarga prolongada e atua no circuito de comando."}
    ]
    if "respostas" not in st.session_state:
        st.session_state.respostas = {}
    for i, p in enumerate(perguntas):
        st.markdown(f"**{i+1}. {p['q']}**")
        st.session_state.respostas[i] = st.radio("Escolha uma resposta", p["op"], key=f"quiz_{i}", label_visibility="collapsed")
    if st.button("Corrigir respostas", type="primary"):
        pontos = 0
        for i, p in enumerate(perguntas):
            idx = p["op"].index(st.session_state.respostas[i])
            if idx == p["a"]:
                pontos += 1
                st.success(f"Questão {i+1}: correta. {p['exp']}")
            else:
                st.error(f"Questão {i+1}: incorreta. {p['exp']}")
        st.metric("Sua pontuação", f"{pontos}/{len(perguntas)}")

elif pagina == "Sobre":
    st.markdown("## Sobre o projeto")
    st.write("O Projeto Elétrica é uma plataforma de aprendizado que explica componentes, conceitos e aplicações da eletricidade em linguagem acessível, do iniciante ao avançado.")
    st.markdown("### O que já existe nesta primeira versão")
    st.markdown("- Pesquisa de conteúdos\n- Biblioteca com categorias\n- Fichas: o que é, para que serve e como funciona\n- Exemplos e cuidados de segurança\n- Quiz básico")
    st.markdown("### Próximas evoluções")
    st.markdown("- Diagramas e imagens próprios por componente\n- Conteúdo de instalações, comandos e automação industrial\n- Favoritos e progresso de estudo\n- Simuladores interativos\n- Banco de dados editável e painel administrativo")
    st.warning("O nome exibido é provisório. O conteúdo técnico deve ser revisado antes de uso profissional.")
