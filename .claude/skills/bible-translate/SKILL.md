---
name: bible-translate
description: "Traduz textos bíblicos para português brasileiro acessível e natural (BFL — Bíblia Fácil de Ler). Use esta skill sempre que precisar traduzir versículos, capítulos ou livros da Bíblia para linguagem simples e clara que qualquer brasileiro entenda, independente da região. Trigger: traduzir bíblia, tradução bíblica, BFL, linguagem fácil, tradução acessível, português simples bíblia."
---

# Tradução Bíblica — BFL (Bíblia Fácil de Ler)

## Objetivo

Produzir uma tradução da Bíblia em português brasileiro contemporâneo, natural e universal — compreensível para qualquer pessoa em qualquer região do Brasil, incluindo jovens e adultos com dificuldade de leitura.

## Identidade da Tradução

- **Sigla**: BFL (Bíblia Fácil de Ler)
- **Método**: Equivalência dinâmica — transmitir o significado, não traduzir palavra por palavra
- **Tom**: Acolhedor, claro, direto — como alguém explicando com carinho
- **Público**: Jovens e adultos, especialmente quem tem dificuldade de compreensão

## Processo de Tradução (por versículo)

Para cada versículo, siga esta sequência:

1. **Ler o texto original** (hebraico/grego no campo `o`)
2. **Ler a tradução ACF** (campo `t`) como referência
3. **Compreender o significado** — o que o autor quis dizer no contexto original?
4. **Reescrever em português brasileiro natural** seguindo as diretrizes abaixo
5. **Verificar fidelidade** — o significado do original está preservado? Nada foi adicionado nem omitido?

## Diretrizes de Linguagem

### Palavras e Frases

- Use palavras do dia a dia: "feliz" em vez de "bem-aventurado", "castigo" em vez de "flagelo"
- Frases curtas (máximo ~25 palavras por frase quando possível)
- Ordem direta: sujeito + verbo + complemento (evitar inversões rebuscadas)
- Evite palavras que exijam dicionário: "contenda" → "briga", "concupiscência" → "desejo errado", "iniquidade" → "maldade"
- Palavras arcaicas devem ser substituídas: "vós" → "vocês", "eis" → "vejam", "porquanto" → "porque", "outrossim" → também

### Regionalismo

- Use português neutro que funcione do Oiapoque ao Chuí
- Evite gírias regionais (nem "mano", nem "oxe", nem "bah")
- Evite expressões que só fazem sentido numa região
- Prefira vocabulário que aparece em jornais, escola e TV aberta

### Nomes e Termos Técnicos

- Nomes de pessoas: manter como são conhecidos em português (Moisés, Abraão, Jesus, Paulo)
- Nomes de lugares: usar a forma mais conhecida (Jerusalém, Egito, Babilônia)
- Termos teológicos que não têm substituto simples: manter e explicar no contexto se possível
  - "batismo" — manter (é amplamente conhecido)
  - "propiciatório" → "lugar de perdão" ou "tampa da arca onde Deus perdoava"
  - "holocausto" → "oferta queimada para Deus"
- Medidas e moedas: converter para algo compreensível quando possível
  - "côvado" → "meio metro" ou manter com contexto
  - "denário" → "salário de um dia de trabalho"

### Estilo e Fluidez

- A tradução deve soar como se alguém estivesse contando a história — fluida e envolvente
- Manter o ritmo poético em textos poéticos (Salmos, Provérbios, Cânticos)
- Em narrativas, manter a ação viva e o leitor engajado
- Em cartas (epístolas), o tom deve ser pessoal e direto, como uma carta de verdade
- Em profecias, manter a gravidade sem ser obscuro

### O que NÃO fazer

- Não adicionar interpretação teológica — traduzir o que está escrito
- Não simplificar a ponto de perder nuances importantes
- Não usar linguagem infantil — é fácil, não é para crianças
- Não parafrasear demais — é tradução, não comentário
- Não usar "você" para Deus (manter "tu" ou reestruturar a frase)
- Não remover metáforas famosas — "O Senhor é meu pastor" permanece, por exemplo

## Formato de Saída

Manter exatamente o mesmo formato JSON do projeto. Cada arquivo de livro em `static/data/bfl/{bookId}.json`:

```json
{
  "id": "genesis",
  "name": "Gênesis",
  "nameOrig": "בראשית",
  "lang": "hebrew",
  "testament": "AT",
  "section": "pentateuco",
  "chapters": [
    {
      "c": 1,
      "verses": [
        {
          "v": 1,
          "o": "בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַ/שָּׁמַ֖יִם וְ/אֵ֥ת הָ/אָֽרֶץ",
          "t": "No começo de tudo, Deus criou o céu e a terra."
        }
      ]
    }
  ]
}
```

O campo `o` (original hebraico/grego) permanece idêntico ao arquivo ACF. Só o campo `t` muda.

## Fluxo de Trabalho

1. Ler o arquivo fonte de `static/data/{bookId}.json` (tradução ACF + texto original)
2. Traduzir capítulo por capítulo
3. Salvar em `static/data/bfl/{bookId}.json`
4. Seguir a ordem canônica dos livros (Gênesis → Apocalipse)

## Exemplos de Tradução

### Gênesis 1:1
- **Original**: בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַ/שָּׁמַ֖יִם וְ/אֵ֥ת הָ/אָֽרֶץ
- **ACF**: No princípio criou Deus o céu e a terra.
- **BFL**: No começo de tudo, Deus criou o céu e a terra.

### João 3:16
- **Original**: Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον...
- **ACF**: Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito...
- **BFL**: Deus amou o mundo tanto, tanto, que entregou seu único Filho...

### Salmo 23:1
- **Original**: יְהוָ֥ה רֹ֝עִ֗י לֹ֣א אֶחְסָֽר
- **ACF**: O Senhor é o meu pastor, nada me faltará.
- **BFL**: O Senhor é o meu pastor, e nada vai me faltar.

### Romanos 8:28
- **ACF**: E sabemos que todas as coisas contribuem juntamente para o bem daqueles que amam a Deus...
- **BFL**: Nós sabemos que Deus faz tudo cooperar para o bem de quem o ama...

## Checklist de Qualidade (por capítulo)

- [ ] Cada versículo preserva o significado do original?
- [ ] A linguagem é simples e clara?
- [ ] Não há regionalismos ou gírias?
- [ ] O texto flui naturalmente quando lido em voz alta?
- [ ] Nomes próprios estão na forma conhecida em português?
- [ ] Termos técnicos foram simplificados ou contextualizados?
- [ ] O JSON está no formato correto?
