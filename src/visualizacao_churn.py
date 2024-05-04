import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import ceil

def plot_freq_customer(df_in,num_cols):

    df = df_in
    sns.set(style="white")

    # Lista de todas as colunas que deseja plotar
    todas_colunas = df.dtypes[(df.dtypes == 'object')&(df.dtypes.index != 'customerID')].index

    # Criando a figura e os subplots (eixos) com duas linhas e três colunas
    fig, axes = plt.subplots(nrows=ceil(len(todas_colunas)/num_cols), ncols=num_cols, figsize=(15, 15))

    max_categories = 0
    for colunas in todas_colunas:
        max_categories = max(df[colunas].nunique(),max_categories)

    # Iterando sobre todas as colunas e criando um gráfico para cada uma
    for i, coluna in enumerate(todas_colunas):
        row = i // num_cols  # Determina a linha atual
        col = i % num_cols   # Determina a coluna atual

        cate = (df[coluna].nunique() / max_categories) * 0.8
        df_plot = df[coluna].value_counts(normalize=True).to_frame(name='proportion')
        sns.barplot(data=df_plot, x='proportion', y=df_plot.index, orient='h', ax=axes[row, col], width=cate)
        axes[row, col].set_title(coluna)
        axes[row, col].set_ylabel('')
        axes[row, col].set_xlabel('')
        axes[row, col].get_xaxis().set_visible(False)
        axes[row, col].set_xlim(0, 1.1)
        for index, value in enumerate(df_plot['proportion']):
            label = f'{value * 100:.1f}%'.replace('.', ',')
            axes[row, col].text(value + 0.01, index, label, va='center')

    # Esconder os eixos extras se houver (se não usou todos os subplots)
    for j in range(i+1, num_cols * axes.shape[0]):
        row = j // num_cols
        col = j % num_cols
        axes[row, col].set_visible(False)

    # Adicionando um título geral acima de todos os subplots
    fig.suptitle('Análise de Frequência das Características de Clientes', fontsize=16, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Ajusta o layout para dar espaço para o suptitle
    plt.show()


def plot_seg_churn_customer(df_in,num_cols):

    df = df_in
    sns.set(style="white")
    var = 'Churn'
    todas_colunas = df.dtypes[(df.dtypes == 'object')&(df.dtypes.index != 'customerID')&(df.dtypes.index != var)].index
    max_categories = 0
    for colunas in todas_colunas:
        max_categories = max(df[colunas].nunique(), max_categories)

    fig, ax = plt.subplots(nrows=ceil(len(todas_colunas)/num_cols), ncols=num_cols, figsize=(15, 15))

    for i, coluna in enumerate(todas_colunas):
        row = i // num_cols  # Determina a linha atual
        col = i % num_cols   # Determina a coluna atual

        df_cat = pd.DataFrame(index=df[var].value_counts().index)

        for categ in df[coluna].unique():
            df_cat = df_cat.join(pd.DataFrame(df[var][df[coluna]==categ].value_counts(normalize=True))).rename(columns={'proportion':categ})

        df_melted = df_cat.reset_index().melt(id_vars=var, var_name='cat', value_name='Proportion')

        cate = (df[coluna].nunique() / max_categories) * 0.8
        sns.barplot(data=df_melted, y=var, x='Proportion', hue='cat', orient='h', ax=ax[row, col], width=cate)

        bar_height = ax[row, col].patches[0].get_height() / 2

        for bar in ax[row, col].patches:
            if bar.get_width() > 0:
                value = f'{bar.get_width() * 100:.1f}%'.replace('.', ',')
                x = bar.get_width()
                y = bar.get_y() + bar_height
                ax[row, col].text(x + 0.01, y, value, va='center')

        ax[row, col].legend(title='', loc='lower right')
        ax[row, col].set_xlim(0, 1.5)
        ax[row, col].set_title(coluna)
        ax[row, col].set_ylabel('')
        ax[row, col].set_xlabel('')
        ax[row, col].get_xaxis().set_visible(False)

    fig.suptitle(f'{var} Segmentado pelas Características de Clientes', fontsize=16, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def plot_descr_customer(df_in,num_cols):

    df = df_in

    sns.set(style="white")
    todas_colunas = df[['MonthlyCharges','TotalCharges']].dtypes.index

    fig, axes = plt.subplots(nrows=ceil(len(todas_colunas)/num_cols), ncols=num_cols, figsize=(8, 5))

    for i, coluna in enumerate(todas_colunas):
        row = i // num_cols  # Determina a linha atual
        col = i % num_cols   # Determina a coluna atual

        sns.boxplot(y=df[coluna], ax=axes[i])
        axes[i].set_ylabel('')
        axes[i].set_title(coluna)

    axes[0].set_ylim(-10, 900)
    axes[1].set_ylim(-100, 9000)

    fig.suptitle('Análise Descritiva das Características de Clientes', fontsize=16, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    print("Valores:\n", df[['MonthlyCharges','TotalCharges']].describe())