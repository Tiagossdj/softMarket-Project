document.addEventListener('DOMContentLoaded', () => {
  const reportForm = document.getElementById('reportConfigForm');
  const exportExcelBtn = document.querySelector('.btn-export-header');
  const chartContainer = document.querySelector('.chart-container');
  const reportDataTable = document.querySelector('.report-data table tbody');
  const reportDataTableHeader = document.querySelector('.report-data table thead tr');

  async function handleReportSubmit(e) {
      e.preventDefault();
      
      const reportType = document.getElementById('reportType').value;
      const chartType = document.getElementById('chartType').value;
      let dataInicio = document.getElementById('dataInicio').value;
      let dataFim = document.getElementById('dataFim').value;

      // Relatórios que não exigem datas
      const relatoriosSemData = ["estoqueBaixo", "produtosVendidos", "fornecedores", "estoque", "pedidosEstoque"];

      // Ajuste de datas
      if (dataInicio && !dataFim) dataFim = dataInicio;
      if (relatoriosSemData.includes(reportType)) {
          dataInicio = "";
          dataFim = "";
      }

      // Validação de datas
      if (!relatoriosSemData.includes(reportType) && (!dataInicio || !dataFim)) {
          alert('Por favor, selecione uma data ou um período válido.');
          return;
      }

      const reportRoutes = {
          'vendas': 'http://127.0.0.1:5000/relatorio_vendas_json',
          'estoqueBaixo': 'http://127.0.0.1:5000/relatorio_estoque_baixo_json',
          'produtosVendidos': 'http://127.0.0.1:5000/relatorio_compras_json',
          'vendasDiarias': 'http://127.0.0.1:5000/relatorio_vendas_dia_json',
          'fornecedores': 'http://127.0.0.1:5000/relatorio_fornecedores_json',
          'estoque': 'http://127.0.0.1:5000/relatorio_estoque_json',
          'pedidosEstoque': 'http://127.0.0.1:5000/relatorio_pedidos_estoque_json'
      };

      const graphRoutes = {
          'vendas': 'http://127.0.0.1:5000/grafico_vendas_por_produto',
          'estoqueBaixo': 'http://127.0.0.1:5000/grafico_estoque_baixo',
          'produtosVendidos': 'http://127.0.0.1:5000/grafico_compras_por_produto',
          'vendasDiarias': 'http://127.0.0.1:5000/grafico_vendas_dia',
          'fornecedores': 'http://127.0.0.1:5000/grafico_fornecedores'
      };

      const reportRoute = reportRoutes[reportType];
      const graphRoute = graphRoutes[reportType];

      if (!reportRoute) {
          alert('Tipo de relatório não suportado');
          return;
      }

      const reportUrl = new URL(reportRoute);
      const graphUrl = graphRoute ? new URL(graphRoute) : null;

      // Configuração de parâmetros de URL
      if (dataInicio) {
          reportUrl.searchParams.append("data_inicio", dataInicio);
          if (graphUrl) graphUrl.searchParams.append("data", dataInicio);
      }
      if (dataFim) reportUrl.searchParams.append("data_fim", dataFim);
      if (graphUrl) graphUrl.searchParams.append("tipo_grafico", chartType);

      // Limpar containers
      chartContainer.innerHTML = '';
      reportDataTable.innerHTML = '';
      reportDataTableHeader.innerHTML = '';

      try {
          // Processamento do gráfico
          if (graphUrl) {
              const graphResponse = await fetch(graphUrl);
              if (graphResponse.ok) {
                  const graphBlob = await graphResponse.blob();
                  atualizarGrafico(graphBlob);
              } else {
                  chartContainer.innerHTML = '<p>Não foi possível carregar o gráfico.</p>';
              }
          }

          // Processamento do relatório
          const reportResponse = await fetch(reportUrl);
          
          if (!reportResponse.ok) {
              throw new Error('Falha ao carregar dados do relatório');
          }

          const reportData = await reportResponse.json();
          
          if (reportData.length === 0) {
              reportDataTable.innerHTML = '<tr><td colspan="5">Não há dados disponíveis.</td></tr>';
              return;
          }

          // Criar cabeçalho dinâmico
          const headers = Object.keys(reportData[0]);
          const headerRow = headers.map(header => `<th>${header}</th>`).join('');
          reportDataTableHeader.innerHTML = headerRow;

          // Preencher tabela com dados
          reportData.forEach(row => {
              const tr = document.createElement('tr');
              for (let key in row) {
                  const td = document.createElement('td');
                  td.textContent = row[key];
                  tr.appendChild(td);
              }
              reportDataTable.appendChild(tr);
          });

      } catch (error) {
          console.error('Erro:', error);
          alert('Não foi possível carregar o relatório.');
          chartContainer.innerHTML = '<p>Erro ao carregar gráfico.</p>';
          reportDataTable.innerHTML = '<tr><td colspan="5">Erro ao carregar dados.</td></tr>';
      }
  }

  function atualizarGrafico(imagemBlob) {
      const imageUrl = URL.createObjectURL(imagemBlob);
      const img = document.createElement('img');
      img.src = imageUrl;
      img.classList.add('chart-image');
      chartContainer.appendChild(img);
  }

  async function handleExportExcel() {
      const reportType = document.getElementById('reportType').value;
      let dataInicio = document.getElementById('dataInicio').value;
      let dataFim = document.getElementById('dataFim').value;

      if (!reportType) {
          alert('Selecione um tipo de relatório primeiro.');
          return;
      }

      const reportRoutes = {
        'vendas': 'http://127.0.0.1:5000/relatorio_vendas_json',
        'estoqueBaixo': 'http://127.0.0.1:5000/relatorio_estoque_baixo_json',
        'produtosVendidos': 'http://127.0.0.1:5000/relatorio_compras_json',
        'vendasDiarias': 'http://127.0.0.1:5000/relatorio_vendas_dia_json',
        'fornecedores': 'http://127.0.0.1:5000/relatorio_fornecedores_json',
        'estoque': 'http://127.0.0.1:5000/relatorio_estoque_json',
        'pedidosEstoque': 'http://127.0.0.1:5000/relatorio_pedidos_estoque_json'
    };

      const reportRoute = reportRoutes[reportType];
      const reportUrl = new URL(reportRoute);

      if (dataInicio) reportUrl.searchParams.append("data_inicio", dataInicio);
      if (dataFim) reportUrl.searchParams.append("data_fim", dataFim);

      try {
          const reportResponse = await fetch(reportUrl);
          if (!reportResponse.ok) {
              throw new Error('Falha ao carregar dados do relatório');
          }
          const reportBlob = await reportResponse.blob();
          baixarRelatorio(reportBlob, `${reportType}.xlsx`);
      } catch (error) {
          console.error('Erro:', error);
          alert('Não foi possível baixar o relatório.');
      }
  }

  function baixarRelatorio(blob, fileName) {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
  }

  // Adicionar event listeners
  reportForm.addEventListener('submit', handleReportSubmit);
  exportExcelBtn.addEventListener('click', handleExportExcel);
});