from django.db import models
import uuid

def generate_uuid():
    return uuid.uuid4().hex


# ==============================
#      COLABORADORES
# ==============================
class Colaborador(models.Model):
    STATUS_CHOICES = [
        ('desligado', 'Desligado'),
        ('ferias', 'Férias'),
        ('ativo', 'Ativo'),
    ]

    id = models.CharField(
        max_length=32,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    nome = models.CharField(max_length=150)
    imagem = models.ImageField(upload_to='colaboradores/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    telefone = models.CharField(max_length=40, blank=True, null=True)
    numero_empresa = models.CharField(max_length=40, blank=True, null=True)
    data_admissao = models.DateTimeField()

    def __str__(self):
        return self.nome


# ==============================
#            SETORES
# ==============================
class Setor(models.Model):
    MOBILIA_CHOICES = [
        ('pouca', 'Pouca'),
        ('media', 'Média'),
        ('muita', 'Muita'),
    ]

    id = models.CharField(
        max_length=32,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='/var/www/taskif/tcc/main/media/setores/', blank=True, null=True)
    dimensao = models.CharField(max_length=100)
    natureza_piso = models.CharField(max_length=100)
    area_envidracada = models.CharField(max_length=100)
    mobilia = models.CharField(max_length=10, choices=MOBILIA_CHOICES)

    def __str__(self):
        return self.nome


# ==============================
#    TABELAS INTERMEDIÁRIAS
# ==============================
class TarefaSetor(models.Model):
    id = models.CharField(
        max_length=32,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    tarefa = models.ForeignKey("Tarefa", on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)  
    # PROTECT → impede excluir setor se tiver tarefa ligada

    def __str__(self):
        return f"{self.tarefa.titulo} -> {self.setor.nome}"


class TarefaColaborador(models.Model):
    id = models.CharField(
        max_length=32,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    tarefa = models.ForeignKey("Tarefa", on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT)
    # PROTECT → impede excluir colaborador se estiver vinculado a tarefa

    def __str__(self):
        return f"{self.tarefa.titulo} -> {self.colaborador.nome}"


# ==============================
#            TAREFAS
# ==============================
class Tarefa(models.Model):
    SUJEIRA_CHOICES = [
        ('baixo', 'Baixo'),
        ('medio', 'Médio'),
        ('alto', 'Alto'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    PRIORIDADE_CHOICES = [
        ('baixo', 'Baixo'),
        ('medio', 'Médio'),
        ('alto', 'Alto'),
    ]

    id = models.CharField(
        max_length=32,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    nivel_sujeira = models.CharField(max_length=10, choices=SUJEIRA_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    data_inicio = models.DateTimeField()
    data_previsao_termino = models.DateTimeField()
    data_termino = models.DateTimeField(blank=True, null=True)

    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES)

    # RELACIONAMENTOS FIXADOS COM through ↓↓↓
    colaboradores = models.ManyToManyField(
        Colaborador,
        through="TarefaColaborador",
        related_name="tarefas"
    )

    setores = models.ManyToManyField(
        Setor,
        through="TarefaSetor",
        related_name="tarefas"
    )

    def __str__(self):
        return self.titulo


from django.db import models

class ConfiguracaoSistema(models.Model):
    email_institucional = models.EmailField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "Configurações do Sistema"

