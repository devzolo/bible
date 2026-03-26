import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'data')

# Load original genesis
with open(os.path.join(data_dir, 'genesis.json'), 'r', encoding='utf-8') as f:
    genesis = json.load(f)

# Chapter 1 BFL
ch1 = [
    {"v":1,"t":"No começo de tudo, Deus criou o céu e a terra."},
    {"v":2,"t":"A terra não tinha forma e estava vazia. Tudo era escuro sobre as águas profundas. E o Espírito de Deus se movia sobre as águas."},
    {"v":3,"t":"Então Deus disse: \"Que exista luz!\" E a luz passou a existir."},
    {"v":4,"t":"Deus viu que a luz era boa. Então ele separou a luz da escuridão."},
    {"v":5,"t":"Deus chamou a luz de Dia e a escuridão de Noite. Veio a tarde e veio a manhã. Esse foi o primeiro dia."},
    {"v":6,"t":"Então Deus disse: \"Que exista um espaço no meio das águas, separando as águas de cima das águas de baixo.\""},
    {"v":7,"t":"Deus fez esse espaço e separou as águas que ficaram abaixo dele das águas que ficaram acima. E assim aconteceu."},
    {"v":8,"t":"Deus chamou esse espaço de Céu. Veio a tarde e veio a manhã. Esse foi o segundo dia."},
    {"v":9,"t":"Então Deus disse: \"Que as águas debaixo do céu se juntem num só lugar e apareça a parte seca.\" E assim aconteceu."},
    {"v":10,"t":"Deus chamou a parte seca de Terra e o lugar onde as águas se juntaram de Mares. E Deus viu que era bom."},
    {"v":11,"t":"Então Deus disse: \"Que a terra produza plantas: vegetais que deem sementes e árvores que deem frutos com sementes, cada uma de acordo com a sua espécie.\" E assim aconteceu."},
    {"v":12,"t":"A terra produziu plantas: vegetais que dão sementes e árvores que dão frutos com sementes, cada uma de acordo com a sua espécie. E Deus viu que era bom."},
    {"v":13,"t":"Veio a tarde e veio a manhã. Esse foi o terceiro dia."},
    {"v":14,"t":"Então Deus disse: \"Que existam luzes no céu para separar o dia da noite. Elas vão servir para marcar os sinais, as estações, os dias e os anos.\""},
    {"v":15,"t":"\"Essas luzes vão ficar no céu para iluminar a terra.\" E assim aconteceu."},
    {"v":16,"t":"Deus fez as duas grandes luzes: a luz maior para governar o dia e a luz menor para governar a noite. Ele também fez as estrelas."},
    {"v":17,"t":"Deus colocou essas luzes no céu para iluminar a terra,"},
    {"v":18,"t":"para governar o dia e a noite e para separar a luz da escuridão. E Deus viu que era bom."},
    {"v":19,"t":"Veio a tarde e veio a manhã. Esse foi o quarto dia."},
    {"v":20,"t":"Então Deus disse: \"Que as águas se encham de seres vivos e que aves voem sobre a terra, pelo céu.\""},
    {"v":21,"t":"Deus criou os grandes animais do mar e todos os seres vivos que se movem nas águas, cada um de acordo com a sua espécie. Criou também todas as aves, cada uma de acordo com a sua espécie. E Deus viu que era bom."},
    {"v":22,"t":"Deus os abençoou e disse: \"Tenham filhotes e se multipliquem. Encham as águas dos mares. E as aves se multipliquem na terra.\""},
    {"v":23,"t":"Veio a tarde e veio a manhã. Esse foi o quinto dia."},
    {"v":24,"t":"Então Deus disse: \"Que a terra produza seres vivos de acordo com a sua espécie: animais domésticos, animais que se arrastam pelo chão e animais selvagens.\" E assim aconteceu."},
    {"v":25,"t":"Deus fez os animais selvagens, os animais domésticos e todos os animais que se arrastam pelo chão, cada um de acordo com a sua espécie. E Deus viu que era bom."},
    {"v":26,"t":"Então Deus disse: \"Vamos fazer o ser humano à nossa imagem, parecido conosco. Ele vai governar sobre os peixes do mar, as aves do céu, os animais domésticos, toda a terra e todos os animais que se arrastam pelo chão.\""},
    {"v":27,"t":"Deus criou o ser humano à sua imagem. À imagem de Deus ele o criou. Ele os criou homem e mulher."},
    {"v":28,"t":"Deus os abençoou e disse: \"Tenham filhos e se multipliquem. Encham a terra e tomem conta dela. Governem sobre os peixes do mar, as aves do céu e todos os animais que se movem sobre a terra.\""},
    {"v":29,"t":"Deus disse: \"Eu dou a vocês todas as plantas que produzem sementes sobre a terra e todas as árvores que dão frutos com sementes. Isso vai ser o alimento de vocês.\""},
    {"v":30,"t":"\"E para todos os animais da terra, todas as aves do céu e todos os seres que se arrastam pelo chão, eu dou todas as plantas verdes como alimento.\" E assim aconteceu."},
    {"v":31,"t":"Deus olhou para tudo o que tinha feito e viu que era muito bom. Veio a tarde e veio a manhã. Esse foi o sexto dia."},
]

