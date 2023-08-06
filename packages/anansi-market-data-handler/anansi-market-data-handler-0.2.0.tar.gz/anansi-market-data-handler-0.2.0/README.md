# Anansi Market Data Handler

Pacote python cujo objetivo é servir como abstração para aquisição,
armazenamento, leitura e apresentação de dados de mercado, procurando
ser agnóstico quanto à fonte dados[^1].

A ***API*** deste pacote fornece uma interface para os objetos de dados
cujos *métodos* procuram refletir a necessidade de quem lida,
usualmente, com dados deste tipo - os **traders** - abstraindo, por
exemplo, a complexidade matemática da implementação dos indicadores de
mercado, como médias móveis, bandas de bollinger e afins sobre um
conjunto de *candlesticks*, por exemplo.

[^1]: Corretoras, *exchanges*, *brokers* são nomenclaturas comuns para
essas fontes.
