console.log('JS DE NOTIFICACOES CARREGOU');

const btn = document.getElementById('notificacaoBtn');
const modal = document.getElementById('modalNotificacoes');
const fechar = document.getElementById('fecharModal');
const badge = document.getElementById('badgeNotificacao');
const tabela = document.getElementById('tabelaNotificacoes');

btn.onclick = () => modal.style.display = 'flex';
fechar.onclick = () => modal.style.display = 'none';

function carregarNotificacoes() {
    fetch('/notificacoes/')
        .then(res => res.json())
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
                        <td>${n.tempo}</td>
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
        .catch(err => console.error(err));
}

carregarNotificacoes();
setInterval(carregarNotificacoes, 60000);