# Chapter 2 BFL
ch2 = [
    {"v":1,"t":"Assim, o céu, a terra e tudo o que existe neles ficaram prontos."},
    {"v":2,"t":"No sétimo dia, Deus terminou todo o trabalho que tinha feito. E nesse dia ele descansou de tudo o que havia realizado."},
    {"v":3,"t":"Deus abençoou o sétimo dia e o separou como especial. Porque nesse dia ele descansou de toda a obra que tinha criado e feito."},
    {"v":4,"t":"Esta é a história de como o céu e a terra foram criados. No dia em que o Senhor Deus fez a terra e o céu,"},
    {"v":5,"t":"ainda não existia nenhuma planta no campo, e nenhuma erva tinha brotado. Isso porque o Senhor Deus ainda não tinha mandado chuva sobre a terra, e não havia ninguém para cultivar o solo."},
    {"v":6,"t":"Mas uma névoa subia da terra e molhava toda a superfície do solo."},
    {"v":7,"t":"Então o Senhor Deus formou o homem do pó da terra. Ele soprou nas narinas do homem o fôlego de vida, e o homem se tornou um ser vivo."},
    {"v":8,"t":"O Senhor Deus plantou um jardim no Éden, na direção do oriente. E colocou ali o homem que tinha formado."},
    {"v":9,"t":"O Senhor Deus fez nascer da terra todo tipo de árvore bonita de se ver e boa para comer. No meio do jardim estavam a árvore da vida e a árvore do conhecimento do bem e do mal."},
    {"v":10,"t":"Um rio saía do Éden para regar o jardim. Dali ele se dividia em quatro braços."},
    {"v":11,"t":"O primeiro se chama Pisom. Ele passa por toda a terra de Havilá, onde existe ouro."},
    {"v":12,"t":"O ouro dessa terra é de boa qualidade. Ali também se encontram resina perfumada e pedras preciosas."},
    {"v":13,"t":"O segundo rio se chama Giom. Ele passa por toda a terra de Cuxe."},
    {"v":14,"t":"O terceiro rio se chama Tigre. Ele corre pelo lado leste da Assíria. E o quarto rio é o Eufrates."},
    {"v":15,"t":"O Senhor Deus levou o homem e o colocou no jardim do Éden para cuidar dele e tomar conta."},
    {"v":16,"t":"O Senhor Deus deu esta ordem ao homem: \"Você pode comer à vontade de qualquer árvore do jardim."},
    {"v":17,"t":"Mas da árvore do conhecimento do bem e do mal, você não deve comer. Porque no dia em que comer dela, com certeza você vai morrer.\""},
    {"v":18,"t":"Depois o Senhor Deus disse: \"Não é bom que o homem fique sozinho. Vou fazer alguém que seja uma companheira ideal para ele.\""},
    {"v":19,"t":"O Senhor Deus tinha formado da terra todos os animais do campo e todas as aves do céu. Ele os trouxe até o homem para ver que nome ele daria a cada um. E o nome que o homem deu a cada ser vivo, esse ficou sendo o nome dele."},
    {"v":20,"t":"Adão deu nome a todos os animais domésticos, às aves do céu e a todos os animais do campo. Mas não se encontrou uma companheira ideal para ele."},
    {"v":21,"t":"Então o Senhor Deus fez Adão cair num sono muito profundo. Enquanto ele dormia, Deus tirou uma de suas costelas e fechou a carne no lugar."},
    {"v":22,"t":"Com a costela que tirou do homem, o Senhor Deus formou uma mulher e a trouxe até Adão."},
    {"v":23,"t":"Adão disse: \"Agora sim! Esta é osso dos meus ossos e carne da minha carne. Ela será chamada mulher, porque foi tirada do homem.\""},
    {"v":24,"t":"Por isso o homem deixa o pai e a mãe e se une à sua mulher. E os dois se tornam uma só carne."},
    {"v":25,"t":"O homem e sua mulher estavam nus e não sentiam vergonha."},
]

