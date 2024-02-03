# Дипломна робота

## Прогнозування результатів вступної кампанії до закладів вищої освіти на основі моделей машинного навчання
> _— Що ти тут робиш?_ <br>
> _— Намагаюсь навчити дерево передбачати майбутнє освіти в країні..._

### Зміст
* [Опис проекту](#about)
* [Прогрес](#progress)
* [Результати](#results)

### <a name="about"></a> Опис проекту
Ця робота присвячена прогнозуванню результатів вступної кампанії до закладів вищої освіти за допомогою моделей машинного навчання.
Основна мета — визначити та розробити ефективні методи передбачення кількості виділених бюджетних місць на основі аналізу даних з вступних кампаній з 2018-го по 2023-й роки.
У планах створення практичного додатка для використання отриманих моделей у реальному часі.

### <a name="progress"></a> Прогрес
- [X] [Збір даних](https://github.com/Natanius18/diploma/tree/master/web_scraping)
- [X] [Попередня обробка](https://github.com/Natanius18/diploma/blob/master/data_processing/data_preprocessing.ipynb)
- [X] [Аналіз даних](https://github.com/Natanius18/diploma/blob/master/data_processing/data_analysis.ipynb)
- [X] [Побудова лінійних моделей машинного навчання](https://github.com/Natanius18/diploma/blob/master/data_processing/linear_models.ipynb)
- [X] [Дерево рішень](https://github.com/Natanius18/diploma/blob/master/data_processing/decision_tree.ipynb)
  * візуалізація дерева за допомогою graphviz, [pdf](https://github.com/Natanius18/diploma/blob/master/data_processing/tree_structure.pdf)
  * візуалізація дерева за допомогою drteeviz, [великий svg файл](https://drive.google.com/file/d/1ziFkgu4TSQH-hWnhufSrnQgf5Qr_dsoF/view?usp=sharing)
- [X] [Випадковий ліс](https://github.com/Natanius18/diploma/blob/master/data_processing/random_forest.ipynb)
- [ ] [Boosting](https://github.com/Natanius18/diploma/blob/master/data_processing/boosting.ipynb)
- [ ] Метод головних компонент (PCA)
- [ ] Створення додатка для передбачення

### <a name="results"></a> Результати
![Порівняння результатів навчання моделей](tools/r2_and_mse.png?raw=true)
