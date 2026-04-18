console.log('JS DE NOTIFICACOES CARREGOU');

// ===============================
// ELEMENTOS DO DOM
// ===============================
document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById('notificacaoBtn');
    const modal = document.getElementById('modalNotificacoes');
    const fechar = document.getElementById('fecharModal');
    const badge = document.getElementById('badgeNotificacao');
    const tabela = document.getElementById('tabelaNotificacoes');

    // ===============================
    // VALIDAÇÃO DO DOM
    // ===============================
    if (!btn || !modal || !fechar || !badge || !tabela) {
        console.error('Elementos de notificação não encontrados');
        return;
    }

    // ===============================
    // EVENTOS
    // ===============================
    btn.onclick = () => modal.style.display = 'flex';
    fechar.onclick = () => modal.style.display = 'none';

    // ===============================
    // FORMATAR TEMPO
    // ===============================
    function formatarTempo(valor) {
        const minutos = parseInt(valor, 10);

        if (isNaN(minutos)) return '-';

        if (minutos < 60) return `${minutos} min`;

        const horas = Math.floor(minutos / 60);
        const restoMin = minutos % 60;

        if (horas < 24) {
            return restoMin > 0 ? `${horas}h ${restoMin}min` : `${horas}h`;
        }

        const dias = Math.floor(horas / 24);
        if (dias < 7) return `${dias} dia(s)`;

        const semanas = Math.floor(dias / 7);
        if (semanas < 4) return `${semanas} semana(s)`;

        const meses = Math.floor(semanas / 4);
        return `${meses} mês(es)`;
    }

    // ===============================
    // CARREGAR NOTIFICAÇÕES
    // ===============================
    function carregarNotificacoes() {

        // 🚨 usa URL dinâmica do Django
        if (typeof urlNotificacoes === "undefined") {
            console.error("URL de notificações não definida!");
            return;
        }

        fetch(urlNotificacoes)
            .then(res => {
                if (!res.ok) {
                    throw new Error("Erro na requisição: " + res.status);
                }
                return res.json();
            })
            .then(data => {

                tabela.innerHTML = '';

                if (data.total > 0) {
                    badge.style.display = 'inline-block';
                    badge.innerText = data.total;

                    data.notificacoes.forEach(n => {
                        const tr = document.createElement('tr');

                        tr.innerHTML = `
                            <td>${n.tarefa}</td>
                            <td class="${n.tipo === 'atrasada' ? 'text-danger' : 'text-warning'}">
                                ${n.status}
                            </td>
                            <td>
                                ${n.tipo === 'atrasada'
                                    ? `Atrasada há ${formatarTempo(n.tempo)}`
                                    : `Faltam ${formatarTempo(n.tempo)}`
                                }
                            </td>
                        `;

                        tabela.appendChild(tr);
                    });
                } else {
                    badge.style.display = 'none';
                    tabela.innerHTML = `
                        <tr>
                            <td colspan="3" class="text-center text-muted">
                                Nenhuma notificação
                            </td>
                        </tr>
                    `;
                }
            })
            .catch(err => console.error('Erro ao carregar notificações:', err));
    }

    // ===============================
    // INIT
    // ===============================
    carregarNotificacoes();
    setInterval(carregarNotificacoes, 60000);
});