# Alerta de Chuva

[![codecov](https://codecov.io/gh/rodrigoneal/alerta-chuva/graph/badge.svg?token=FQY0AP0SXM)](https://codecov.io/gh/rodrigoneal/alerta-chuva)
[![GitHub Actions](https://github.com/rodrigoneal/alerta-chuva/actions/workflows/github-actions.yml/badge.svg)](https://github.com/rodrigoneal/alerta-chuva/actions/workflows/github-actions.yml)

## Introdução
Este projeto surge da necessidade crucial, uma vez que resido próximo ao rio Acari, que tem sido negligenciado pelas autoridades públicas ao longo dos anos. Com os impactos do aquecimento global e o fenômeno El Niño, a previsão é de um aumento nas chuvas. Portanto, o objetivo do alerta de chuva é notificar sobre registros de chuvas na cabeceira do rio Acari ou a proximidade de nuvens em minha região ou na cabeceira.

Inicialmente, a intenção é enviar alertas pelo Telegram por meio de um bot sempre que indícios de chuvas fortes forem detectados. Isso é importante, já que posso estar dormindo e não ter consciência imediata do que está acontecendo.

## Funcionamento Técnico

### Detecção de Chuva
A classe `Chuva` contém métodos como `chuva_detectada`, `choveu_fraca`, `choveu_moderada`, `choveu_forte` e `choveu_muito_forte`. Esses métodos realizam web scraping no site da prefeitura para obter informações sobre o acumulado de chuvas em intervalos de 15 minutos. Ainda estou decidindo se devo armazenar todos os dados ou substituir apenas o último registro.

Quando for detectada chuva forte em áreas específicas, o sistema enviará notificações pelo Telegram. Planejo também implementar um método utilizando inteligência artificial para prever possíveis transbordamentos do rio, treinando o modelo com dados históricos sempre que isso ocorrer.

### Radar Meteorológico
A classe `Radar` possui o método `radar`, que captura imagens do radar e analisa a presença de nuvens sobre determinados bairros. Atualmente, mapeei apenas alguns bairros, mas pretendo melhorar a precisão dessa análise futuramente.

Por enquanto, fiz o mapeamento dos bairros de Campo Grande, Ilha do Governador e Parque Columbia, além de definir as zonas.

O processo de verificação começa dos níveis mais amplos para os mais específicos: primeiramente, verifica-se a presença de chuva na cidade do Rio de Janeiro, depois na cabeceira do rio e por fim no meu bairro.

Se desejar contribuir mapeando seu próprio bairro, sinta-se à vontade para fazer um fork e me informar.

### Notificação de Chuva
Ainda não comecei a trabalhar nela, mas pretendo fazer isso logo, Pois o verão está logo ali.

Em caso de dúvidas, estou à disposição. Abraços.
