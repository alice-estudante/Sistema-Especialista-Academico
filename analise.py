from experta import Fact, Field, KnowledgeEngine, NOT, Rule, P
import csv
# Constante de configuração do sistema escolar
totalAulas = 80

# 1. Base de Conhecimento (Fatos)
class Aluno(Fact):
    """Armazena os dados coletados do aluno."""
    cpf = Field(int)
    nome = Field(str)
    dataNasc = Field(str)
    mat = Field(int)
    nota1 = Field(float)
    nota2 = Field(float)
    faltas = Field(int)
    disciplinas_reprovadas = Field(int, default=0)


class MediaGeral(Fact):
    """Fato derivado: média calculada das notas."""

    valor = Field(float)


class Frequencia(Fact):
    """Fato derivado: porcentagem de presença calculada."""

    porcentagem = Field(float)


class SituacaoAcademica(Fact):
    """Resultado da situação final do aluno no semestre."""

    status = Field(str)


class PerfilMerito(Fact):
    """Indica elegibilidade para bolsa de mérito acadêmico."""

    elegivel = Field(bool)


class RiscoAcademico(Fact):
    """Nível de alerta e recomendações/plano de ação."""

    alerta = Field(str)
    recomendacao = Field(str)


# 2. Motor de Inferência (Regras)
class SistemaAcademico(KnowledgeEngine):

    # --- REGRA 1: Cálculo das Variáveis Derivadas ---
    @Rule(
        Aluno(
            nota1=P(lambda x: isinstance(x, (int, float))),
            nota2=P(lambda x: isinstance(x, (int, float))),
            faltas=P(lambda x: x >= 0),
        )
    )
    def calcular_variaveis_derivadas(self):

        # Cálculo da Média
        media = (aluno["nota1"] + aluno["nota2"]) / 2.0

        # Cálculo da Frequência baseado na constante totalAulas
        presencas = totalAulas - aluno["faltas"]
        freq_pct = (presencas / totalAulas) * 100.0

        # Declara os fatos inferidos
        self.declare(MediaGeral(valor=media))
        self.declare(Frequencia(porcentagem=freq_pct))

    # --- REGRAS: Definição da Situação Acadêmica ---
    @Rule(
        Frequencia(porcentagem=P(lambda f: f < 75.0)),
        NOT(SituacaoAcademica()),
    )
    def reprovado_por_faltas(self):
        self.declare(SituacaoAcademica(status="Reprovado por Faltas"))

    @Rule(
        Frequencia(porcentagem=P(lambda f: f >= 75.0)),
        MediaGeral(valor=P(lambda m: m < 4.0)),
        NOT(SituacaoAcademica()),
    )
    def reprovado_por_nota(self):
        self.declare(SituacaoAcademica(status="Reprovado por Nota"))

    @Rule(
        Frequencia(porcentagem=P(lambda f: f >= 75.0)),
        MediaGeral(valor=P(lambda m: 4.0 <= m < 7.0)),
        NOT(SituacaoAcademica()),
    )
    def em_recuperacao(self):
        self.declare(
            SituacaoAcademica(status="Em Recuperação / Exame Final")
        )

    @Rule(
        Frequencia(porcentagem=P(lambda f: f >= 75.0)),
        MediaGeral(valor=P(lambda m: m >= 7.0)),
        NOT(SituacaoAcademica()),
    )
    def aprovado(self):
        self.declare(SituacaoAcademica(status="Aprovado"))

    # --- REGRAS: Concessão de Bolsas e Destaque ---
    @Rule(
        MediaGeral(valor=P(lambda m: m >= 8.0)),
        Frequencia(porcentagem=P(lambda f: f >= 90.0)),
        NOT(PerfilMerito()),
    )
    def elegivel_bolsa_merito(self):
        self.declare(PerfilMerito(elegivel=True))

    @Rule(
        MediaGeral(valor=P(lambda m: m < 8.0)),
        NOT(PerfilMerito()),
    )
    def nao_elegivel_bolsa_media(self):
        self.declare(PerfilMerito(elegivel=False))

    @Rule(
        Frequencia(porcentagem=P(lambda f: f < 90.0)),
        NOT(PerfilMerito()),
    )
    def nao_elegivel_bolsa_freq(self):
        self.declare(PerfilMerito(elegivel=False))

    # --- REGRAS: Plano de Ação e Risco Acadêmico ---
    @Rule(
        Aluno(disciplinas_reprovadas=P(lambda r: r >= 4)),
        NOT(RiscoAcademico()),
    )
    def risco_jubilacao(self):
        self.declare(
            RiscoAcademico(
                alerta="ALTO RISCO DE JUBILAÇÃO",
                recomendacao="Rematrícula limitada a no máximo 2 disciplinas.",
            )
        )

    @Rule(
        Frequencia(porcentagem=P(lambda f: f <= 80.0)),
        Aluno(disciplinas_reprovadas=P(lambda r: r < 4)),
        NOT(RiscoAcademico()),
    )
    def risco_desfasamento_frequencia(self):
        self.declare(
            RiscoAcademico(
                alerta="Alerta de Risco de Desfasamento (Frequência Crítica <= 80%)",
                recomendacao="Rematrícula recomendada em no máximo 4 disciplinas com acompanhamento pedagógico.",
            )
        )

    @Rule(
        Frequencia(porcentagem=P(lambda f: f > 80.0)),
        Aluno(disciplinas_reprovadas=P(lambda r: r < 4)),
        NOT(RiscoAcademico()),
    )
    def risco_normal(self):
        self.declare(
            RiscoAcademico(
                alerta="Sem Risco Imediato",
                recomendacao="Rematrícula liberada para carga horária regular.",
            )
        )


