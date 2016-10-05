
Código escrito em python compatível com a versão 2.7

Módulos necessários:
numpy, scipy, opencv, sqlite3

Para calcular os descritores e indexar:

python cbir.py

Para executar uma busca:

python main.py <path_imagem_entrada> <k-proximos> <metodo>

metodo={fourier,sift}

============================

exemplo:
python main.py 1.jpg 5 sift


Obs: As imagens devem estar em uma pasta chamada 'images' no mesmo diretório dos executáveis.
