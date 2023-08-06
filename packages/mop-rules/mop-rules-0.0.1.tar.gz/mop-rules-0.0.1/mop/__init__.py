# -*- coding: utf-8 -*-
"""
Данный модуль реализует полезные инструменты для автоматизации
модифицирования файлов различных расширений
--------------------------------------------------------------------------
Сам модуль служит полезным инструментом для разработчиков на языке Python,
способным автоматизировать рядовые рутинные задачи.
Например:
  a) добавление строки шебанга и кодировки в начало скрипта Python
     #!/usr/bin/env python3
     # -*- coding: utf-8 -*-
  б) валидация файла, то есть:
    * удаление повторяющихся строк описанных выше модификаторов(шебанг и кодировка)
    * исправление "неправильной - не переносимой" строки шебанга:
        - #!/bin/python3
        - #!/usr/bin/python3 # какой-то комментарий
        - пробелы перед и(или) после шебанга и др.
  в) применение изложенных операций выше к множеству файлов,
     имена которых можно получить:
       * загрузив из текщего рабочего каталога (просто вызов mop.py)
       * передав в виде аргумента командной строки имена файл(а)ов и(или) каталог(а)ов
       * через перенаправление потока ввода:
           + some_pogram | mop.py
           + 'mop.py < some_text_file[.txt]' (файл не обязан иметь расширение)
             в последнем случаем имена файлов или каталогов должны начинаться
             каждый с новой строки
  г) аниме
"""

import os
import stat
import sys

from chardet.universaldetector import UniversalDetector

DEF_ENCODING_FILES = sys.getdefaultencoding()
DEF_ENCODING_NAME_FILES = sys.getfilesystemencoding()

SHEBANG = '#!/usr/bin/env python3'
ENCODING = '# -*- coding: utf-8 -*-'
SPECS = [SHEBANG, ENCODING]

PY = ['py', 'pyw']

