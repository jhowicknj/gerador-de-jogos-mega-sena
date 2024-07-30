import streamlit as st
import pandas as pd
from collections import Counter
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar o estilo dos gráficos
sns.set(style="whitegrid")

# Título do aplicativo
st.title("Análise da Mega-Sena")

# Instruções para o usuário
st.markdown("""
Este aplicativo analisa os resultados históricos da Mega-Sena fornecidos em uma planilha Excel e sugere jogos com base na frequência dos números.

1. **Faça o upload da sua planilha Excel** contendo os resultados da Mega-Sena.
2. **Veja os números mais frequentes** e os jogos sugeridos com base nesses números.
3. **Observe gráficos e tabelas** para uma melhor compreensão dos dados.
""")

# Upload da planilha
uploaded_file = st.file_uploader("Escolha a planilha Excel com os resultados da Mega-Sena", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Ler a planilha
        df = pd.read_excel(uploaded_file)
        
        # Mostrar os primeiros registros
        st.subheader("Primeiros registros da planilha:")
        st.write(df.head())

        # Flatten os números da planilha, considerando todas as linhas e colunas
        numeros = df.values.flatten()
        
        # Filtrar apenas números válidos (remover valores NaN e não inteiros)
        numeros = [num for num in numeros if pd.notnull(num) and isinstance(num, (int, float))]
        
        # Contar a frequência dos números
        contador = Counter(numeros)
        numeros_frequentes = contador.most_common(60)  # Os 60 números mais frequentes

        # Pegue os números mais frequentes
        numeros_mais_frequentes = [numero for numero, frequencia in numeros_frequentes]

        # Mostrar os números mais frequentes
        st.subheader("Números mais frequentes:")
        numeros_df = pd.DataFrame(numeros_frequentes, columns=['Número', 'Frequência'])
        st.write(numeros_df)

        # Mostrar gráfico de frequências
        st.subheader("Distribuição de Frequências dos Números")
        fig, ax = plt.subplots()
        sns.barplot(x='Número', y='Frequência', data=numeros_df, ax=ax, palette='viridis')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Monte 5 jogos com 6 números cada
        jogos = []
        for _ in range(5):
            jogo = random.sample(numeros_mais_frequentes, 6)
            jogos.append(jogo)

        # Mostrar os jogos
        st.subheader("Jogos sugeridos:")
        for i, jogo in enumerate(jogos, start=1):
            st.write(f"Jogo {i}: {sorted(jogo)}")

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
