# Desafio Luizalab

Esta breve api foi produzida utilizando python[#is_life] e tornadoweb.

Desafio sugerido por Renato Pedigoni.

A solicitacao é que fosse produzido um codigo simples para validar minha forma de programar.

Para este teste foi utilizado o banco de dados SQLite por ser altamente portavel e de facil manuseio para realizacao de testes.

Para abstracao da execução das querys junto ao banco de dados foi utilizado o SQLAlchemy, é facil de ser utilizado e atende muito bem ao padrao ORM.

Documentado utilizando o projeto aberto swagger.io

Code review pode ser feito por este repositório.

## Executando o projeto
Para executar o projeto monte o virtualenv para testes, baseado nos requeriments no projeto e utilize o arquivo app.py.
Segue brevemente como fazer isso:

```bash
# inicializando
$ git clone https://github.com/LaercioPatricio/desafio_luizalab
$ cd 'folder'
$ mkdir env
$ virtualenv env
$ source env/bin/activate
$ (env)cd [project_dir]
$ (env)pip install -r requiments.txt
..
$ (env)python app.py

```
Pronto projeto rodando agora é só utilizar a url no seu navegador
http://localhost:5000/static/docs/index.html


### Rodando os testes do CRUD utilizando a abstração programada por mim
```bash

python test_crud.py

```
### Rodando os testes do tornadoweb utilizando urls da API produzida como desafio

```bash
python test_tornado_app.py

```

## Documentação
Para vizualizar a documentação dos serviços expostos, após inicializar o serviço, utilize a url: http://localhost:5000/static/docs/index.html

## Documentação do código
Para visualizar a documentação do código após inicializar o serviço, utilize a url: http://localhost:5000/static/docs/__init__.html no navegador

