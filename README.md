Главной точкой входа приложения является main.py.

Для корректного запуска системы необходимо установить следующие библиотеки:
- stanza (pip install stanza)
- nltk (pip install --user -U nltk)
- torch (pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121)
- pymorphy3 (pip install pymorphy3)
- wikipediaapi (pip install wikipedia-api)
  
Для запуска вычислений на GPU необходимо установить соответствующие инструменты CUDA (https://developer.nvidia.com/cuda-downloads).

В случае проблем с обнаружением видеокарты, следует посетить данную страницу (https://stackoverflow.com/questions/57238344/i-have-a-gpu-and-cuda-installed-in-windows-10-but-pytorchs-torch-cuda-is-availa).

sample1.txt - текстовый документ с тестовым набором предложений для проверки работы системы.

Stopwords.txt - текстовый документ с набором стоп-слов. Может быть изменен пользователем по его усмотрению.

test_html.html в папке additional - пример сформированного системой семантического графа (из-за размера графа время загрузки страницы может составлять до 1 минуты в зависимости от используемого оборудования).