def get_encoding(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done: break
    detector.close()
    return detector.result['encoding']

def open_for_read(file, *pargs, **kargs):
    """
    Функция открытия файла, предотвращающая ошибки чтения из-за кодировки файла
    Имеет те же аргументы что и функция

    open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None,
         closefd=True, opener=None)

    КРОМЕ атрибута encoding - функция автоматически подбирает нужную кодировку
    """

    # функцияя open_for_reed может применяться в каком-нибудь цикле
    # при обходе файлов
    # и по ресурсам будет очень затратно каждый раз вызывать
    # get_encoding(file) - чтобы получить кодировку файла

    # Поэтому при каждом вызове мы будем сохранять кодировку
    # УСПЕШНО открытого файла(то есть без ошибок)
    # и с этой же кодировки будем пытаться открыть уже СЛЕДУЮЩИЙ файл
    try:
        enc = open_for_read.last_enc     # пытаемся извлечь последнюю удачную кодировку
    except:
        enc = DEF_ENCODING_FILES         # иначе берём ту, что по умолчанию

    try:
        # пытаемся открыть файл с кодировкой, сохранённой
        # после предыдущего вызова функции open_for_read
        f_obj = open(file, *pargs, encoding=enc, **kargs)
        # здесь стоит отметить важну проблему,
        # состоящую в том, что сразу ошибка не вылезет
        # например если открыть файл с кодировкой 'Windows-1252',
        # используя стандартную кодировку 'utf-8'
        # то ошибка появится только ПРИ ЧТЕНИИ
        f_obj.read(20)       # пытаемся прочитать немного символов из файла
        f_obj.seek(0)        # если ошибки нет, то возвращаемся к началу файла
    except:
        # закрываем файл чтобы удалить ссылки на него
        f_obj.close()

        # используем сложную и ресурсоёмкую функцию get_encoding
        # чтобы узнать истинную кодировку
        # UPD: сюда тоже можно добавить обработку ошибок 
        enc = get_encoding(file)
        f_obj = open(file, *pargs, encoding=enc, **kargs)

    # сохраняем значение кодировки, при которой файл удачно был открыт
    # используем здесь интересный приём
    # сохраняем  кодировку как атрибут нашей функции - тем самым не используя
    # глобальные переменные
    open_for_read.last_enc = enc

    # возвращаем открытый файл
    return f_obj


def getNFirstLines(f_obj, N):
    """
    Возвращает из 'file_obj' первые 'N' строк в виде списка,
    причом длина этого списка <= N
    То есть сработает коректно даже если в файле меньше N строк
    """
    f_obj.seek(0)
    res = []
    for _ in range(N):

        line = f_obj.readline()

        if not line:
            break
        else:
            for spec in SPECS:
                if spec == line.strip():
                    res.append(spec)
                    break
            else:
                res.append(line.rstrip())

    f_obj.seek(0)
    return res

def addMods(filename, *strings, deep=5, newline = '\n', repeat=False):
    with open_for_read(filename, 'r+') as fio:

        if not repeat:
            nLines = getNFirstLines(fio, deep)
            inserties = [str for str in strings if str not in nLines]
        else:
            inserties = strings

        if inserties:
            data = fio.read()

            for line in inserties:
                data = line + newline + data

            fio.seek(0)
            fio.write(data)
            fio.truncate()

def leadToValid(filename, deep=5):
    """
    Привести к валидному виду
    """
    with open_for_read(filename, 'r+') as fio:
        nLines = getNFirstLines(fio, deep)

        for i in range(len(nLines)):
            if nLines[i] != SHEBANG and (nLines[i].lstrip().startswith('#!') and 'python' in nLines[i]):
                nLines[i] = SHEBANG

        for spec in SPECS:
            if spec in nLines:
                while nLines.count(spec) > 1:
                    nLines.pop(nLines.index(spec))

        if SHEBANG in nLines:
            indexShebang = nLines.index(SHEBANG)
            if indexShebang != 0:
                nLines.pop(indexShebang)
                nLines.insert(0, SHEBANG)


        nLines = [line + '\n' for line in nLines]
        lines = fio.readlines()
        lines[:deep] = nLines

        fio.seek(0)
        fio.writelines(lines)
        fio.truncate()

def getScripts(from_dir, *f_exts, add_subs=True):
    """
    Находим все ФАЙЛЫ с расширением '.py' (или лубым(И) другим(И) указанным(И))
    в переданном каталоге [и его подкаталогах (по умолчанию)]

    'from_dir' : Каталог, в котором ведётся поиск файлов-скриптов
    ----------------------------------------------------------------
    'f_exts'   : Кортеж расширений, по которым ведётся поиск файлов.
                 Если расширения файлов не были переданы в функцию,
                 то просто будут найдены все возможные файлы
    ----------------------------------------------------------------
    'add_subs' : Флаг, отвечающий за добавление в поиск файлов,
                 всех подкаталогов указанной директории 'from_dir'
    """

    f_exts = set(ext.lower() for ext in f_exts)

    scripts = []
    for (cur_dir, subs, files) in os.walk(from_dir):

        # если при поиске файлов не нужно посещать подкаталоги
        # удаляем их из обхода
        if not add_subs:
            subs.clear()

        # заметим что в списке files расположены только имена ФАЙЛОВ
        # то есть дополнительную проверку на то, является ли
        # filename - файлом на диске, проводить НЕ нужно
        for filename in files:
            # получаем расширение файла
            cur_ext = os.path.splitext(filename)[1]
            # убираем символ разделяющий расширение от имени файла
            # например БЫЛО - '.py' СТАНЕТ 'py'
            cur_ext = cur_ext[1:]
            # приводим расширение к нижнимему регистру
            # то есть может быть 'PY', а не 'py' - а это разные строки
            cur_ext = cur_ext.lower()
            # если такое расширение есть в множестве
            if cur_ext in f_exts:
                # собираем полное имя файла
                path = os.path.join(cur_dir, filename)
                # добавляем в результирующий список файлов
                scripts.append(path)

    return scripts

def makeExecFile(filename):
    """
    Дать файлу права на выполнение
    """
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def main():

    if len(sys.argv) == 1:
        # если stdin связан с КОНСОЛЬЮ
        # а не через перенправление ввода (<, |) файлов и программ
        if sys.stdin.isatty():
            # находим все ФАЙЛЫ с расширением .py 
            # в текущем рабочем каталоге 
            # и его подкаталогах
            scripts = getScripts(os.getcwd(), *PY)

            for file in scripts:
                try:
                    addMods(file, *SPECS)
                    leadToValid(file)
                    makeExecFile(file)
                except Exception as e:
                    print(e)
                    print(file)
        else:
            while True:
                try:
                    # здесь удобно использовать input() тк она
                    # удаляет '\n' автоматически в конце ввода строки
                    # хотя всё это можно было бы компактнее организовать
                    # например через for
                    # for file in sys.stdin: ...
                    file = input()
                except EOFError:             # если достигли конца файла или ввода
                    break                    # завершаем бесконечный цикл
                else:
                    if os.path.isfile(file):
                        addMods(file, *SPECS)
                        leadToValid(file)
                        makeExecFile(file)
    else:
        if os.path.isfile(sys.argv[1]):
            file = sys.argv[1]
            addMods(file, *SPECS)
            leadToValid(file)
            makeExecFile(file)