# Chapter 3 BFL
ch3 = [
    {"v":1,"t":"A serpente era o animal mais esperto de todos os que o Senhor Deus tinha feito. Ela disse à mulher: \"É verdade que Deus disse que vocês não podem comer de nenhuma árvore do jardim?\""},
    {"v":2,"t":"A mulher respondeu à serpente: \"Nós podemos comer das frutas das árvores do jardim."},
    {"v":3,"t":"Mas da fruta da árvore que está no meio do jardim, Deus disse: Não comam dela e nem toquem nela, senão vocês vão morrer.\""},
    {"v":4,"t":"A serpente disse à mulher: \"Vocês não vão morrer de jeito nenhum!"},
    {"v":5,"t":"Deus sabe que, no dia em que vocês comerem dessa fruta, os olhos de vocês vão se abrir. Vocês vão ficar como Deus, conhecendo o bem e o mal.\""},
    {"v":6,"t":"A mulher olhou para a árvore e viu que a fruta era boa de comer e bonita de ver. Ela também desejou aquela fruta para ter conhecimento. Então pegou a fruta, comeu e deu também ao seu marido, que estava com ela. E ele comeu."},
    {"v":7,"t":"Nessa hora, os olhos dos dois se abriram. Eles perceberam que estavam nus. Então costuraram folhas de figueira e fizeram roupas para se cobrir."},
    {"v":8,"t":"Quando chegou a brisa do fim da tarde, eles ouviram o Senhor Deus andando pelo jardim. Adão e sua mulher se esconderam entre as árvores, longe da presença do Senhor Deus."},
    {"v":9,"t":"O Senhor Deus chamou Adão e perguntou: \"Onde você está?\""},
    {"v":10,"t":"Adão respondeu: \"Eu ouvi a tua voz no jardim e fiquei com medo, porque estava nu. Por isso me escondi.\""},
    {"v":11,"t":"Deus perguntou: \"Quem disse a você que estava nu? Você comeu da árvore que eu mandei não comer?\""},
    {"v":12,"t":"Adão respondeu: \"A mulher que tu me deste como companheira, ela me deu a fruta da árvore, e eu comi.\""},
    {"v":13,"t":"O Senhor Deus perguntou à mulher: \"Por que você fez isso?\" A mulher respondeu: \"A serpente me enganou, e eu comi.\""},
    {"v":14,"t":"Então o Senhor Deus disse à serpente: \"Já que você fez isso, você é maldita entre todos os animais. Você vai andar de barriga no chão e vai comer pó todos os dias da sua vida."},
    {"v":15,"t":"Eu vou colocar inimizade entre você e a mulher, e entre os seus descendentes e os descendentes dela. Eles vão esmagar a sua cabeça, e você vai ferir o calcanhar deles.\""},
    {"v":16,"t":"Para a mulher, Deus disse: \"Eu vou aumentar muito o seu sofrimento na gravidez. Você vai ter filhos com dor. Você vai desejar o seu marido, e ele vai dominar sobre você.\""},
    {"v":17,"t":"E para Adão, disse: \"Já que você ouviu a sua mulher e comeu da árvore que eu mandei não comer, a terra é maldita por sua causa. Você vai sofrer para tirar o seu alimento dela todos os dias da sua vida."},
    {"v":18,"t":"A terra vai produzir espinhos e ervas ruins para você. E você vai comer as plantas do campo."},
    {"v":19,"t":"Você vai trabalhar e suar muito para conseguir o seu pão, até o dia em que voltar para a terra. Porque você foi feito do pó, e ao pó você vai voltar.\""},
    {"v":20,"t":"Adão deu à sua mulher o nome de Eva, porque ela seria a mãe de todos os seres humanos."},
    {"v":21,"t":"O Senhor Deus fez roupas de pele de animal para Adão e sua mulher, e os vestiu."},
    {"v":22,"t":"Então o Senhor Deus disse: \"O homem agora ficou como um de nós, conhecendo o bem e o mal. Ele não pode estender a mão, pegar também da árvore da vida, comer e viver para sempre.\""},
    {"v":23,"t":"Por isso, o Senhor Deus expulsou o homem do jardim do Éden, para que ele trabalhasse a terra de onde tinha sido feito."},
    {"v":24,"t":"Depois de expulsar o homem, Deus colocou querubins no lado leste do jardim do Éden. Colocou também uma espada de fogo que girava para todos os lados, para guardar o caminho da árvore da vida."},
]

# Build chapters: use BFL for 1-3, ACF original for 4-50
bfl_translations = {1: ch1, 2: ch2, 3: ch3}

new_chapters = []
for ch in genesis['chapters']:
    c_num = ch['c']
    if c_num in bfl_translations:
        bfl_verses = bfl_translations[c_num]
        bfl_map = {v['v']: v['t'] for v in bfl_verses}
        new_verses = []
        for orig_v in ch['verses']:
            new_verses.append({
                "v": orig_v['v'],
                "o": orig_v['o'],
                "t": bfl_map.get(orig_v['v'], orig_v['t'])
            })
        new_chapters.append({"c": c_num, "verses": new_verses})
    else:
        new_chapters.append(ch)

result = {
    "id": genesis['id'],
    "name": genesis['name'],
    "nameOrig": genesis['nameOrig'],
    "lang": genesis['lang'],
    "testament": genesis['testament'],
    "section": genesis['section'],
    "chapters": new_chapters
}

os.makedirs(os.path.join(data_dir, 'bfl'), exist_ok=True)
with open(os.path.join(data_dir, 'bfl', 'genesis.json'), 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

print(f"Done! Genesis BFL: {len(new_chapters)} chapters")
print(f"Translated: chapters 1-3")
print(f"ACF fallback: chapters 4-50")
