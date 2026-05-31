#!/bin/zsh
echo "Добро пожаловать в автоматизированную систему обработки корпоративной почты"
echo ""
echo "Требуется ли установка pytest?"
echo "1) Да"
echo "2) Нет"
read firstAns
if [ "$firstAns" = "1" ]; then
  echo "Выполняется установка..."
  python3 -m pip install pytest
  echo "Установка завершена"
fi
echo "Очистить результаты предыдущих сортировок?"
echo "1) Да"
echo "2) Нет"
read ans
if [ "$ans" = "1" ]; then
    find SortedInbox -type f -delete
    echo "Папки очищены."
fi
echo ""
echo "Запускаем программу..."
cd src
python3 main.py
cd ..
echo ""
echo "Показать отчет по сортировке?"
echo "1) Да"
echo "2) Нет"
read ans
if [ "$ans"="1" ]; then
  important=$(find SortedInbox/Important -type f | wc -l)
  incidents=$(find SortedInbox/Incidents -type f | wc -l)
  noreply=$(find SortedInbox/Noreply -type f | wc -l)
  other=$(find SortedInbox/Other -type f | wc -l)
  questions=$(find SortedInbox/Questions -type f | wc -l)
  security=$(find SortedInbox/Security -type f | wc -l)
  spam=$(find SortedInbox/Spam -type f | wc -l)
  unreadable=$(find SortedInbox/Unreadable -type f | wc -l)
  total=$((important+incidents+noreply+other+questions+security+spam+unreadable))
  echo "Отчет по сортировке:"
  echo ""
  echo "Important : $important"
  echo "Incidents : $incidents"
  echo "Noreply.  : $noreply"
  echo "Other     : $other"
  echo "Questions : $questions"
  echo "Security  : $security"
  echo "Spam      : $spam"
  echo "Unreadable: $unreadable"
echo ""
echo "Всего файлов: $total"
fi
echo ""
echo "Работа завершена"