# 3. Execução
def proc_alunos(arq = "alunos.csv"):
    engine = SistemaAcademico()

    print("OIIIIIIIIIIIIII")

    try:
        with open(arq, "r", newline="", encoding = "utf-8") as arquivo:
            leitor = csv.reader(arquivo)

            for linha in leitor:
                if not linha:
                    continue

                cpf = int(linha[0])
                nome = linha[1]
                dataNasc = linha[2]
                mat = int(linha[3])
                nota1 = float(linha[4])
                nota2 = float(linha[5])
                faltas = int(linha[6])
                reprovadas = int(linha[7])

                engine.reset()

                engine.declare(
                    Aluno(
                        cpf=cpf,
                        nome=nome,
                        dataNasc=dataNasc,
                        mat=mat,
                        nota1=nota1,
                        nota2=nota2,
                        faltas=faltas,
                        disciplinas_reprovadas=reprovadas
                    )
                )

                engine.run()

        # Exibição dos resultados
        print("\n" + "=" * 45)
        print(f" RELATÓRIO FINAL: {nome.upper()}")
        print("=" * 45)

        for fact_id, fact in engine.facts.items():
            if isinstance(fact, MediaGeral):
                print(f"• Média Geral: {fact['valor']:.2f}")
            elif isinstance(fact, Frequencia):
                print(f"• Frequência Calculada: {fact['porcentagem']:.1f}%")
            elif isinstance(fact, SituacaoAcademica):
                print(f"• Situação Acadêmica: {fact['status']}")
            elif isinstance(fact, PerfilMerito):
                bolsa = "SIM - Indicado para Bolsa por Mérito" if fact["elegivel"] else "NÃO - Não cumpre os requisitos"
                print(f"• Mérito / Bolsa: {bolsa}")
            elif isinstance(fact, RiscoAcademico):
                print(f"• Nível de Risco: {fact['alerta']}")
                print(f"• Plano de Ação: {fact['recomendacao']}")

        print("=" * 45)

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arq}' não encontrado.")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")


    if __name__ == "__main__":
        alunos_arq = "alunos.csv"
        proc_alunos(alunos_arq)