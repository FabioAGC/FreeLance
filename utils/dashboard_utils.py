from utils.db_utils import listar_clientes, listar_servicos

def get_dashboard_metrics():
    clientes = listar_clientes()
    servicos = listar_servicos()
    total_clientes = len(clientes)
    ativos = [s for s in servicos if s[5].lower() == 'em andamento']
    pendentes = [s for s in servicos if s[5].lower() == 'pendente']
    concluidos = [s for s in servicos if s[5].lower() == 'concluido']
    total_ativos = len(ativos)
    total_pendentes = len(pendentes)
    faturamento = sum(float(s[3]) - float(s[4]) for s in concluidos)
    return {
        'total_clientes': total_clientes,
        'total_ativos': total_ativos,
        'total_pendentes': total_pendentes,
        'faturamento': faturamento,
        'recentes': servicos[-3:] if servicos else []
    }
